// input:
// samplesheet
// id,sequences,barcodes,mapping,sample_metadata
// output1:
// tuple val(meta), file(sequence_files), file(barcode_files), file(mapping_files)
// output2:
// tuple val(meta), file(sample_metadata_files)

workflow sps_data_ingestion {
    take:
    samplesheet

    main:
    samplesheet
        .splitCsv(header: true, sep: ',')
        .map { create_sps_channels(it) }
        .multiMap { it ->
            reads: tuple(it[0], it[1], it[2], it[3])
            sample_md: tuple(it[0], it[4])
        }
        .set { result }

    emit:
    reads = result.reads
    sample_md = result.sample_md
}


def create_sps_channels(LinkedHashMap row) {
    def meta = [:]
    meta.id = row.id
    def array = []
    if (!file(row.sequences).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Sequences file does not exist!\n${row.sequences}"
    }
    if (!file(row.barcodes).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Barcodes file does not exist!\n${row.barcodes}"
    }
    if (!file(row.mapping).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Mapping file does not exist!\n${row.mapping}"
    }
    if (!file(row.sample_metadata).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Sample_Metadata file does not exist!\n${row.sample_metadata}"
    }
    array = [ meta, file(row.sequences), file(row.barcodes), file(row.mapping), file(row.sample_metadata) ]
    return array
}
