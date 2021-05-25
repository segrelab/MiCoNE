// input:
// samplesheet
// id,otu_table,rep_seqs,samplemetadata
// output1:
// tuple val(meta), file(otu_table), file(rep_seqs), file(samplemetadata)
// output2:
// tuple val(meta), file(otu_table_wtax)

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
    if (!file(row.samplemetadata).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Samplemetadata file does not exist!\n${row.samplemetadata}"
    }
    array = [ meta, file(row.otu_table), file(row.rep_seqs), file(row.samplemetadata) ]
    return array
}
