def get_samplesheet_paths(LinkedHashMap row) {
    def meta = [:]
    meta.id           = row.sample
    meta.single_end   = row.single_end.toBoolean()
    meta.strandedness = row.strandedness
    return meta
}

def getHierarchy(String task_process) {
    def hierarchy = task_process.split(":")
    return hierarchy.collect { it.replaceAll("_workflow", "") }
}
