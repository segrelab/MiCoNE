// input:
// samplesheet
// id,trimmed_sequences,manifest,sample_metadata
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
        .multiMap { it ->
            reads: tuple(it[0], it[1], it[2])
            sample_md: tuple(it[0], it[3])
        }
        .set { result }

    emit:
    reads = result.reads
    sample_md = result.sample_md
}


def create_dc_channels(LinkedHashMap row) {
    def meta = [:]
    meta.id = row.id
    def array = []
    if (!file(row.trimmed_sequences).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Trimmed_Sequences file does not exist!\n${row.trimmed_sequences}"
    }
    if (!file(row.manifest).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Manifest file does not exist!\n${row.manifest}"
    }
    if (!file(row.sample_metadata).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Sample_Metadata file does not exist!\n${row.sample_metadata}"
    }
    array = [ meta, file(row.trimmed_sequences), file(row.manifest), file(row.sample_metadata) ]
    return array
}
