#!/usr/bin/env Rscript

suppressWarnings(library(dada2))

multithread <- ${ncpus}
maxEE <- ${max_ee}
truncQ <- ${trunc_q}
forward_trim_cmd <- "forward_trim.txt"
reverse_trim_cmd <- "reverse_trim.txt"

forward_untrimmed.reads <- list.files(".", pattern="_R1_001.fastq.gz\$", full.names=TRUE)
reverse_untrimmed.reads <- list.files(".", pattern="_R2_001.fastq.gz\$", full.names=TRUE)

  if(length(forward_untrimmed.reads) == 0) {
    errQuit("No input files with the expected filename format found.")
  }
  if(length(reverse_untrimmed.reads) == 0) {
    errQuit("No input files with the expected filename format found.")
  }

# read trim and filter commands
forward_trim.cmd <- read.csv(forward_trim_cmd, header=FALSE)
reverse_trim.cmd <- read.csv(reverse_trim_cmd, header=FALSE)
trimLeft <- c(forward_trim.cmd[1,2], reverse_trim.cmd[1,2])
truncLen <- c(forward_trim.cmd[2,2], reverse_trim.cmd[2,2])


# trim sequences
forward_trimmed.reads <- file.path("trimmed", basename(forward_untrimmed.reads))
reverse_trimmed.reads <- file.path("trimmed", basename(reverse_untrimmed.reads))
out <- suppressWarnings(
    filterAndTrim(
        forward_untrimmed.reads,
        forward_trimmed.reads,
        reverse_untrimmed.reads,
        reverse_trimmed.reads,
        truncLen=truncLen,
        trimLeft=trimLeft,
        maxEE=maxEE,
        truncQ=truncQ,
        rm.phix=TRUE,
        multithread=multithread
    )
)

# check trimmed reads
cat(ifelse(file.exists(forward_trimmed.reads), ".", "x"), sep="")
cat(ifelse(file.exists(reverse_trimmed.reads), ".", "x"), sep="")
trimmed.reads <- list.files("trimmed", pattern=".fastq.gz\$", full.names=TRUE)
cat("\n")
if(length(trimmed.reads) == 0) { # All reads were filtered out
  errQuit("No reads passed the filter (was truncLen longer than the read length?)", status=2)
}

manifest <- read.csv("MANIFEST", header=TRUE, check.names=FALSE)
manifest_trimmed <- manifest[manifest[, "filename"] %in% basename(trimmed.reads),]

write.csv(manifest_trimmed, "trimmed/MANIFEST", row.names=FALSE, quote=FALSE)
