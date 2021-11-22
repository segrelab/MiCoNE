"""
    Module that deals with validation of the pipeline results
"""

import ast
from itertools import chain, groupby
import multiprocessing as mp
from operator import itemgetter
import pathlib
import re
import subprocess
from typing import Dict, List, Tuple

import pandas as pd
import simplejson

from .otu_validator import OtuValidator
from .network_schema import NodesModel, LinksModel, NetworkmetadataModel


def validate_pipeline(history_file: pathlib.Path) -> str:
    """Check if the pipeline execution was successful
    We assume that the last run pipeline is the target

    Parameters
    ----------
    history_file : pathlib.Path
        The path to the nextflow history file

    Returns
    -------
    str
        success or fail
    """
    history: pd.DataFrame = pd.read_table(history_file, header=None, sep="\t")
    status = history.iloc[-1, 3]
    if status == "ERR":
        return "fail"
    elif status == "OK":
        return "success"
    else:
        raise ValueError("Unknown status")


def process_trace(trace_file: pathlib.Path) -> Dict[str, List[str]]:
    """Process the nextflow trace file and return the processes that succeeded and failed

    Parameters
    ----------
    trace_file : pathlib.Path
        The path to the trace file

    Returns
    -------
    Dict[str, List[str]]
        A dictionary that lists the "success" processes and "fail" processes
    """
    trace: pd.DataFrame = pd.read_table(trace_file, index_col=0, sep="\t")
    trace_grouped = trace.groupby("status")
    trace_summary = {"success": [], "fail": []}
    for group_label, ids in trace_grouped.groups.items():
        if group_label in {"CACHED", "COMPLETED"}:
            trace_summary["success"].extend([trace.loc[id_, "name"] for id_ in ids])
        elif group_label in {"FAILED"}:
            trace_summary["fail"].extend([trace.loc[id_, "name"] for id_ in ids])
        else:
            raise ValueError(f"Unknown group label {group_label}")
    return trace_summary


def validate_biom_file(biom_file: pathlib.Path) -> Tuple[str, pathlib.Path]:
    """Validate biom file

    Parameters
    ----------
    biom_file : pathlib.Path
        Path to the biom file

    Returns
    -------
    Tuple[str, pathlib.Path]
        result, path to biom file
    """
    otu_validator = OtuValidator(dtype="biom", ext="biom")
    try:
        otu_validator.load_validate(biom_file)
        result = "success"
    except:
        result = "fail"
    return result, biom_file


def validate_biom_results(
    biom_files: List[pathlib.Path], ncpus: int = 1
) -> Dict[str, List[pathlib.Path]]:
    """Validate the biom files in the pipeline output
    The biom files must contain observation and sample metadata

    Parameters
    ----------
    biom_files : List[pathlib.Path]
        The list of biom files to validate
    ncpus : int, optional
        The number of cpus to use
        Default value is 1

    Returns
    -------
    Dict[str, List[str]]
        Dictionary containing the "success" files and "fail" files
    """
    args = biom_files
    with mp.Pool(processes=ncpus) as pool:
        results = pool.map(validate_biom_file, args)
    results_dict = {
        k: [v[-1] for v in g]
        for k, g in groupby(sorted(results, key=itemgetter(0)), key=itemgetter(0))
    }
    return results_dict


def validate_network_file(network_file: pathlib.Path) -> Tuple[str, pathlib.Path]:
    """Validate network file

    Parameters
    ----------
    network_file : pathlib.Path
        Path to the network file

    Returns
    -------
    Tuple[str, pathlib.Path]
        result, path to network file
    """
    with open(network_file, "r") as fid:
        data = simplejson.load(fid)
    # Validation
    nodes_model = NodesModel({"nodes": data["nodes"]}, strict=False)
    links_model = LinksModel({"links": data["links"]}, strict=False)
    non_meta_keys = ["nodes", "links"]
    metadata = {k: v for k, v in data.items() if k not in non_meta_keys}
    networkmetadata_model = NetworkmetadataModel(metadata, strict=False)
    try:
        nodes_model.validate()
        links_model.validate()
        networkmetadata_model.validate()
        result = "success"
    except:
        result = "fail"
    return result, network_file


def validate_network_results(
    network_files: List[pathlib.Path], ncpus: int = 1
) -> Dict[str, List[pathlib.Path]]:
    """Validate the network files in the pipeline output
    These must be `Network` objects not `NetworkGroup` objects

    Parameters
    ----------
    network_files : List[pathlib.Path]
        The list of network files to validate
    ncpus : int, optional
        The number of cpus to use
        Default value is 1

    Returns
    -------
    Dict[str, List[str]]
        Dictionary containing the "success" files and "fail" files
    """
    args = network_files
    with mp.Pool(processes=ncpus) as pool:
        results = pool.map(validate_network_file, args)
    results_dict = {
        k: [v[-1] for v in g]
        for k, g in groupby(sorted(results, key=itemgetter(0)), key=itemgetter(0))
    }
    return results_dict


def validate_expected_results(
    execution_dir: pathlib.Path, trace_file: pathlib.Path, output_dir: pathlib.Path
) -> Dict[str, List[str]]:
    """Compare expected results (from nextflow config) with produced results
    This needs to be run in the conda environment

    Parameters
    ----------
    execution_dir : pathlib.Path
        The path to the pipeline execution directory
    trace_file : pathlib.Path
        The path to the trace file
    output_dir : pathlib.Path
        The path to the output directory

    Returns
    -------
    Dict[str, List[str]]
        List of modules that "success" or "fail"
    """
    cmd = ["nextflow", "config", "-flat", execution_dir]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    modules = list(
        chain(
            *[
                ast.literal_eval(re.search(r"(\['.*?'\])", s).group(1))
                for s in stdout.decode("utf-8").split("\n")
                if "selection =" in s
            ]
        )
    )
    results = {"success": [], "fail": []}
    for module in modules:
        # Check the trace file for success
        trace = process_trace(trace_file)
        module_failures = [module for failure in trace["fail"] if module in failure]
        # Check the outputs dir for folder
        module_dirs = [dir for dir in output_dir.glob(f"**/{module}*") if dir.is_dir()]
        if not module_failures and module_dirs:
            results["success"].append(module)
        else:
            results["fail"].append(module)
    return results


def check_results(pipeline_dir: pathlib.Path, procs: int):
    """Run all the validation functions on the pipeline_dir
    1. validate_pipeline(history_file)
    2. process_trace(trace_file)
    3. validate_biom_results(biom_files, procs)
    4. validate_network_results(network_files, procs)
    5. validate_expected_results(pipeline_dir, trace_file, output_dir)

    Returns
    -------
    tuple
        A tuple containing results from the processes in the order specified above
    """
    history_file = pipeline_dir / ".nextflow/history"
    trace_file = pipeline_dir / "trace.txt"
    output_dir = pipeline_dir / "outputs"
    biom_files = list(pathlib.Path("outputs/tax_assignment").glob("**/*.biom"))
    network_files = list(
        pathlib.Path("outputs/network_inference/network").glob(
            "make_network_with_pvalue/**/*_network.json"
        )
    ) + list(
        pathlib.Path("outputs/network_inference/network").glob(
            "make_network_without_pvalue/**/*_network.json"
        )
    )
    return (
        validate_pipeline(history_file),
        process_trace(trace_file),
        validate_biom_results(biom_files, procs),
        validate_network_results(network_files, procs),
        validate_expected_results(pipeline_dir, trace_file, output_dir),
    )
