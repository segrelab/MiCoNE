#!/usr/bin/env Rscript

library(mLDM)
library(caret)

otu_file <- "${otu_file}"
sample_metadata <- "${sample_metadata}"
Z_mean <- as.double("${Z_mean}")
max_iteration <- as.integer("${max_iteration}")
corr_file <- "${meta.id}_corr.tsv"

read_otu_data <- function(tablefile) {
    table <- read.table(tablefile, header=TRUE, check.names=FALSE, comment.char="", sep="\\t")
    table.rownames <- table[, 1]
    table <- table[, 2:ncol(table)]
    table.matrix <- data.matrix(table)
    rownames(table.matrix) <- table.rownames
    return(table.matrix)
}

read_sample_data <- function(tablefile) {
    table <- read.table(tablefile, header=TRUE, check.names=FALSE, comment.char="", sep="\\t")
    table.rownames <- table[, 1]
    table <- as.data.frame(table[, 2:ncol(table)])
    dmy <- dummyVars(" ~ .", data=table)
    table.frame <- data.frame(predict(dmy, newdata=table))
    table.matrix <- data.matrix(table.frame)
    rownames(table.matrix) <- table.rownames
    return(table.matrix)
}

otu <- read_otu_data(otu_file)
otu_t <- t(otu)
sample.md <- read_sample_data(sample_metadata) # Must be purely numeric or categorical metadata

mldmNetwork <- mLDM(X=otu_t, M=sample.md, Z_mean=Z_mean, max_iteration=max_iteration, verbose=TRUE)

otuNetwork <- mldmNetwork\$optimal[[9]]

rownames(otuNetwork) <- rownames(otu)
colnames(otuNetwork) <- rownames(otu)

# In case of incorrect convergence
otuNetwork[otuNetwork > 1] <- 1
otuNetwork[otuNetwork < -1] <- -1

write.table(otuNetwork, file=corr_file, quote=FALSE, col.names=NA, sep="\\t")
