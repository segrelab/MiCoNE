#!/usr/bin/env Rscript

suppressWarnings(library(dada2))

big.data <- ${big_data}
multithread <- ${ncpus}

# get files
filts <- sort(list.files(".", pattern="fastq.gz\$", full.names=TRUE))
# Extract sample names, assuming filenames have format: SAMPLENAME_XXX.fastq
sample.file.names <- sapply(strsplit(basename(filts), "_"), `[`, 1)


manifest <- read.csv("MANIFEST", header=TRUE, comment.char='#')
sample.names <- sort(unique(manifest\$sample.id))
names(filts) <- sample.names


# Denoising
if(big.data) {
    err <- learnErrors(filts, nbases = 1e8, multithread=multithread, randomize=TRUE)
    # Infer sequence variants
    dds <- vector("list", length(sample.names))
    names(dds) <- sample.names
    for(sam in sample.names) {
        cat("Processing:", sam, "\n")
        derep <- derepFastq(filts[[sam]])
        dds[[sam]] <- dada(derep, err=err, multithread=multithread)
    }
} else {
    # get error rates
    err <- learnErrors(filts, multithread=multithread)
    # NOTE: This now supports filepaths directly (no need to derep)
    # apply the dada2 algorithm
    dds <- dada(filts, err=err, multithread=multithread)
}

seq.table <- makeSequenceTable(dds)
rownames(seq.table) <- sample.names

write.table(t(seq.table), file="seq_table.tsv", col.names=NA, sep="\\t")
