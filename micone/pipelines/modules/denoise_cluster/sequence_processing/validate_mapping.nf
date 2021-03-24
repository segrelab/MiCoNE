// Step0: Checking validity of the mapping file
process validate_mapping {
    tag "$id"
    publishDir "${output_dir}", mode: 'copy', overwrite: true

    input:
    file(mapping_file)

    output:
    file "*"
    stdout is_map_valid

    script:
    template 'denoise_cluster/sequence_processing/validate_mapping.sh'
}

