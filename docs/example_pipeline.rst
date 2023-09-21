=====================================
Example pipeline setup and execution
=====================================

.. _common-setup:

Preliminary setup and common instructions
-----------------------------------------

1. Setting up the MiCoNE environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before execution of the ``MiCoNE`` pipeline we need to install the environments:

.. code:: sh

    micone install

.. warning:: This command will take a considerable amount of time (several hours) as MiCoNE will install all the ``conda`` environments

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

First follow the instructions in steps 1-3 in the :ref:`common-setup` section.

Let us assume that you have multiplexed (``run1``, ``run2``, and ``run3``) paired end 16S sequence data stored in the ``<pipeline_dir>/seqs`` folder. To run the pipeline you will need the following:

1. ``forward.fastq.gz``: Forward reads
2. ``reverse.fastq.gz``: Reverse reads
3. ``barcodes.fastq.gz``: Barcodes
4. ``mapping.tsv``: Mapping file
5. ``sample_metadata.tsv``: Sample metadata file

.. warning:: Keep the file names as they are. The pipeline might have issues if the file names are changed.

An example ``sample_sheet.csv`` file will look like this:

+-----+------+--------------------------------------+--------------------------------------+---------------------------------------+----------------------------+------------------------------------+
| id  | run  | forward                              | reverse                              | barcodes                              | mapping                    | sample_metadata                    |
+=====+======+======================================+======================================+=======================================+============================+====================================+
| id1 | run1 | sequences/run1/seqs/forward.fastq.gz | sequences/run1/seqs/reverse.fastq.gz | sequences/run1/seqs/barcodes.fastq.gz | sequences/run1/mapping.tsv | sequences/run1/sample_metadata.tsv |
+-----+------+--------------------------------------+--------------------------------------+---------------------------------------+----------------------------+------------------------------------+
| id2 | run2 | sequences/run2/seqs/forward.fastq.gz | sequences/run2/seqs/reverse.fastq.gz | sequences/run2/seqs/barcodes.fastq.gz | sequences/run2/mapping.tsv | sequences/run2/sample_metadata.tsv |
+-----+------+--------------------------------------+--------------------------------------+---------------------------------------+----------------------------+------------------------------------+
| id3 | run3 | sequences/run3/seqs/forward.fastq.gz | sequences/run3/seqs/reverse.fastq.gz | sequences/run3/seqs/barcodes.fastq.gz | sequences/run3/mapping.tsv | sequences/run3/sample_metadata.tsv |
+-----+------+--------------------------------------+--------------------------------------+---------------------------------------+----------------------------+------------------------------------+

.. note:: These files must follow the ``qiime2`` supported formats. For more information about the supported formats see the `qiime2 documentation <https://docs.qiime2.org/2023.7/tutorials/importing/>`__.


Network inference workflow
---------------------------

Before running this workflow make sure that your OTU tables have taxonomy metadata and sample metadata information.
You must run the workflow from the TA step if they do not.

First follow the instructions in steps 1-3 in the :ref:`common-setup` section.

Let us assume that you have 3 sets of OTU tables (``id1``, ``id2``, and ``id3``) you wish to analyze. To run the pipeline you will need the following:

1. ``otu_table.tsv``: OTU table in ``.tsv`` format
2. ``obs_metadata.tsv``: Taxonomy assignments  in ``.tsv`` format. It must contain the following columns: "Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species". The latter columns can be dropped if you have grouped your taxonomy at a higher level.
3. ``sample_metadata.tsv``: Sample metadata file
4. ``children_map.json``: A file that maps the current taxonomy ids to lower taxonomic level. Can be an empty JSON if you wish to ignore this field.

.. warning:: Keep the file names as they are. The pipeline might have issues if the file names are changed.

An example ``sample_sheet.csv`` file will look like this:

+-----+--------------------------+-----------------------------+--------------------------------+------------------------------+
| id  | otu_table                | obs_metadata                | sample_metadata                | children_map                 |
+=====+==========================+=============================+================================+==============================+
| id1 | inputs/id1/otu_table.tsv | inputs/id1/obs_metadata.tsv | inputs/id1/sample_metadata.tsv | inputs/id1/children_map.json |
+-----+--------------------------+-----------------------------+--------------------------------+------------------------------+
| id2 | inputs/id2/otu_table.tsv | inputs/id2/obs_metadata.tsv | inputs/id2/sample_metadata.tsv | inputs/id2/children_map.json |
+-----+--------------------------+-----------------------------+--------------------------------+------------------------------+
| id3 | inputs/id3/otu_table.tsv | inputs/id3/obs_metadata.tsv | inputs/id3/sample_metadata.tsv | inputs/id3/children_map.json |
+-----+--------------------------+-----------------------------+--------------------------------+------------------------------+


.. note:: Example data can be found `here <https://github.com/segrelab/MiCoNE-synthetic-data/tree/main/data>`__.

