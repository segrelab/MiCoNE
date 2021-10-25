// input:
// samplesheet
// id,run,forward,reverse,barcodes,mapping,sample_metadata
// output1:
// tuple val(meta), file(forward_files), file(reverse_files), file(barcode_files), file(mapping_files)
// output2:
// tuple val(meta), file(sample_metadata_files)

workflow spp_data_ingestion {
    take:
    samplesheet

    main:
    samplesheet
        .splitCsv(header: true, sep: ',')
        .map { create_spp_channels(it) }
        .multiMap { row ->
            reads: tuple(row[0], row[1], row[2], row[3], row[4])
            sample_md: tuple(row[0], row[5])
        }
        .set { result }

    emit:
    reads = result.reads
    sample_md = result.sample_md
}


def create_spp_channels(LinkedHashMap row) {
    def meta = [:]
    meta.id = row.id
    meta.run = row.run
    def array = []
    if (!file(row.forward).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Forward sequences file does not exist!\n${row.forward_sequences}"
    }
    if (!file(row.reverse).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Reverse sequences file does not exist!\n${row.reverse_sequences}"
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
    array = [ meta, file(row.forward), file(row.reverse), file(row.barcodes), file(row.mapping), file(row.sample_metadata) ]
    return array
}
