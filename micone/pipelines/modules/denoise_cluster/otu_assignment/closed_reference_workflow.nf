include { join_reads } from './join_reads.nf'
include { fastq2fasta } from './fastq2fasta.nf'
include { closed_reference } from './closed_reference.nf'
include { hash_otutables } from './hash_otutables.nf'


workflow closed_reference_workflow {
    take:
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata), file(samplemetadata_files)
        input_channel
    main:
        if (params.paired_end) {
            input_channel \
                | join_reads \
                | fastq2fasta
        } else {
            input_channel \
                | fastq2fasta
        }
        closed_reference(
            fastq2fasta.out,
            params.denoise_cluster.otu_assignment['closed_reference']['reference_sequences']
        )
        hash_otutables(
            closed_reference.out.meta_channel.first(),
            closed_reference.out.otu_channel.collect(),
            closed_reference.out.repseq_channel.collect(),
            closed_reference.out.samplemetadata_channel.collect()
        )
    emit:
        // hash_otutables has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hash_otutables.out
}
