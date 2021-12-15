#!/usr/bin/env Rscript

library(SpiecEasi)
library(Matrix)

otu_file <- "${otu_file}"
method <- "${method}"
rep.num <- as.integer("${nreps}")
ncpus <- as.integer("${ncpus}")
nlambda <- as.double("${nlambda}")
lambda.min.ratio <- as.double("${lambda_min_ratio}")
corr_file <- "${meta.id}_corr.tsv"

# NOTE: The data does not have to be normalized
# Read in the OTU table
read_otu <- function(otufile) {
  otu <- read.table(otufile, header = TRUE, comment.char = "", check.names = FALSE, sep = "\\t")
  rownames(otu) <- otu[, 1]
  otu <- otu[, 2:ncol(otu)]
  return(otu)
}

# NOTE: You have to transpose the otu_data
# Calculate correlations using SpiecEasi
run_spieceasi <- function(otu_data, method = "mb", rep.num = 50, ncores = 4, nlambda = 20, lambda.min.ratio = 1e-2) {
  otu_ids <- rownames(otu_data)
  otu.spieceasi <- spiec.easi(
    t(otu_data),
    method = method,
    lambda.min.ratio = lambda.min.ratio,
    nlambda = nlambda,
    pulsar.params = list(rep.num = rep.num, ncores = ncores)
  )
  if (method == "mb") {
    sebeta <- symBeta(getOptBeta(otu.spieceasi), mode = "maxabs")
    mat <- as.matrix(sebeta)
  } else if (method == "glasso") {
    secor <- cov2cor(getOptCov(otu.spieceasi))
    mat <- as.matrix(secor * getRefit(otu.spieceasi))
  }
  matdims <- rep(list(otu_ids), 2)
  dimnames(mat) <- matdims
  return(mat)
}


# Actual script
otu_data <- read_otu(otu_file)
spieceasi.corr <- run_spieceasi(
  otu_data,
  method = method,
  rep.num = rep.num,
  ncores = ncpus,
  nlambda = nlambda,
  lambda.min.ratio = lambda.min.ratio
)

# In case of incorrect convergence
spieceasi.corr[spieceasi.corr > 1] <- 1
spieceasi.corr[spieceasi.corr < -1] <- -1

write.table(spieceasi.corr, file = corr_file, sep = "\\t", quote = FALSE, col.names = NA)
