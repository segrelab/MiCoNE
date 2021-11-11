#!/usr/bin/env Rscript

library(propr)
library(parallel)

ncpus <- ${ncpus}

# cl <- makeCluster(ncpus)

read_otu <- function(otu_file) {
    otu <- read.table(otu_file, header=TRUE, comment.char="", check.names=FALSE, sep="\\t")
    rownames(otu) <- otu[, 1]
    otu <- otu[, 2:ncol(otu)]
    return(otu)
}

apply_propr <- function(otu_file, bootstrap=TRUE) {
    otu <- read_otu(otu_file)
    if(bootstrap) {
        corr_file <- gsub("_otu.boot", "_corr.boot", otu_file)
    } else {
        corr_file <- gsub("_otu.tsv", "_corr.tsv", otu_file)
    }
    pr <- propr(t(otu), metric = "rho", ivar = "clr")
    mat <- pr@matrix
    matdims <- rep(list(rownames(otu)), 2)
    dimnames(mat) <- matdims
    write.table(mat, file=corr_file, sep="\\t", quote=FALSE, col.names=NA)
    return(corr_file)
}

apply_propr("${otu_file}", bootstrap=FALSE)

bootstrap_files = list.files(pattern="*_otu.boot")
results <- mclapply(bootstrap_files, apply_propr, mc.cores = ncpus)
