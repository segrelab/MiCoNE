#!/usr/bin/env nextflow

def correlations = params.correlations
def obs_metadata = params.obs_metadata
def children_map = params.children_map
def cmetadata = file(params.cmetadata)
def metadata = file(params.metadata)
def output_dir = file(params.output_dir)

Channel
    .fromPath(correlations)
    .ifEmpty {exit 1, "Correlation files not found"}
    .map { tuple(
        (it.getParent().baseName + '_' + it.baseName.split("_corr")[0]),
        it.getParent().baseName,
        it.baseName.split("_corr")[0],
        it
    ) }
    .set { chnl_correlation }

Channel
    .fromPath(obs_metadata)
    .ifEmpty {exit 1, "Observation metadata files not found"}
    .map { tuple(
        (it.getParent().baseName + '_' + it.baseName.split("_obs_metadata")[0]),
        it
    ) }
    .set { chnl_obs_metadata }

Channel
    .fromPath(children_map)
    .ifEmpty {exit 1, "Childrendata files not found"}
    .map { tuple(
        (it.getParent().baseName + '_' + it.baseName.split("_children")[0]),
        it
    ) }
    .set { chnl_children_map }

chnl_correlation
    .join(chnl_obs_metadata, by: 0)
    .join(chnl_children_map, by: 0)
    .set { chnl_input }

process make_network {
    tag "$id"
    publishDir "${output_dir}/${dataset}", mode: 'copy', overwrite: true

    input:
    set val(id), val(dataset), val(level), file(corr_file), file(obsdata_file), file(childrenmap_file) from chnl_input

    output:
    set val(id), file('*_network.json') into chnl_output

    script:
    {{ make_network }}
}
