#!/usr/bin/env Rscript

suppressWarnings(library(dada2))

big.data <- ${big_data}
multithread <- ${ncpus}

# Load file names and sample names from manifest file
manifest <- read.csv("MANIFEST", comment.char="#")
reads <- sapply(as.character(manifest\$absolute.filepath), basename)
sample.names <- as.character(manifest\$sample.id)
names(reads) <- sample.names

# Denoising
if(big.data) {
    reads.err <- learnErrors(reads, nbases=1e8, multithread=multithread,  randomize=TRUE)
    reads.dada <- vector("list", length(sample.names))
    names(reads.dada) <- sample.names
    for(sample in sample.names) {
        cat("Processing:", sample, "\\n")
        read.derep <- derepFastq(reads[[sample]])
        reads.dada[[sample]] <- dada(read.derep, err=reads.err, multithread=multithread)
    }
} else {
    reads.err <- learnErrors(reads, multithread=multithread)
    reads.derep <- derepFastq(reads)
    reads.dada <- dada(reads.derep, err=reads.err, multithread=multithread)
}

seq.table <- makeSequenceTable(reads.dada)
rownames(seq.table) <- sample.names

write.table(t(seq.table), file="seq_table.tsv", col.names=NA, sep="\\t")
