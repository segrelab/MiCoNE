// input:
// samplesheet
// id,otu_table,rep_seqs,sample_metadata
// output1:
// tuple val(meta), file(otu_table), file(rep_seqs), file(sample_metadata)

workflow ta_data_ingestion {
    take:
    samplesheet

    main:
    samplesheet
        .splitCsv(header: true, sep:',')
        .map { create_ta_channels(it) }
        .set { result }

    emit:
    result
}

def create_ta_channels(LinkedHashMap row) {
    def meta = [:]
    meta.id = row.id
    def array = []
    if (!file(row.otu_table).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Otu_Table file does not exist!\n${row.sequences}"
    }
    if (!file(row.rep_seqs).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Rep_Seqs file does not exist!\n${row.barcodes}"
    }
    if (!file(row.sample_metadata).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Sample_Metadata file does not exist!\n${row.sample_metadata}"
    }
    array = [ meta, file(row.otu_table), file(row.rep_seqs), file(row.sample_metadata) ]
    return array
}
