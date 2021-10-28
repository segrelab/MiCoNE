include { join_reads } from './join_reads.nf'
include { fastq2fasta } from './fastq2fasta.nf'
include { de_novo } from './de_novo.nf'
include { hashing2 } from './hashing2.nf'


workflow de_novo_workflow {
    take:
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata), file(samplemetadata_files)
        input_channel
    main:
        if (params.paired_end) {
            input_channel \
                | join_reads \
                | fastq2fasta \
                | de_novo
        } else {
            input_channel \
                | fastq2fasta \
                | de_novo
        }
        hashing2(
            de_novo.out.meta_channel.first(),
            de_novo.out.otu_channel.collect(),
            de_novo.out.repseq_channel.collect(),
            de_novo.out.samplemetadata_channel.collect()
        )
    emit:
        // hashing2 has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hashing2.out
}
