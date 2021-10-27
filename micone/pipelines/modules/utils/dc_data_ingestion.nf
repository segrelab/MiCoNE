// input:
// samplesheet
// id,run,trimmed_sequences,manifest,sequence_metadata,sample_metadata
// output1:
// tuple val(meta), file(trimmed_sequences), file(manifest_file)
// output2:
// tuple val(meta), file(sample_metadata_files)

workflow dc_data_ingestion {
    take:
    samplesheet

    main:
    samplesheet
        .splitCsv(header: true, sep: ',')
        .map { create_dc_channels(it) }
        .set { result }
    emit:
    result
}


def create_dc_channels(LinkedHashMap row) {
    def meta = [:]
    meta.id = row.id
    meta.run = row.run
    def array = []
    if (!file(row.trimmed_sequences)) {
        exit 1, "ERROR: Please check input samplesheet -> Trimmed_Sequences file does not exist!\n${row.trimmed_sequences}"
    }
    if (!file(row.manifest).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Manifest file does not exist!\n${row.manifest}"
    }
    if (!file(row.sequence_metadata).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Sequence_Metadata file does not exist!\n${row.sequence_metadata}"
    }
    if (!file(row.sample_metadata).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Sample_Metadata file does not exist!\n${row.sample_metadata}"
    }
    array = [ meta, file(row.trimmed_sequences), file(row.manifest), file(row.sequence_metadata), file(row.sample_metadata) ]
    return array
}
