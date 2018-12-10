#!/usr/bin/env Rscript
library(SpiecEasi)

# NOTE: The data does not have to be normalized
# Read in the OTU table
read_otu <- function(otufile) {
    otu <- read.table(otufile, header = TRUE)
    rownames(otu) <- otu$OTU_ID
    otu <- otu[, 2:ncol(otu)]
    return(otu)
}

# NOTE: You have to transpose the otu_data
# Calculate correlations using SpiecEasi
run_spieceasi <- function(otu_data, method='mb') {
    otu.spieceasi <- spiec.easi(t(otu_data), method=method, lambda.min.ratio=1e-2,
                                nlambda=20, icov.select.params=list(rep.num=50))
    return(otu.spieceasi)
}


# Actual script
otu_data <- read_otu('$resample')
otu_ids <- rownames(otu_data)
spieceasi.out <- run_spieceasi(otu_data, method='mb')
betamat <- as.matrix(symBeta(getOptBeta(spieceasi.out), mode='maxabs'))
matdims <- rep(list(otu_ids), 2)
dimnames(betamat) <- matdims
write.table(betamat, file='$bootname', sep='\t', quote=FALSE)
