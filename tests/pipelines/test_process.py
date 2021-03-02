"""
    Module containing tests for the `Process` class
"""

import pathlib
import os

import pytest

from micone.config import ParamsSet
from micone.pipelines import Process
from micone.config.params import Input


def setup_internal(
    pipeline_settings,
    example_pipelines,
    module="network_inference",
    pipeline="network_inference.network.make_network_with_pvalue",
):
    internal_raw = pipeline_settings[module]
    internal = ParamsSet(internal_raw)
    if "." in pipeline:
        pipeline_fname = pipeline.replace(".", "_")
    else:
        pipeline_fname = pipeline
    user_settings = example_pipelines[pipeline_fname]
    params = internal[pipeline]
    if "." in pipeline:
        levels = pipeline.split(".")
        x = user_settings
        for i in range(len(levels)):
            x = x[levels[i]]
        params.merge(x)
    else:
        params.merge(user_settings[pipeline])
    return params


def setup_external(
    pipeline_settings,
    example_pipelines,
    module="otu_assignment",
    pipeline="otu_assignment.sequence_processing.demultiplex_454",
):
    external_raw = pipeline_settings[module]
    external = ParamsSet(external_raw)
    if "." in pipeline:
        pipeline_fname = pipeline.replace(".", "_")
    else:
        pipeline_fname = pipeline
    user_settings = example_pipelines[pipeline_fname]
    params = external[pipeline]
    if "." in pipeline:
        levels = pipeline.split(".")
        x = user_settings
        for i in range(len(levels)):
            x = x[levels[i]]
        params.merge(x)
    else:
        params.merge(user_settings[pipeline])
    return params


@pytest.mark.usefixtures("pipeline_settings", "example_pipelines")
class TestInternalProcess:
    """ Tests for the `Process` class """

    def test_init(self, pipeline_settings, example_pipelines):
        params = setup_internal(pipeline_settings, example_pipelines)
        assert Process(params, profile="local", output_location=".")

    def test_update_location(self, pipeline_settings, example_pipelines):
        params = setup_internal(pipeline_settings, example_pipelines)
        process = Process(params, profile="local", output_location=".")
        output_dir = pathlib.Path.home() / "Documents/results"
        process.update_location(str(output_dir), "input")
        for input_ in process.params.input:
            assert str(input_.location).startswith(str(pathlib.Path.home()))
        for output_ in process.params.output:
            assert not output_.location.is_absolute()
        process.update_location(str(output_dir), "output")
        for output_ in process.params.output:
            assert str(output_.location).startswith(str(pathlib.Path.home()))

    def test_build_bad(self, pipeline_settings, example_pipelines, tmpdir):
        params = setup_internal(pipeline_settings, example_pipelines)
        process = Process(params, profile="local", output_location=".")
        process_dir = tmpdir.mkdir("test_process_build")
        output_dir = pathlib.Path.cwd() / "tests/data"
        with pytest.raises(FileNotFoundError):
            process.build(process_dir)
        process.update_location(str(output_dir), "input")
        process.build(process_dir)

    def test_build_good(self, pipeline_settings, example_pipelines, tmpdir):
        params = setup_internal(
            pipeline_settings,
            example_pipelines,
            module="otu_processing",
            pipeline="otu_processing.filter.group",
        )
        process = Process(params, profile="local", output_location=".")
        process_dir = tmpdir.mkdir("test_process_build")
        output_dir = pathlib.Path.cwd() / "tests/data"
        process.update_location(str(output_dir), "input")
        process.build(process_dir)
        script_file = os.path.join(process_dir, "otu_processing.filter.group.nf")
        config_file = os.path.join(process_dir, "otu_processing.filter.group.config")
        assert os.path.exists(script_file)
        assert os.path.exists(config_file)

    def test_cmd(self, pipeline_settings, example_pipelines, tmpdir):
        params = setup_internal(
            pipeline_settings,
            example_pipelines,
            module="otu_processing",
            pipeline="otu_processing.filter.group",
        )
        process = Process(params, profile="local", output_location=".")
        assert process.cmd
        process_dir = tmpdir.mkdir("test_process_cmd")
        output_dir = pathlib.Path.cwd() / "tests/data"
        process.update_location(str(output_dir), "input")
        process.build(process_dir)
        cmd = process.cmd
        paths = [p for p in str(cmd).split(" ") if not p.startswith("-") and "/" in p]
        for path in paths:
            if path.endswith(".config") or path.endswith(".nf"):
                assert pathlib.Path(path).exists()

    def test_run(self, pipeline_settings, example_pipelines, tmpdir):
        params = setup_internal(
            pipeline_settings,
            example_pipelines,
            module="otu_processing",
            pipeline="otu_processing.filter.group",
        )
        process = Process(params, profile="local", output_location=".")
        process_dir = tmpdir.mkdir("test_process_run")
        output_dir = pathlib.Path.cwd() / "tests/data"
        process.update_location(str(output_dir), "input")
        process.build(process_dir)
        process.run()
        assert process.output
        assert not process.error
        process.log()
        for output in process.params.output:
            if "*" in str(output.location):
                str_loc = str(output.location)
                ind = str_loc.find("*")
                files = list(pathlib.Path(str_loc[:ind]).glob(str_loc[ind:]))
                assert len(files) > 0
            else:
                assert output.location.exists()

    @pytest.mark.filterwarnings("ignore::UserWarning")
    def test_clean(self, pipeline_settings, example_pipelines, tmpdir):
        params = setup_internal(
            pipeline_settings,
            example_pipelines,
            module="otu_processing",
            pipeline="otu_processing.filter.group",
        )
        process = Process(params, profile="local", output_location=".")
        process_dir = tmpdir.mkdir("test_process_clean")
        output_dir = pathlib.Path.cwd() / "tests/data"
        process.update_location(str(output_dir), "input")
        process.build(process_dir)
        cmd = process.cmd
        paths = [p for p in str(cmd).split(" ") if not p.startswith("-") and "/" in p]
        process.run()
        process.wait()
        for path in paths:
            assert pathlib.Path(path).exists()
        process.clean("all")
        for path in paths:
            assert not pathlib.Path(path).exists()
        process.build(process_dir)
        process.clean("work_dir")
        for path in paths:
            if "work" in path:
                assert not pathlib.Path(path).exists()
            else:
                if not path.endswith(".log"):
                    assert pathlib.Path(path).exists()

    @pytest.mark.filterwarnings("ignore::UserWarning")
    def test_attach_to(self, pipeline_settings, example_pipelines, tmpdir):
        previous_params = setup_internal(
            pipeline_settings,
            example_pipelines,
            module="otu_processing",
            pipeline="otu_processing.transform.normalize",
        )
        previous_process = Process(
            previous_params, profile="local", output_location="."
        )
        curr_params = setup_internal(
            pipeline_settings,
            example_pipelines,
            module="otu_processing",
            pipeline="otu_processing.filter.group",
        )
        curr_process = Process(curr_params, profile="local", output_location=".")
        output_dir = pathlib.Path.cwd() / "tests/data"
        previous_process.update_location(str(output_dir), "input")
        previous_process.build(tmpdir)
        curr_process.attach_to(previous_process)
        with pytest.raises(FileNotFoundError):
            curr_process.build(tmpdir)
        previous_process.run()
        previous_process.output
        curr_process.update_location(str(output_dir), "input")
        curr_process.build(tmpdir)
        curr_process.run()

    def test_dict(self, pipeline_settings, example_pipelines, tmpdir):
        params = setup_internal(
            pipeline_settings,
            example_pipelines,
            module="otu_processing",
            pipeline="otu_processing.filter.group",
        )
        process = Process(params, profile="local", output_location=".")
        process_dir = tmpdir.mkdir("test_process_dict")
        output_dir = pathlib.Path.cwd() / "tests/data"
        process.update_location(str(output_dir), "input")
        process.build(process_dir)
        assert process.params.input
        assert process.params.output
        assert process.params.root_dir
        for params in process.params.parameters:
            assert params.process in params


@pytest.mark.usefixtures("pipeline_settings", "example_pipelines")
class TestExternalProcess:
    """ Tests for the `Process` class """

    def test_init(self, pipeline_settings, example_pipelines):
        params = setup_external(pipeline_settings, example_pipelines)
        assert Process(params, profile="local", output_location=".")

    def test_run(self, pipeline_settings, example_pipelines, tmpdir):
        params = setup_external(
            pipeline_settings,
            example_pipelines,
            module="network_inference",
            pipeline="network_inference.correlation.sparcc",
        )
        process = Process(params, profile="local", output_location=".")
        process_dir = tmpdir.mkdir("test_process_run")
        output_dir = pathlib.Path.cwd() / "tests/data"
        process.update_location(str(output_dir), "input")
        process.build(process_dir)
        process.run()
        assert process.output
        assert not process.error
        process.log()
        for output in process.params.output:
            if "*" in str(output.location):
                str_loc = str(output.location)
                ind = str_loc.find("*")
                files = list(pathlib.Path(str_loc[:ind]).glob(str_loc[ind:]))
                assert len(files) > 0
            else:
                assert output.location.exists()

    @pytest.mark.filterwarnings("ignore::UserWarning")
    def test_ix_attach_to(self, pipeline_settings, example_pipelines, tmpdir):
        sparcc_params = setup_external(
            pipeline_settings,
            example_pipelines,
            module="network_inference",
            pipeline="network_inference.correlation.sparcc",
        )
        json_params = setup_internal(pipeline_settings, example_pipelines)
        to_remove = []
        for io_elem in json_params.input:
            if io_elem.datatype in {"interaction_table"}:
                to_remove.append(io_elem)
        for remove in to_remove:
            json_params.input.remove(remove)
            json_params.input.add(Input(datatype=remove.datatype, format=remove.format))
        sparcc_process = Process(sparcc_params, profile="local", output_location=".")
        json_process = Process(json_params, profile="local", output_location=".")
        output_dir = pathlib.Path.cwd() / "tests/data"
        sparcc_process.update_location(str(output_dir), "input")
        sparcc_process.build(tmpdir)
        json_process.attach_to(sparcc_process)
        json_process.update_location(str(output_dir), "input")
        with pytest.raises(FileNotFoundError):
            json_process.build(tmpdir)
        sparcc_process.run()
        sparcc_process.wait()
        json_process.build(tmpdir)
        json_process.run()
        json_process.wait()
