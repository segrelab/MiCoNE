"""
    Module containing tests for the Params class
"""

import pathlib

import pytest

from mindpipe.config import ParamsSet
from mindpipe.config.params import Params


@pytest.mark.usefixtures("pipeline_settings", "example_pipelines")
class TestParamsSet:
    """ Tests for ParamsSet class """

    def test_init(self, pipeline_settings):
        internal_raw = pipeline_settings["otu_processing"]
        assert ParamsSet(internal_raw)
        wrong_format = {
            "env": "mindpipe",
            "output_location": "split_otu_table",
            "input": [{"datatype": "sequence_16s", "format": ["fasta"]}],
            "output": [
                {"datatype": "otu_table", "format": ["biom"], "location": "*.biom"}
            ],
            "parameters": [{"process": "something", "data": 123}],
        }
        assert Params(("otu_processing.filtering.partition", wrong_format))
        with pytest.raises(TypeError):
            Params(
                (
                    "otu_processing.filtering.partition",
                    {**wrong_format, "input": "string"},
                )
            )
        with pytest.raises(TypeError):
            Params(
                (
                    "otu_processing.filtering.partition",
                    {**wrong_format, "output": "string"},
                )
            )
        with pytest.raises(TypeError):
            Params(
                (
                    "otu_processing.filtering.partition",
                    {**wrong_format, "parameters": "string"},
                )
            )
        with pytest.raises(ValueError):
            Params(
                (
                    "otu_processing.filtering.partition",
                    {**wrong_format, "input": [{"datatype": "sequence_16s"}]},
                )
            )
        with pytest.raises(ValueError):
            Params(
                (
                    "otu_processing.filtering.partition",
                    {**wrong_format, "output": [{"datatype": "sequence_16s"}]},
                )
            )
        with pytest.raises(ValueError):
            Params(
                (
                    "otu_processing.filtering.partition",
                    {**wrong_format, "parameters": [{"data": "temp"}]},
                )
            )

    def test_iter_len(self, pipeline_settings):
        external_raw = pipeline_settings["otu_assignment"]
        external = ParamsSet(external_raw)
        count = 0
        for l1 in external_raw:
            for l2 in external_raw[l1]:
                for l3 in external_raw[l1][l2]:
                    count += 1
        assert count == len(external)
        for process in external:
            assert isinstance(process, Params)

    def test_contains_getitem(self, pipeline_settings):
        external_raw = pipeline_settings["otu_assignment"]
        external = ParamsSet(external_raw)
        for l1 in external_raw:
            for l2 in external_raw[l1]:
                for l3 in external_raw[l1][l2]:
                    test_external_key = f"{l1}.{l2}.{l3}"
                    assert test_external_key in external

    def test_param_get(self, pipeline_settings):
        internal_raw = pipeline_settings["otu_processing"]
        internal = ParamsSet(internal_raw)
        curr_param = internal["otu_processing.filtering.group"]
        assert curr_param.get("otu_table", category="input")
        assert curr_param.get("group", category="parameters")
        assert curr_param.get("children_map", category="output")

    def test_param_update_location(self, pipeline_settings):
        external_raw = pipeline_settings["otu_assignment"]
        external = ParamsSet(external_raw)
        curr_param = external[
            "otu_assignment.sequence_processing.demultiplexing_illumina"
        ]
        curr_param.update_location(
            "sequence_16s", location="file_path", category="input"
        )
        assert external[
            "otu_assignment.sequence_processing.demultiplexing_illumina"
        ].get("sequence_16s", "input").location == pathlib.Path("file_path")

    def test_param_merge(self, pipeline_settings, example_pipelines):
        external_raw = pipeline_settings["otu_assignment"]
        external = ParamsSet(external_raw)
        curr_param = external["otu_assignment.sequence_processing.demultiplexing_454"]
        user_settings = example_pipelines["demultiplexing_454"]
        curr_param.merge(
            user_settings["otu_assignment"]["sequence_processing"]["demultiplexing_454"]
        )
        assert curr_param.get("sequence_16s", "input").location == pathlib.Path(
            "/path/to/sequence_16s"
        )
        assert curr_param.get("quality", "input").location == pathlib.Path(
            "/path/to/quality"
        )
        assert curr_param.get(
            "sample_barcode_mapping", "input"
        ).location == pathlib.Path("/path/to/mapping")
