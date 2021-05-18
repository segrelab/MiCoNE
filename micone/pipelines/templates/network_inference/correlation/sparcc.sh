#!/usr/bin/env bash

fastspar --iterations ${iterations} --yes \
    --otu_table ${otu_file} \
    --correlation ${meta.id}_corr.tsv \
    --covariance ${meta.id}_cov.tsv \
    --threads ${ncpus}

function do_fastspar {
    args=(\$(echo \$1 | tr "," "\\n"))
    number=\$args[0]
    otu_table=\$args[0]
    fastspar --iterations ${iterations} --yes \
        --otu_table \$otu_table \
        --correlation ${meta.id}_\${number}_corr.boot \
        --covariance ${meta.id}_\${number}_cov.boot \
        --threads ${ncpus}
}

find . -name "*_otu.boot" | awk '{print NR "," $0}' | parallel -j ${ncpus} do_fastspar
