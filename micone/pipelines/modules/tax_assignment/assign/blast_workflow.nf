include { import_reads } from './import_reads.nf'
include { blast } from './blast.nf'
include { add_md2biom } from './add_md2biom.nf'


workflow blast_workflow {
    take:
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta'), file(samplemetadata_files)
        input_channel
    main:
        input_channel \
            | import_reads
        blast(
            import_reads.out,
            params.tax_assignment.assign['blast']['references']
        )
        add_md2biom(blast.out)
    emit:
        // add_md2biom has publishDir
        // tuple val(meta), file("otu_table_wtax.biom")
        add_md2biom.out
}
