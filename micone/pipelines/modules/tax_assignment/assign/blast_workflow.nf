include { import_reads } from './import_reads.nf'
include { import_references } from './import_references.nf'
include { blast } from './blast.nf'
include { add_md2biom } from './add_md2biom.nf'


workflow blast_workflow {
    take:
        // tuple val(id), file(rep_seqs)
        rep_seqs_channel
        // tuple val(id), file(ref_seqs)
        // TODO: This should be made a `${params.blast.ref_seqs}`
        ref_seqs_channel
        // tuple val(id), file(sample_metadata)
        otu_table_channel
        // tuple val(id), file(sample_metadata)
        sample_metadata_channel
        // TODO: rep_seqs, otu_table and sample_metadata should ideally be in one channel
        // otu_table and rep_seqs come out of the same channel but sample_metadata is input
    main:
        rep_seqs_channel | import_reads
        // FIXME: This process uses ref_seqs file directly in the script as `params.ref_seqs`
        ref_seqs_channel | import_references
        import_reads.out.combine(import_references.out) \
            | blast \
            | join(otu_table_channel) \
            | join(sample_metadata_channel) \
            | add_md2biom
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        add_md2biom.out
}
