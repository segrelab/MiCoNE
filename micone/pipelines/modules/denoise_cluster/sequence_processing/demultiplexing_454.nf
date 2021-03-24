// TODO: Move this to the workflow
map_validity = is_map_valid
                .map { e ->
                    if (e == 'No errors or warnings were found in mapping file.\n')
                       'No errors pipeline execution proceeding'
                    else
                        exit 1, 'Mapping file has errors'
                }

// Step1: Create lists of [id, sequence, quality] for each sample
sequence_data_chnl
    .join(quality_data_chnl)
    .tuple { combined_data_chnl }

// Step2: Pass the above list of file-locations as comma-separated strings to `split_libraries.py`
process demultiplexing_fasta {
    tag "demultiplexing_454"
    publishDir "${output_dir}", mode: 'copy', overwrite: true

    input:
    val(all_data)
    file(mapping)

    output:
    file('*.fna')

    script:
    combined_data = all_data
                    .inject(['', '']) {
            acc, x -> acc.withIndex().collect { e, i -> (e + ',' + x[i+1])}
        } .collect { it[1..-1] }
    (sequences, qualities) = combined_data
    template 'denoise_cluster/sequence_processing/demultiplexing_fasta.sh'
}
