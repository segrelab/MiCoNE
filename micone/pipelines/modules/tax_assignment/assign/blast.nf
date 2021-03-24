// TODO: Move these to workflows
chnl_repseqs_artifact
    .combine(chnl_reftax_artifact)
    .tuple { chnl_repseqs_reftax }

// Step2: Blast representative sequences against the blast database
process assign_taxonomy {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    tuple val(id), file(repseq_artifact), file(taxmap_artifact), file(refseq_artifact)
    output:
    tuple val(id), file("taxonomy.tsv")
    script:
    template 'tax_assignment/assign/assign_taxonomy_blast.sh'
}
