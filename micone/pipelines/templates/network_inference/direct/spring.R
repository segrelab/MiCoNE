#!/usr/bin/env Rscript

library(SPRING)

otu_file <- "${otu_file}"
corr_file <- "${meta.id}_corr.tsv"
nlambda <- as.double("${nlambda}")
lambda.min.ratio <- as.double("${lambda_min_ratio}")
ncpus <- as.integer("${ncpus}")

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

# Apply SPRING on QMP data.
fit.spring <- SPRING(otu_t,
  nlambda = nlambda,
  lambda.min.ratio = lambda.min.ratio,
  ncores = ncpus,
  Rmethod = "approx",
  quantitative = FALSE,
  lambdaseq = "data-specific",
  rep.num = 50,
  verbose = TRUE
)

# StARS-selected lambda index based on the threshold (default = 0.01)
opt.K <- fit.spring\$output\$stars\$opt.index
# Estimated adjacency matrix from sparse graphical modeling technique ("mb" method) (1 = edge, 0 = no edge)
adj.K <- as.matrix(fit.spring\$fit\$est\$path[[opt.K]])
# Estimated partial correlation coefficient, same as negative precision matrix.
pcor.K <- as.matrix(SpiecEasi::symBeta(fit.spring\$output\$est\$beta[[opt.K]], mode = "maxabs"))

# In case of incorrect convergence
pcor.K[pcor.K > 1] = 1
pcor.K[pcor.K < -1] = -1

otuNetwork <- pcor.K
rownames(otuNetwork) <- rownames(otu)
colnames(otuNetwork) <- rownames(otu)
write.table(otuNetwork, file = corr_file, quote = FALSE, col.names = NA, sep = "\\t")
