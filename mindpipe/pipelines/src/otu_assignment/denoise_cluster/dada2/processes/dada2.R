#!/usr/bin/env Rscript

suppressWarnings(library(dada2))

big.data <- ${big_data}
multithread <- ${ncpus}

# Load fastq files
reads <- list.files(".", pattern=".fastq", full.names=TRUE)

# Load sample names from manifest file
manifest <- read.csv("MANIFEST", comment.char="#")
sample.names <- manifest\$sample.id
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

# Export sequences
uniquesToFasta(
   getUniques(seq.table),
   fout="unhashed_rep_seqs.fasta",
   ids=paste0("Seq", seq(length(getUniques(seq.table))))
)

# Export to biom
library(biomformat)
st.biom <- make_biom(t(seq.table))
write_biom(st.biom, "unhashed_otu_table.biom")
