include { join_reads } from './join_reads.nf'
include { fastq2fasta } from './fastq2fasta.nf'
include { open_reference } from './open_reference.nf'
include { hashing2 } from './hashing2.nf'


workflow open_reference_workflow {
    take:
        // tuple val(meta), file(trimmed_sequences), file(manifest_file), file(samplemetadata_files)
        input_channel
    main:
        if (params.paired_end) {
            input_channel \
                | join_reads \
                | fastq2fasta \
                | open_reference \
                | hashing2
        } else {
            input_channel \
                | fastq2fasta \
                | open_reference \
                | hashing2
        }
    emit:
        // hashing2 has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hashing2.out
}
