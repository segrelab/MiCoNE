include { import_files } from './import_files.nf'
include { uchime } from './uchime.nf'
include { export_files } from './export_files.nf'


workflow uchime_workflow {
    take:
        // tuple val(id), file(otu_table), file(rep_seqs)
        input_channel
    main:
        input_channel \
            | import_files \
            | uchime \
            | export_files
    emit:
        // has `publishDir` -> ${params.output_dir}/${id}
        export_files.out
}
