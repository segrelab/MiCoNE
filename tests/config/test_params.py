"""
    Module containing tests for the Params class
"""

import pytest

from mindpipe.config import InternalParamsSet, ExternalParamsSet
from mindpipe.config.params import Params


@pytest.mark.usefixtures("pipeline_settings")
class TestParamsSet:
    """ Tests for ParamsSet class """

    def test_init(self, pipeline_settings):
        internal_raw = pipeline_settings["internal"]
        external_raw = pipeline_settings["external"]
        assert InternalParamsSet(internal_raw)
        assert ExternalParamsSet(external_raw)
        wrong_format = {
            "root": "src/internal/split_otu_table",
            "output_location": "split_otu_table",
            "input": [{"datatype": "sequence_16s", "format": ["fasta"]}],
            "output": [
                {"datatype": "otu_table", "format": ["biom"], "location": "*.biom"}
            ],
            "parameters": [{"process": "something", "data": 123}],
        }
        assert Params(("wrong_format", wrong_format))
        with pytest.raises(TypeError):
            Params(("wrong_format", {**wrong_format, "input": "string"}))
        with pytest.raises(TypeError):
            Params(("wrong_format", {**wrong_format, "output": "string"}))
        with pytest.raises(TypeError):
            Params(("wrong_format", {**wrong_format, "parameters": "string"}))
        with pytest.raises(ValueError):
            Params(
                (
                    "wrong_format",
                    {**wrong_format, "input": [{"datatype": "sequence_16s"}]},
                )
            )
        with pytest.raises(ValueError):
            Params(
                (
                    "wrong_format",
                    {**wrong_format, "output": [{"datatype": "sequence_16s"}]},
                )
            )
        with pytest.raises(ValueError):
            Params(("wrong_format", {**wrong_format, "parameters": [{"data": "temp"}]}))

    def test_iter_len(self, pipeline_settings):
        internal_raw = pipeline_settings["internal"]
        internal = InternalParamsSet(internal_raw)
        assert len(internal_raw) == len(internal)
        for process in internal:
            assert isinstance(process, Params)
        external_raw = pipeline_settings["external"]
        external = ExternalParamsSet(external_raw)
        count = 0
        for l1 in external_raw:
            for l2 in external_raw[l1]:
                for l3 in external_raw[l1][l2]:
                    count += 1
        assert count == len(external)
        for process in external:
            assert isinstance(process, Params)

    def test_contains_getitem(self, pipeline_settings):
        internal_raw = pipeline_settings["internal"]
        external_raw = pipeline_settings["external"]
        internal = InternalParamsSet(internal_raw)
        external = ExternalParamsSet(external_raw)
        test_internal_key = list(internal_raw.keys())[0]
        for l1 in external_raw:
            for l2 in external_raw[l1]:
                for l3 in external_raw[l1][l2]:
                    test_external_key = f"{l1}.{l2}.{l3}"
                    assert test_external_key in external
        assert test_internal_key in internal

    def test_param_get(self, pipeline_settings):
        internal_raw = pipeline_settings["internal"]
        internal = InternalParamsSet(internal_raw)
        curr_param = internal["group_by_taxa"]
        assert curr_param.get("otu_table", category="input")
        assert curr_param.get("group_by_taxa", category="parameters")
        assert curr_param.get("children_map", category="output")

    # TODO: Add tests for dict, merge, attach_to
