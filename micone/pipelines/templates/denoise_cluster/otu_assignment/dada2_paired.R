#!/usr/bin/env Rscript

suppressWarnings(library(dada2))

big.data <- ${big_data}
multithread <- ${ncpus}

# get files
# Forward and reverse fastq filenames have format: SAMPLENAME_R1_001.fastq and SAMPLENAME_R2_001.fastq
filtFs <- sort(list.files(".", pattern="_R1_001.fastq.gz\$", full.names=TRUE))
filtRs <- sort(list.files(".", pattern="_R2_001.fastq.gz\$", full.names=TRUE))
# Extract sample names, assuming filenames have format: SAMPLENAME_XXX.fastq
sample.file.names <- sapply(strsplit(basename(filtFs), "_"), `[`, 1)
sample.file.namesR <- sapply(strsplit(basename(filtRs), "_"), `[`, 1)

if(!identical(sample.file.names, sample.file.namesR)) stop("Forward and reverse files do not match.")

manifest <- read.csv("MANIFEST", header=TRUE, comment.char='#')
sample.names <- sort(unique(manifest\$sample.id))

names(filtFs) <- sample.names
names(filtRs) <- sample.names


# Denoising
if(big.data) {
    # Learn forward error rates
    errF <- learnErrors(filtFs, nbases=1e8, multithread=multithread)
    # Learn reverse error rates
    errR <- learnErrors(filtRs, nbases=1e8, multithread=multithread)
    # Sample inference and merger of paired-end reads
    mergers <- vector("list", length(sample.names))
    names(mergers) <- sample.names
    for(sam in sample.names) {
        cat("Processing:", sam, "\n")
        derepF <- derepFastq(filtFs[[sam]])
        ddF <- dada(derepF, err=errF, multithread=multithread)
        derepR <- derepFastq(filtRs[[sam]])
        ddR <- dada(derepR, err=errR, multithread=multithread)
        merger <- mergePairs(ddF, derepF, ddR, derepR)
        mergers[[sam]] <- merger
    }
    rm(derepF); rm(derepR)
} else {
    # get error rates
    errF <- learnErrors(filtFs, multithread=multithread)
    errR <- learnErrors(filtRs, multithread=multithread)
    # NOTE: This now supports filepaths directly (no need to derep)
    # apply the dada2 algorithm
    dadaFs <- dada(filtFs, err=errF, multithread=multithread)
    dadaRs <- dada(filtRs, err=errR, multithread=multithread)
    # merge paired reads
    mergers <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, verbose=TRUE)
}

seq.table <- makeSequenceTable(mergers)
rownames(seq.table) <- sample.names

write.table(t(seq.table), file="seq_table.tsv", col.names=NA, sep="\\t")
