#!/usr/bin/env Rscript

library(propr)

otu_file <- "${otu_file}"
corr_file <- "${otu_file.baseName.split('_otu')[0]}_corr.tsv"

read_otu <- function(otufile) {
    otu <- read.table(otufile, header=TRUE, comment.char="", sep="\\t")
    rownames(otu) <- otu[, 1]
    otu <- otu[, 2:ncol(otu)]
    return(otu)
}


otu <- read_otu(otu_file)

pr <- propr(t(otu), metric = "rho", ivar = "clr")
mat <- pr@matrix
matdims <- rep(list(rownames(otu)), 2)
dimnames(mat) <- matdims

write.table(mat, file=corr_file, sep="\\t", quote=FALSE, col.names=NA)
