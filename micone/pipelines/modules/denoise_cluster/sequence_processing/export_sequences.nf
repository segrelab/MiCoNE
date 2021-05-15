// Export the sequences and fix the manifest file
process export_sequences {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f1}/${f2}/${f3}/${meta.id}",
        saveAs: { filename -> filename.split("/")[1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(demux_artifact)
    output:
        tuple val(meta), file('demux_seqs/*.fastq.gz'), file('demux_seqs/MANIFEST')
    script:
        f1, f2, f3 = getHierarchy("${task.process}")
        template 'denoise_cluster/sequence_processing/export_sequences.py'
}
