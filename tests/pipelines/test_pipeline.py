"""
    Module containing tests for the `Pipeline` class
"""

import pathlib

import pytest

from micone.pipelines import Pipeline


@pytest.mark.usefixtures("example_pipelines")
class TestPipeline:
    """ Tests for the `Pipeline` class """

    def test_pipeline_init(self, example_pipeline_files):
        user_settings = example_pipeline_files["grouptaxa_sparcc_json"]
        assert Pipeline(user_settings, profile="local")

    def test_pipeline_len_getitem(self, example_pipeline_files):
        user_settings = example_pipeline_files["grouptaxa_sparcc_json"]
        pipeline = Pipeline(user_settings, profile="local")
        assert len(pipeline) == 6
        process = pipeline["network_inference.network.make_network.1"]
        assert process == "network_inference.network.make_network.1"

    @pytest.mark.filterwarnings("ignore::UserWarning")
    def test_pipeline_run(self, example_pipeline_files, tmpdir):
        user_settings = example_pipeline_files["grouptaxa_sparcc_json"]
        pipeline_dir = tmpdir.mkdir("test_pipeline")
        input_dir = pathlib.Path.cwd() / "tests/data"
        pipeline = Pipeline(
            user_settings,
            profile="local",
            output_location=pipeline_dir,
            base_dir=input_dir,
        )
        for process in pipeline.run():
            process.wait()
            process.log()
            assert process.status == "success"
