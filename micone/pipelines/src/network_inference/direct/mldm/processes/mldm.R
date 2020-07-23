#!/usr/bin/env Rscript

library(mLDM)

otu_file <- "${otu_file}"
sample_metadata <- "${sample_metadata}"
Z_mean <- ${Z_mean}
max_iteration <- ${max_iteration}
corr_file <- "${otu_file.baseName.split('_otu')[0]}_corr.tsv"

read_data <- function(datafile) {
    data <- read.table(datafile, header=TRUE, comment.char="", sep="\\t")
    data.rownames <- data[, 1]
    data <- data.matrix(data[, 2:ncol(data)])
    rownames(data) <- data.rownames
    return(data)
}

otu <- read_data(otu_file)
sample.md <- read_data(sample_metadata) # Must be purely numeric metadata

mldmNetwork <- mLDM(X=t(otu), M=sample.md, Z_mean=Z_mean, max_iteration=max_iteration, verbose=TRUE)

otuNetwork <- mldmNetwork\$optimal[[9]]
rownames(otuNetwork) <- rownames(otu)
colnames(otuNetwork) <- rownames(otu)

write.table(otuNetwork, file=corr_file, quote=FALSE, col.names=NA, sep="\\t")
