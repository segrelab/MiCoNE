// Step1b: Import references
process import_references {
    tag: "${id}"
    label: 'qiime2'
    output:
    tuple file('tax_map.qza'), file('reference_sequences.qza')
    script:
    template 'tax_assignment/assign/import_references.sh'
}

