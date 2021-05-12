process filter {
    label 'sparcc'
    tag "${id}"
    // publishDir "${params.output_dir}/${task.process}/${id}", saveAs: { filename -> filename.split("/")[-1] }, mode: 'copy', overwrite: true
    input:
        tuple val(id), val(datatuple), val(level), file(boot_file)
    output:
        tuple val(id), val(datatuple), val(level), file('filtered/*.boot')
    script:
        template 'network_inference/bootstrap/filter.py'
}
