=====================================
Example pipeline setup and execution
=====================================

Preliminary setup
-----------------

Before execution of the ``MiCoNE`` pipeline we need to install the environments:

.. code:: sh

    micone install

.. note:: This command will take a considerable amount of time (several hours) as MiCoNE will install all the ``conda`` environments

If you wish to install only a subset of the environments, you can specify the environments to install using the ``-e`` option:

.. code:: sh

    micone install -e <env1>

The list of supported environments can be found in the :ref:`supported_environments` section.

- micone-cozine
- micone-dada2
- micone-flashweave
- micone-harmonies
- micone-mldm
- micone-propr
- micone-qiime2
- micone-sparcc
- micone-spieceasi
- micone-spring


Network inference workflow
---------------------------

Install the micone conda environment.
Run micone install -e <env> to install all the sub-environments that you need
Run micone init -w full -o <pipeline_dir> to set up the pipeline template. This creates a nextflow workflow template for the full pipeline.
Replace the existing main.nf,nextflow.config and samplesheet.csv files with the ones that I have attached to this email. You will also need to modify some of the files in the pipeline_dir according to these instructions: https://github.com/segrelab/MiCoNE/tree/master#configuration-and-the-pipeline-template
Finally, you can run the pipeline using bash run.sh or qsub run.sh (if running on the cluster)
Note that this workflow is only valid if your biom files already have taxonomy labels assigned. You must run the workflow from the TA step if they do not. Let me know if this is the case.

Other useful references:
All the supported configuration options in table format: https://github.com/segrelab/MiCoNE-pipeline-paper/tree/master/tables/csv
Actual default configuration files used during program execution (copied over when you use the micone init -w full -o <pipeline_dir> command: https://github.com/segrelab/MiCoNE/tree/master/micone/pipelines/configs
Here are example configuration files that were used in the analysis performed for the paper: https://github.com/segrelab/MiCoNE-pipeline-paper/tree/master/scripts/runs

