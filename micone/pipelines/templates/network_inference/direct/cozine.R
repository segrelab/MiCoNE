#!/usr/bin/env Rscript

library(COZINE)


otu_file <- "${otu_file}"
corr_file <- "${meta.id}_corr.tsv"
lambda.min.ratio <- as.double("${lambda_min_ratio}")

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

# Calculate hurdle function and pcorr matrix
hf <- cozine(dat = otu_t, parallel = FALSE, lambda.min.ratio = lambda.min.ratio)
mat <- as.matrix(hf\$adjMat[[which.min(hf\$BIC_etc\$BIC)]])
# NOTE: This returns a non-symmetric matrix, hence we need to symmetrize it
otuNetwork <- (mat + t(mat)) / 2

write.table(otuNetwork, file = corr_file, quote = FALSE, col.names = NA, sep = "\\t")
