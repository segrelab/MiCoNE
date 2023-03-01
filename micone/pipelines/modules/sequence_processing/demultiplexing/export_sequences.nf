include { getHierarchy } from '../../../functions/functions.nf'

// Export the sequences and fix the manifest file
process export_sequences {
    label 'qiime2'
    tag "${meta.id}-${meta.run}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/demultiplexed_sequences/${meta.id}-${meta.run}",
        saveAs: { filename -> filename.split("/")[1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(demux_artifact)
    output:
    tuple val(meta), file('demux_seqs/*.fastq.gz'), file('demux_seqs/MANIFEST'), file('demux_seqs/metadata.yml')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        sample_filter = params.sequence_processing.demultiplexing['export_sequences']['sample_filter']
        template 'sequence_processing/demultiplexing/export_sequences.sh'
}
