#!/usr/bin/env python3

from qiime2 import Artifact


def main(input_type, input_path, input_format, output_path):
    imported_artifact = Artifact.import_data(
        input_type, input_path, view_type=input_format
    )
    imported_artifact.save(output_path)


if __name__ == "__main__":
    INPUT_TYPE = "SampleData[SequencesWithQuality]"
    INPUT_PATH = "MANIFEST"
    INPUT_FORMAT = "SingleEndFastqManifestPhred33"
    OUTPUT_PATH = "${id}_sequences.qza"
    main(INPUT_TYPE, INPUT_PATH, INPUT_FORMAT, OUTPUT_PATH)
