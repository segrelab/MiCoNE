#!/usr/bin/env julia

using Distributed
addprocs(${ncpus})

@everywhere using FlashWeave

using CSV
using DataFrames
metadata_path = "fmt-control-Family_sample_metadata.tsv"

# data
data_path = "${otu_file}"
new_data_path = "${otu_file.baseName}.tsv"
if data_path != new_data_path
    cp(data_path, new_data_path, force=true, follow_symlinks=true)
end
metadata_path = "${sample_metadata}"
# NOTE: Transposing directly here does not work if the column names are long
metadata = CSV.read(metadata_path, DataFrame)
metadata_transpose = DataFrame(
    [[names(metadata)]; collect.(eachrow(metadata))], [:column; Symbol.(axes(metadata, 1))]
)
new_metadata_path = "${sample_metadata.baseName}_transposed.tsv"
CSV.write(new_metadata_path, metadata_transpose; writeheader=false, delim="\\t")

# options
sensitive = ${sensitive}
heterogeneous = ${heterogeneous}
FDR = ${fdr_correction}

netw_results = learn_network(
new_data_path,
new_metadata_path,
sensitive=sensitive,
heterogeneous=heterogeneous,
FDR=FDR,
transposed=true,
)

# You need to use networkx to export the .gml to table
output_file = "${meta.id}_network.gml"
save_network(output_file, netw_results)
