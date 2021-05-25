// input:
// samplesheet
// id,otu_table_wtax
// output1:
// tuple val(meta), file(otu_table_wtax)

workflow op_data_ingestion {
    take:
    samplesheet

    main:
    samplesheet
        .splitCsv(header: true, sep:',')
        .map { create_op_channels(it) }
        .set { result }

    emit:
    result
}

def create_op_channels(LinkedHashMap row) {
    def meta = [:]
    meta.id = row.id
    def array = []
    if (!file(row.otu_table_wtax).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Otu_Table_Wtax file does not exist!\n${row.sequences}"
    }
    array = [ meta, file(row.otu_table_wtax) ]
    return array
}
