#!/usr/bin/env Rscript

library(propr)
libarary(parallel)

ncpus <- ${ncpus}
otu_file <- "${otu_file}"
corr_file <- "${meta.id}_corr.tsv"

# cl <- makeCluster(ncpus)

read_otu <- function(otufile) {
    otu <- read.table(otufile, header=TRUE, comment.char="", sep="\\t")
    rownames(otu) <- otu[, 1]
    otu <- otu[, 2:ncol(otu)]
    return(otu)
}

apply_propr <- function(otufile) {
    otu <- read_otu(otu_file)
    corr_file <- gsub("_otu.boot", "_corr.boot", otu_file)
    pr <- propr(t(otu), metric = "rho", ivar = "clr")
    mat <- pr@matrix
    matdims <- rep(list(rownames(otu)), 2)
    dimnames(mat) <- matdims
    write.table(mat, file=corr_file, sep="\\t", quote=FALSE, col.names=NA)
    return corr_file
}

bootstrap_files = list.files(pattern="*_otu.boot")
results <- mclapply(bootstrap_files, apply_propr, mc.cores = ncpus)
