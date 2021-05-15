// demultiplex
process demultiplexing_illumina {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(sequence_artifact), file(mapping_file)
    output:
        tuple val(meta), file('*_demux.qza')
    script:
        meta.demultiplexing = "illumina"
        rev_comp_barcodes = params.denoise_cluster.sequence_processing['demultiplexing_illumina']['rev_comp_barcodes']
        rev_comp_mapping_barcodes = params.denoise_cluster.sequence_processing['demultiplexing_illumina']['rev_comp_mapping_barcodes']
        rcb = rev_comp_barcodes == 'True' ? '--p-rev-comp-barcodes' : '--p-no-rev-comp-barcodes'
        rcmb = rev_comp_mapping_barcodes == 'True' ? '--p-rev-comp-mapping-barcodes' : '--p-no-rev-comp-mapping-barcodes'
        template 'denoise_cluster/sequence_processing/demultiplex_illumina.sh'
}
