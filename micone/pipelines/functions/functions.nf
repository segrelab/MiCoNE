def updateMeta(Map args) {
    def Map meta = [:]
    meta.id                = args.id ?: ''
    meta.run               = args.run ?: ''
    meta.single_end        = args.single_end ?: ''
    meta.strandedness      = args.strandedness ?: ''
    meta.denoise_cluster   = args.denoise_cluster ?: ''
    meta.chimera_checking  = args.chimera_checking ?: ''
    meta.tax_assignment    = args.tax_assignment ?: ''
    meta.otu_processing    = args.otu_processing ?: ''
    meta.network_inference = args.network_inference ?: ''
    return meta
}

def getHierarchy(String task_process) {
    def hierarchy = task_process.split(":")
    return hierarchy.collect { it.replaceAll("_workflow", "") }
}
