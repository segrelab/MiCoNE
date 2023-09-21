=====================================
Example pipeline setup and execution
=====================================

Preliminary setup and common instructions
-----------------------------------------

1. Setting up the MiCoNE environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before execution of the ``MiCoNE`` pipeline we need to install the environments:

.. code:: sh

    micone install

.. note:: This command will take a considerable amount of time (several hours) as MiCoNE will install all the ``conda`` environments

If you wish to install only a subset of the environments, you can specify the environments to install using the ``-e`` option:

.. code:: sh

    micone install -e <env1>

The list of supported environments can be found in the :ref:`supported-environments` section.


2. Initializing the pipeline template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set up the ``nextflow`` workflow template for the desired workflow, you can use the ``micone init`` command:

.. code:: sh

    micone init -w <workflow> -o <pipeline_dir>

This initializes the ``workflow`` in the ``pipeline_dir`` folder. For a list of supported workflow see the :ref:`supported-workflows` section.

Detailed information about the various files in the pipeline folder can be found in the :ref:`pipeline-configuration` section.


3. Downloading data and setting up the pipeline template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download the data directory from `here <https://zenodo.org/record/7051556/files/data.zip?download=1>`__ and put it under ``<pipeline_dir>/nf_micone/data``.
2. Update the ``sample_sheet.csv`` and ``metadata.json`` files in the base ``<pipeline_dir>`` directory to reflect the samples and metadata of the data you wish to analyze.
3. Update the ``nextflow.config`` file if you wish to make any changes to the default configuration. The default configuration files can be found `here <https://github.com/segrelab/MiCoNE/tree/master/micone/pipelines/configs>`__ and the supported configuration options can be found in the tables in the :ref:`pipeline-configuration` section.

.. note:: Example configurations used for the manuscript can be found in the ``scripts/runs`` folder of the `MiCoNE-pipeline-paper <https://github.com/segrelab/MiCoNE-pipeline-paper/tree/master/scripts/runs>`__ repository.


4. Run the pipeline
~~~~~~~~~~~~~~~~~~~~

To run the pipeline, you can use the ``run.sh`` script in the ``<pipeline_dir>``:

.. code:: sh

    conda activate micone

    # To run the code locally
    bash run.sh

    # To run the code on the cluster using the scheduler
    qsub run.sh

Full pipeline workflow
----------------------

Network inference workflow
---------------------------

Note that this workflow is only valid if your biom files already have taxonomy labels assigned. You must run the workflow from the TA step if they do not.

