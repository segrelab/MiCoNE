#!/usr/bin/env python3

import networkx as nx
import numpy as np
import pandas as pd


def main(otu_file, network_file, output_file):
    otu_table = pd.read_table(otu_file, index_col=0)
    graph = nx.read_gml(network_file)
    nodes = otu_table.index
    size = (len(nodes), len(nodes))
    interaction_table = pd.DataFrame(
        np.zeros(size, dtype=float), index=nodes, columns=nodes
    )
    directed = nx.is_directed(graph)
    for source, target, data in graph.edges(data=True):
        if (source in nodes) and (target in nodes):
            interaction_table.loc[source, target] = data["weight"]
            if not directed:
                interaction_table.loc[target, source] = data["weight"]
    interaction_table.to_csv(output_file, sep="\\t", index=True, float_format="%.4f")


if __name__ == "__main__":
    OTU_FILE = "${otu_file}"
    NETWORK_FILE = "${network_file}"
    OUTPUT_FILE = "${meta.id}_corr.tsv"
    main(OTU_FILE, NETWORK_FILE, OUTPUT_FILE)
