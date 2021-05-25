// input:
// samplesheet
// id,otu_table,obs_metadata,sample_metadata,children_map
// output1:
// tuple val(meta), file(otu_table), file(obs_metadata), file(sample_metadata), file(children_map)

workflow ni_data_ingestion {
    take:
    samplesheet

    main:
    samplesheet
        .splitCsv(header: true, sep:',')
        .map { create_ni_channels(it) }
        .set { result }

    emit:
    result
}

def create_ni_channels(LinkedHashMap row) {
    def meta = [:]
    meta.id = row.id
    def array = []
    if (!file(row.otu_table).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Otu_Table file does not exist!\n${row.sequences}"
    }
    if (!file(row.obs_metadata).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Obs_Metadata file does not exist!\n${row.barcodes}"
    }
    if (!file(row.sample_metadata).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Sample_Metadata file does not exist!\n${row.sample_metadata}"
    }
    if (!file(row.children_map).exists()) {
        exit 1, "ERROR: Please check input samplesheet -> Children_Map file does not exist!\n${row.children_map}"
    }
    array = [ meta, file(row.otu_table), file(row.obs_metadata), file(row.sample_metadata), file(row.children_map) ]
    return array
}
