// TODO: Move this to workflows
// Join sequence_files, manifest_file and trim_cmd
chnl_seqs_trim
    .join(chnl_manifest_trim, by: 0)
    .join(chnl_trimcmd_trim, by: 0)
    .tuple { chnl_trim }

// 4. Trimming the sequences using cutadapt
process trimming {
    tag "${id}"
    publishDir "${output_dir}/${id}", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
    tuple val(id), file(sequence_files), file(manifest_file), file(trim_cmd)
    output:
    tuple val(id), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST')
    script:
    template 'denoise_cluster/sequence_processing/trimming.R'
}
