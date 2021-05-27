#!/usr/bin/env python3

from qiime2 import Artifact
from qiime2.plugins import demux


def main(sequence_artifact, seq_samplesize, output_dir):
    demux_artifact = Artifact.load(sequence_artifact)
    demux_viz = demux.visualizers.summarize(demux_artifact, n=seq_samplesize)
    demux_viz.visualization.export_data(output_dir)


if __name__ == "__main__":
    SEQUENCE_ARTIFACT = "${sequence_artifact}"
    SEQ_SAMPLESIZE = ${seq_samplesize}
    OUTPUT_DIR = "output"
    main(SEQUENCE_ARTIFACT, SEQ_SAMPLESIZE, OUTPUT_DIR)
