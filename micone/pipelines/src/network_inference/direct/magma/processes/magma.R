#!/usr/bin/env Rscript

library(SpiecEasi)
library(rMAGMA)

otu_file <- "${otu_file}"
corr_file <- "${otu_file.baseName.split('_otu')[0]}_corr.tsv"

read_otu <- function(otufile) {
    otu <- read.table(otufile, header=TRUE, comment.char="", sep="\\t")
    rownames(otu) <- otu[, 1]
    otu <- otu[, 2:ncol(otu)]
    return(otu)
}


otu <- read_otu(otu_file)

magma.result <- magma(data = t(otu))
cov <- MASS::ginv(magma.result\$opt.icov)
secor <- cov2cor(cov)
mat <- as.matrix(secor*magma.result\$refit)
matdims <- rep(list(rownames(otu)), 2)
dimnames(mat) <- matdims

write.table(mat, file=corr_file, sep="\\t", quote=FALSE, col.names=NA)
