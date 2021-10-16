include { join_reads } from './join_reads.nf'
include { fastq2fasta } from './fastq2fasta.nf'
include { de_novo } from './de_novo.nf'
include { hashing2 } from './hashing2.nf'


workflow de_novo_workflow {
    take:
        // tuple val(meta), file(trimmed_sequences), file(manifest_file), file(samplemetadata_files)
        input_channel
    main:
        if (params.paired_end) {
            input_channel \
                | join_reads \
                | fastq2fasta \
                | de_novo \
                | hashing2
        } else {
            input_channel \
                | fastq2fasta \
                | de_novo \
                | hashing2
        }
    emit:
        // hashing2 has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hashing2.out
}
