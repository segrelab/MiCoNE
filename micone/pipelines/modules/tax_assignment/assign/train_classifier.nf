// TODO: Move this to workflows
// Step1: Train classifier on reference_sequences and taxonomy_map
if(classifier) {
    Channel
        .fromPath(classifier)
        .tuple { chnl_classifier_artifact }
} else {
    process train_classifier {
        output:
        file('classifier.qza')
        script:
        template 'tax_assignment/assign/train_classifier.sh'
    }
}

