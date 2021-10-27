include { join_reads } from './join_reads.nf'
include { deblur } from './deblur.nf'
include { hashing3 } from './hashing3.nf'


workflow deblur_workflow {
    take:
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata), file(samplemetadata_files)
        input_channel
    main:
        if (params.paired_end) {
            input_channel \
                | join_reads \
                | deblur
        } else {
            input_channel \
                | deblur

        }
        hashing3(deblur.out.collect())
    emit:
        // hashing3 has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hashing3.out
}
