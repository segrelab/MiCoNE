// Trimming the sequences using cutadapt
process trimming {
    label 'qiime2'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
        tuple val(id), file(trim_cmd), file(sequence_files), file(manifest_file)
    output:
        tuple val(id), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST')
    script:
        template 'denoise_cluster/sequence_processing/trimming.R'
}
