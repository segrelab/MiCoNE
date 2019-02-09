"""
    Module that defines a complete pipeline by incorporating settings and processes
"""

import collections
import pathlib
from typing import Iterator, List, Optional

import networkx as nx
import toml

from ..config import Config
from .process import Process


class Pipeline(collections.Sequence):
    """
        Class that defines the pipeline and contains methods to run the pipeline

        Parameters
        ----------
        user_settings_file : str
            The user created settings file that describes the pipeline
        profile : {'local', 'sge'}
            The execution environment
        base_dir : str, optional
            The absolute location of the base directory for the input files
            This needs to be supplied if the input files location in the settings are relative
            If None, then current working directory is used
        resume : bool, optional
            The flag to determine whether a previous execution is resumed
            Default value is False

        Other Parameters
        ----------------
        title : str, optional
            The title of the pipeline
        order : List[str], optional
            The order of the processes in the pipeline
        output_location : str, optional
            The base output location to store all pipeline results

        Attributes
        ----------
        title : str
            The title of the pipeline
        output_location : str
            The base output location to store all pipeline results
        config : Config
            The configuration object for the `mindpipe` pipelines
        profile : str
            The execution environment for the pipeline
        base_dir : pathlib.Path
            The absolute path to the base input file directory
        process_tree : nx.DiGraph
            The process tree for the pipeline
            Every node has a "process" attribute which contains the `Process` class
    """

    _req_keys = {"title", "order", "output_location"}

    def __init__(
        self,
        user_settings_file: str,
        profile: str,
        base_dir: Optional[str] = None,
        resume: Optional[bool] = False,
        **kwargs,
    ) -> None:
        self.config = Config()
        self.profile = profile
        self.resume = resume
        if base_dir is None:
            self.base_dir = pathlib.Path.cwd()
        else:
            base_path = pathlib.Path(base_dir)
            if base_path.is_absolute() and base_path.exists():
                self.base_dir = base_path
            else:
                raise ValueError("base_dir path must be absolute and must exist")
        user_settings = self._parse_settings(user_settings_file, **kwargs)
        title = kwargs.get("title")
        order = kwargs.get("order")
        output_location = kwargs.get("output_location")
        self.process_tree = self._parse_process_tree(
            order if order else user_settings["order"]
        )
        self.title = title if title else user_settings["title"]
        self.output_location = (
            output_location if output_location else user_settings["output_location"]
        )
        self._create_processes(user_settings)

    @staticmethod
    def _parse_process_tree(process_string: str) -> nx.Graph:
        """
            Parses the process string and creates a process tree from it

            Parameters
            ----------
            process_string : str
                The string that represents the process tree

            Returns
            -------
            nx.Graph
                A nx.Graph representing the process tree
        """
        processes = [
            p for p in process_string.strip().replace("\n", " ").split(" ") if p
        ]
        graph = nx.DiGraph()
        if len(processes) == 1:
            graph.add_node(processes[0])
            return graph
        # NOTE: We do not support forking in the first process
        process_stack = collections.deque([processes[0]])
        delimiters = {"(", ")", "|"}
        for process in processes[1:]:
            if process not in delimiters:
                parent = process_stack.pop()
                if process in graph.nodes:
                    graph.node[process]["count"] += 1
                    count = graph.node[process]["count"]
                    new_process = f"{process}.{count}"
                    graph.add_edge(parent, new_process)
                    process_stack.append(new_process)
                else:
                    graph.add_edge(parent, process)
                    graph.node[process]["count"] = 1
                    process_stack.append(process)
            elif process == "(":
                process_stack.append(process_stack[-1])
            elif process == "|":
                process_stack.pop()
                process_stack.append(process_stack[-1])
            elif process == ")":
                process_stack.pop()
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError(
                "The processes do not form a directed acyclic graph. Please check the order"
            )
        return graph

    def _parse_settings(self, settings_file: str, **kwargs) -> dict:
        """
            Parses the user created settings file

            Parameters
            ----------
            settings_file : str
                The user defined settings file that describes the pipeline

            Returns
            -------
            dict
                The dictionary of verified user settings
        """
        with open(settings_file, "r") as fid:
            settings = toml.load(fid)
        for key in self._req_keys:
            if key not in settings and key not in kwargs:
                raise ValueError(
                    f"Required key '{key}' not found in user_settings or parameters to constructor"
                )
        return settings

    def _create_processes(self, settings: dict) -> None:
        """
            Create `Process` instances and add them to the process_tree

            Parameters
            ----------
            settings : dict
                The dictionary of verified user settings
        """
        # Create processes for each node
        tree = self.process_tree
        for node_name in tree.nodes:
            suffix_flag = ""
            suffixes = [f".{i}" for i in range(len(tree.nodes))]
            for suffix in suffixes:
                if node_name.endswith(suffix):
                    process_name = node_name.rsplit(suffix, 1)[0]
                    suffix_flag = suffix
                    break
            else:
                process_name = node_name
            level_1, level_2, level_3 = process_name.split(".")
            default_process_data = self.config.params_set[process_name]
            user_process_data = settings[level_1][level_2][level_3]
            default_process_data.merge(user_process_data)
            if suffix_flag:
                root_dir = str(default_process_data.root_dir) + suffix_flag
            else:
                root_dir = str(default_process_data.root_dir)
            tree.node[node_name]["process"] = Process(
                default_process_data,
                self.profile,
                str(self.output_location),
                id=node_name,
                root_dir=root_dir,
                resume=self.resume,
            )

    def __iter__(self) -> Iterator:
        return iter(self.process_tree.nodes)

    def __len__(self) -> int:
        return len(self.process_tree.nodes)

    def __getitem__(self, key: str) -> Process:
        for process in self:
            if process.name == key:
                return process
        raise KeyError(f"{key} is not a process of this pipeline")

    def __repr__(self) -> str:
        processes = [process.name for process in self]
        return (
            f"<Pipeline title={self.title} output_location={self.output_location} "
            f"processes={processes}>"
        )

    def __str__(self) -> str:
        return self.title

    def run(self) -> Iterator[Process]:
        """
            Starts the execution of the pipeline
            Returns an iterator over the processes being executed

            Returns
            -------
            Iterator[Process]
                Iterator over each process currently being executed
       """
        # Get the process for the root node and update locations
        tree = self.process_tree
        root_node = next(nx.topological_sort(tree))
        root_node_process = tree.node[root_node]["process"]
        root_node_process.update_location(str(self.base_dir), "input")
        root_path = self.output_location / root_node_process.params.root_dir
        root_node_process.update_location(str(root_path), "output")
        # Attach outputs of parent node to inputs of child node
        for prev_process_name, curr_process_name in nx.bfs_edges(tree, root_node):
            curr_process = tree.node[curr_process_name]["process"]
            prev_process = tree.node[prev_process_name]["process"]
            curr_process.update_location(str(self.base_dir), "input")
            root_path = self.output_location / curr_process.params.root_dir
            curr_process.update_location(str(root_path), "output")
            curr_process.attach_to(prev_process)
        processes = nx.bfs_tree(tree, root_node)
        tree_diag = self.output_location + "/DAG.pdf"
        self.draw_process_tree(tree_diag)
        for process_name in processes:
            process = self.process_tree.node[process_name]["process"]
            loc = pathlib.Path(self.output_location)  # / process.params.output_location
            if self.resume and process.io_exist:
                yield process
            else:
                process.build(str(loc))
                process.run()
                yield process

    def draw_process_tree(self, fpath: str) -> None:
        """
            Draw the DAG chart of the process tree

            Parameters
            ----------
            fpath: str
                The file path where the DAG chart should be saved
        """
        import matplotlib.pyplot as plt

        tree = self.process_tree
        nodes = list(self.process_tree.nodes)
        labels = {n: n.split(".", 2)[-1] for n in nodes}
        pos = nx.drawing.nx_agraph.graphviz_layout(tree, prog="dot")
        nx.draw_networkx_nodes(tree, pos, node_size=500, alpha=0.8)
        nx.draw_networkx_edges(tree, pos, width=1.0, arrows=True)
        text = nx.draw_networkx_labels(tree, pos, labels=labels, font_size=8)
        for _, t in text.items():
            t.set_rotation(30)
        plt.axis("off")
        plt.savefig(fpath)

    # TODO: Create computational metadata
