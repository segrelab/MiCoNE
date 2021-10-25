include { updateMeta } from '../../../functions/functions.nf'

// demultiplex
process demultiplexing_illumina_paired {
    label 'qiime2'
    tag "${new_meta.id}-${new_meta.run}"
    input:
        tuple val(meta), file(sequence_artifact), file(mapping_file)
    output:
        tuple val(new_meta), file('*_demux.qza')
    script:
        new_meta = updateMeta(meta)
        new_meta.demultiplexing = 'illumina'
        barcode_column = params.sequence_processing.demultiplexing['demultiplexing_illumina_paired']['barcode_column']
        rev_comp_barcodes = params.sequence_processing.demultiplexing['demultiplexing_illumina_paired']['rev_comp_barcodes']
        rev_comp_mapping_barcodes = params.sequence_processing.demultiplexing['demultiplexing_illumina_paired']['rev_comp_mapping_barcodes']
        rcb = rev_comp_barcodes ? '--p-rev-comp-barcodes' : '--p-no-rev-comp-barcodes'
        rcmb = rev_comp_mapping_barcodes ? '--p-rev-comp-mapping-barcodes' : '--p-no-rev-comp-mapping-barcodes'
        template 'sequence_processing/demultiplexing/demultiplex_illumina_paired.sh'
}
