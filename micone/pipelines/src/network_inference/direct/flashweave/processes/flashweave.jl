#!/usr/bin/env julia

using Distributed
addprocs(${ncpus})

@everywhere using FlashWeave

using CSV
using DataFrames

# data
data_path = "${otu_file}"
metadata_path = "${sample_metadata}"
metadata = CSV.read(metadata_path, DataFrame; transpose=true)
new_metadata_path = "transposed_" * metadata_path
CSV.write(new_metadata_path, metadata; delim="\\t")

# options
sensitive = ${sensitive}
heterogeneous = ${heterogeneous}
FDR = ${fdr_correction}

netw_results = learn_network(
data_path,
new_metadata_path,
sensitive=sensitive,
heterogeneous=heterogeneous,
FDR=FDR,
transposed=true,
)

# You need to use networkx to export the .gml to table
output_file = "${otu_file.baseName.split('_otu')[0]}_network.gml"
save_network(output_file, netw_results)
