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
        corr_file <- paste0("${meta.id}", "_corr.tsv")
    }
    pr <- propr(t(otu), metric = "rho", ivar = "clr")
    mat <- pr@matrix
    matdims <- rep(list(rownames(otu)), 2)
    dimnames(mat) <- matdims
    if(otu_file == corr_file) stop("Correlation file and OTU file names are the same")
    write.table(mat, file=corr_file, sep="\\t", quote=FALSE, col.names=NA)
    return(corr_file)
}

apply_propr("${otu_file}", bootstrap=FALSE)

bootstrap_files = list.files(pattern="*_otu.boot")
results <- mclapply(bootstrap_files, apply_propr, mc.cores = ncpus)
