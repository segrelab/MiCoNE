#!/usr/bin/env Rscript

suppressWarnings(library(dada2))

chimera.method <- "${chimera_method}"
multithread <- ${ncpus}

# load table and convert to matrix
seq.table <- read.csv("seq_table.tsv", sep="\\t")
rownames(seq.table) <- seq.table[,1]
seq.table <- seq.table[ -c(1) ]
seq.mat <- data.matrix(seq.table)
mode(seq.mat) <- "integer"

# chimera removal
seq.table.nochim <- removeBimeraDenovo(t(seq.mat), method=chimera.method, multithread=multithread, verbose=TRUE)

# Export sequences
uniquesToFasta(
   getUniques(seq.table.nochim),
   fout="unhashed_rep_seqs.fasta",
   ids=paste0("Seq", seq(length(getUniques(seq.table.nochim))))
)

# Export to biom
library(biomformat)
st.biom <- make_biom(t(seq.table.nochim))
write_biom(st.biom, "unhashed_otu_table.biom")
