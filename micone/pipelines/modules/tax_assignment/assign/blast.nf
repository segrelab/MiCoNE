// Blast representative sequences against the blast database
process blast {
    label 'qiime2'
    tag "${id}"
    input:
        tuple val(id), file(repseq_artifact), file(taxmap_artifact), file(refseq_artifact)
    output:
        tuple val(id), file("taxonomy.tsv")
    script:
        template 'tax_assignment/assign/assign_taxonomy_blast.sh'
}
