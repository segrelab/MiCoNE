include { import_files } from './import_files.nf'
include { uchime } from './uchime.nf'
include { export_files } from './export_files.nf'


workflow uchime_workflow {
    take:
        // tuple val(id), file(otutable_file), file(repseqs_file), file(samplemetadata_files)
        input_channel
    main:
        input_channel \
            | import_files \
            | uchime \
            | export_files
    emit:
        // export_files has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        export_files.out
}
