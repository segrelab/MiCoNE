#!/usr/bin/env nextflow

def correlations = params.correlations
def pvalues = params.pvalues
def sample_metadata = params.sample_metadata
def lineagedata = params.lineagedata
def childrendata = params.childrendata
def output_dir = file(params.output_dir)
def metadata = params.metadata

Channel
    .fromPath(correlations)
    .ifEmpty {exit 1, "Correlation files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_corr")[0],
            it
        )
    }
    .into { correlation_chnl_all; correlation_chnl_otu }

Channel
    .fromPath(pvalues)
    .ifEmpty {exit 1, "Pvalue files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_pval")[0],
            it
        )
    }
    .into { pvalue_chnl_all; pvalue_chnl_otu }

Channel
    .fromPath(sample_metadata)
    .ifEmpty {exit 1, "Sample metadata files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_sample_metadata")[0],
            it
        )
    }
    .set { sample_metadata_chnl }

Channel
    .fromPath(lineagedata)
    .ifEmpty {exit 1, "Taxondata files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_taxondata")[0],
            it
        )
    }
    .into { taxondata_chnl_all; taxondata_chnl_otu }

Channel
    .fromPath(childrendata)
    .ifEmpty {exit 1, "Childrendata files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_children")[0],
            it
        )
    }
    .set { childrendata_chnl }

Channel
    .fromPath(metadata)
    .ifEmpty {exit 1, "Metadata files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it
        )
    }
    .set { metadata_chnl }

sample_metadata_chnl
    .map { tuple(it[0], it[1]) }
    .set { levels_chnl }

levels_chnl
    .combine(metadata_chnl, by: 0)
    .into { combined_metadata_chnl_all; combined_metadata_chnl_otu }

correlation_chnl_all
    .join(pvalue_chnl_all, by: [0, 1])
    .join(combined_metadata_chnl_all, by: [0, 1])
    .join(taxondata_chnl_all, by: [0, 1])
    .join(childrendata_chnl, by: [0, 1])
    .set { jsonnet_input_chnl_all }

correlation_chnl_otu
    .join(pvalue_chnl_otu, by: [0, 1])
    .join(combined_metadata_chnl_otu, by: [0, 1])
    .join(taxondata_chnl_otu, by: [0, 1])
    .filter { it[1] == 'OTU_level' }
    .set { jsonnet_input_chnl_otu }

process make_jsonnet_all {
    tag "${id}|${level}"
    publishDir "${output_dir}/make_jsonnet/${id}"

    input:
    set val(id), val(level), file(correlation_file), file(pvalue_file), file(metadata_file), file(taxondata_file), file(childrendata_file) from jsonnet_input_chnl_all

    output:
    set val(id), val(level), file('*_net.json') into jsonnet_output_chnl_all

    script:
    {{ make_jsonnet }}
}

process make_jsonnet_otu {
    tag "${id}|${level}"
    publishDir "${output_dir}/make_jsonnet/${id}"

    input:
    set val(id), val(level), file(correlation_file), file(pvalue_file), file(metadata_file), file(taxondata_file) from jsonnet_input_chnl_otu

    output:
    set val(id), val(level), file('*_net.json') into jsonnet_output_chnl_otu

    script:
    """
    #!/usr/bin/env python3
    from mind.utils import CooccurNet
    network = CooccurNet.load_data(
        corr_file="$correlation_file",
        pval_file="$pvalue_file",
        meta_file="$metadata_file",
        lineage_file="$taxondata_file"
    )
    json_str = network.network_json
    with open('${id}_${level}_net.json', 'w') as fid:
        fid.write(json_str)
    """
}