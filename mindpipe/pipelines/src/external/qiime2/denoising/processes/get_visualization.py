#!/usr/bin/env python3

from qiime2 import Artifact
from qiime2.plugins import demux


def get_visulization(demux_sequence_file):
    demux_sequences = Artifact.load(demux_sequence_file)
    demux_viz = demux.visualizers.summarize(demux_sequences)
    demux_viz.visualization.export_data("output")


if __name__ == "__main__":
    DEMUX_SEQUENCES = "${sequence_artifact}"
    get_visulization(DEMUX_SEQUENCES)
