#!/usr/bin/env Rscript

library(HARMONIES)

otu_file <- "${otu_file}"
corr_file <- "${meta.id}_corr.tsv"
iterations <- as.integer("${iterations}")
sparsity_cutoff <- as.double("${sparsity_cutoff}")

read_otu_data <- function(tablefile) {
  table <- read.table(tablefile, header = TRUE, check.names = FALSE, comment.char = "", sep = "\\t")
  table.rownames <- table[, 1]
  table <- table[, 2:ncol(table)]
  table.matrix <- data.matrix(table)
  rownames(table.matrix) <- table.rownames
  mode(table.matrix) <- "integer"
  return(table.matrix)
}

otu <- read_otu_data(otu_file)
otu_t <- t(otu)

inference.results <- HARMONIES(
  count.matrix = otu_t,
  phenotype = rep(0, nrow(otu_t)),
  N.mcmc = iterations,
  sparsity.cutoff = sparsity_cutoff,
  beta.stars = 0.05,
)

otuNetwork <- inference.results\$partial.corr
rownames(otuNetwork) <- rownames(otu)
colnames(otuNetwork) <- rownames(otu)

# In case of incorrect convergence
otuNetwork[otuNetwork > 1] <- 1
otuNetwork[otuNetwork < -1] <- -1

write.table(otuNetwork, file = corr_file, quote = FALSE, col.names = NA, sep = "\\t")
