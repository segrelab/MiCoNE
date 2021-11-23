#!/usr/bin/env Rscript

suppressWarnings(library(dada2))

chimera.method <- "${chimera_method}"
multithread <- as.integer("${ncpus}")

# load table and convert to matrix
seq.table.file <- "${seqtable_file}"
seq.table <- read.csv(seq.table.file, sep = "\\t", check.names = FALSE)
rownames(seq.table) <- seq.table[, 1]
seq.table <- seq.table[-c(1)]
seq.mat <- data.matrix(seq.table)
mode(seq.mat) <- "integer"

# chimera removal
seq.table.nochim <- removeBimeraDenovo(t(seq.mat), method = chimera.method, multithread = multithread, verbose = TRUE)

# Export sequences
uniquesToFasta(
  getUniques(seq.table.nochim),
  fout = "unhashed_rep_seqs.fasta",
  ids = paste0("Seq", seq(length(getUniques(seq.table.nochim))))
)
write.table(t(seq.table.nochim), file = "seq_table_nochim.tsv", col.names = NA, sep = "\\t", quote = FALSE)

# Export to biom
system("biom convert -i seq_table_nochim.tsv -o unhashed_otu_table.biom --to-hdf5")
