#!/usr/bin/env Rscript

suppressWarnings(library(dada2))

multithread <- ${ncpus}
maxEE <- ${max_ee}
truncQ <- ${trunc_q}
trim_cmd <- "${trim_cmd}"

untrimmed.reads <- list.files(".", pattern=".fastq.gz\$", full.names=TRUE)

  if(length(untrimmed.reads) == 0) {
    errQuit("No input files with the expected filename format found.")
  }

# read trim and filter commands
trim.cmd <- read.csv(trim_cmd, header=FALSE)
trimLeft <- trim.cmd[1,2]
truncLen <- trim.cmd[2,2]


# trim sequences
trimmed.reads <- file.path("trimmed", basename(untrimmed.reads))
out <- suppressWarnings(
    filterAndTrim(
        untrimmed.reads,
        trimmed.reads,
        truncLen=truncLen,
        trimLeft=trimLeft,
        maxEE=maxEE,
        truncQ=truncQ,
        rm.phix=TRUE,
        multithread=multithread
    )
)

# check trimmed reads
cat(ifelse(file.exists(trimmed.reads), ".", "x"), sep="")
trimmed.reads <- list.files("trimmed", pattern=".fastq.gz\$", full.names=TRUE)
cat("\n")
if(length(trimmed.reads) == 0) { # All reads were filtered out
  errQuit("No reads passed the filter (was truncLen longer than the read length?)", status=2)
}

file.copy("MANIFEST", "trimmed")
