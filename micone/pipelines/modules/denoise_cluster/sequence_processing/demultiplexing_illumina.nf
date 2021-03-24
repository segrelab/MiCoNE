// TODO: Move this to workflows
chnl_seqartifact
    .join(chnl_mapping)
    .tuple { chnl_demux_input }

// Step3: demultiplex
process demultiplex {
    tag "${id}"
    input:
    tuple val(id), file(sequence_artifact), file(mapping_file)
    output:
    tuple val(id), file('*_demux.qza')
    script:
    def rcb = rev_comp_barcodes == 'True' ? '--p-rev-comp-barcodes' : '--p-no-rev-comp-barcodes'
    def rcmb = rev_comp_mapping_barcodes == 'True' ? '--p-rev-comp-mapping-barcodes' : '--p-no-rev-comp-mapping-barcodes'
    template 'denoise_cluster/sequence_processing/demultiplex_illumina.sh'
}
