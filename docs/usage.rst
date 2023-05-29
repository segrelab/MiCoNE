=====
Usage
=====

Workflow
--------

.. figure:: images/pipeline.png
   :alt: pipeline

   pipeline

It supports the conversion of raw 16S sequence data into co-occurrence
networks. Each process in the pipeline supports alternate tools for
performing the same task, users can use the configuration file to change
these values.

Usage
-----

The ``MiCoNE`` pipelines comes with an easy-to-use CLI. To get a list of
subcommands you can type:

.. code:: sh

   micone --help

Supported subcommands:

1. ``install`` - Initializes the package and environments (creates
   ``conda`` environments for various pipeline processes)
2. ``init`` - Initialize the nextflow templates for the micone workflow
3. ``clean`` - Cleans files from a pipeline run (cleans temporary data,
   log files and other extraneous files)
4. ``validate-results`` - Check the results of the pipeline execution

Initializing the environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to run the pipeline various ``conda`` environments must first
be installed on the system. Use the following comand to initialize all
the environments:

.. code:: sh

   micone install

Or to initialize a particular environment use:

.. code:: sh

   micone install -e "micone-qiime2"

The list of supported environments are: - micone-cozine - micone-dada2 -
micone-flashweave - micone-harmonies - micone-mldm - micone-propr -
micone-qiime2 - micone-sparcc - micone-spieceasi - micone-spring

Initializing the pipeline template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To initialize the full pipeline (from raw 16S sequencing reads to
co-occurrence networks):

.. code:: sh

   micone init -w <workflow> -o <path/to/folder>

Other supported pipeline templates are (work in progress): - full - ni -
op_ni - ta_op_ni

To run the pipeline, update the relevant config files (see next
section), activate the ``micone`` environment and run the ``run.sh``
script that was copied to the directory:

.. code:: sh

   bash run.sh

This runs the pipeline locally using the config options specified.

To run the pipeline on an SGE enabled cluster, add the relevant
project/resource allocation flags to the ``run.sh`` script and run as:

.. code:: sh

   qsub run.sh

Configuration and the pipeline template
---------------------------------------

The pipeline template for the micone “workflow” (see previous section
for list of supported options) is copied to the desired folder after
running ``micone init -w <workflow>``. The template folder contains the
following folders and files:

-  nf_micone: Folder contatining the ``micone`` default configs, data,
   functions, and modules
-  templates: Folder containing the templates (scripts) that are
   executed during the pipeline run
-  main.nf: The pipeline “workflow” defined in the ``nextflow`` DSL 2
   specification
-  nextflow.config: The configuration for the pipeline. This file needs
   to be modified in order to change any configuration options for the
   pipeline run
-  metadata.json: Contains the basic metadata that describes the dataset
   that is to be processed. Should be updated accordingly before
   pipeline execution
-  samplesheet.csv: The file that contains the locations of the input
   data necessary for the pipeline run. Should be updated accordingly
   before pipeline execution
-  run.sh: The ``bash`` script that contains commands used to execute
   the ``nextflow`` pipeline

The folder ``nf_micone/configs`` contains the default configs for all
the ``micone`` pipeline workflows. These options can also be viewed in
tabular format in the
`documentation <https://micone.readthedocs.io/en/latest/usage.html#configuring-the-pipeline>`__.

For example, to change the tool used for OTU assignment to ``dada2`` and
``deblur``, you can add the following to ``nextflow.config``:

.. code:: groovy

   // ... config initialization
   params {
          // ... other config options
          denoise_cluster {
           otu_assignment {
               selection = ['dada2', 'deblur']
           }
       }
   }

Example configuration files used for the analyses in the manuscript can
be found
`here <https://github.com/segrelab/MiCoNE-pipeline-paper/tree/master/scripts/runs>`__.

Visualization of results (coming soon)
--------------------------------------

The results of the pipeline execution can be visualized using the
scripts in the `manuscript
repo <https://github.com/segrelab/MiCoNE-pipeline-paper/tree/master/scripts>`__


Configuring the pipeline
------------------------

The parameters for the pipeline execution are in the `micone/pipelines/configs/*.config`_ in the MiCoNE GitHub repository. These can be configured using the `nextflow.config`_ file.

The following tables contain the list of default parameters for each step of the pipeline:

Sequence Processing (SP)
++++++++++++++++++++++++

+------------+---------+-------------------+----------------+----------+
| Step       | Task    | Tool              | Parameter      | Value    |
+============+=========+===================+================+==========+
| Sequence   | Demulti\ | demultiplexin\     | barcode_column | barcode- |
| Processing | plexing | g_illumina_single |                | sequence |
+------------+---------+-------------------+----------------+----------+
| Sequence   | Demulti\ | demultiplexin\     | rev\            | false    |
| Processing | plexing | g_illumina_single | _comp_barcodes |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | Demulti\ | demultiplexin\     | rev_comp_ma\    | false    |
| Processing | plexing | g_illumina_single | pping_barcodes |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | Demulti\ | demultiplexin\     | barcode_column | barcode- |
| Processing | plexing | g_illumina_paired |                | sequence |
+------------+---------+-------------------+----------------+----------+
| Sequence   | Demulti\ | demultiplexin\     | rev\            | false    |
| Processing | plexing | g_illumina_paired | _comp_barcodes |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | Demulti\ | demultiplexin\     | rev_comp_ma\    | false    |
| Processing | plexing | g_illumina_paired | pping_barcodes |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | T\       | export_vis\        | seq_samplesize | 10000    |
| Processing | rimming | ualization_single |                |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | T\       | export_vis\        | seq_samplesize | 10000    |
| Processing | rimming | ualization_paired |                |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | T\       | trimming_single   | ncpus          | 1        |
| Processing | rimming |                   |                |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | T\       | trimming_single   | max_ee         | 2        |
| Processing | rimming |                   |                |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | T\       | trimming_single   | trunc_q        | 2        |
| Processing | rimming |                   |                |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | T\       | trimming_paired   | ncpus          | 1        |
| Processing | rimming |                   |                |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | T\       | trimming_paired   | max_ee         | 2        |
| Processing | rimming |                   |                |          |
+------------+---------+-------------------+----------------+----------+
| Sequence   | T\       | trimming_paired   | trunc_q        | 2        |
| Processing | rimming |                   |                |          |
+------------+---------+-------------------+----------------+----------+

Denoising and Clustering (DC)
+++++++++++++++++++++++++++++

+-----------------+-----------------+---------------------+-----------+
| Task            | Tool            | Parameter           | Value     |
+=================+=================+=====================+===========+
| OTU assignment  | Closed          | ncpus               | 1         |
|                 | reference       |                     |           |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Closed          | percent_identity    | 0.97      |
|                 | reference       |                     |           |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Closed          | strand              | “plus”    |
|                 | reference       |                     |           |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Closed          | reference_sequences | “gg_97”   |
|                 | reference       |                     |           |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Open reference  | ncpus               | 1         |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Open reference  | percent_identity    | 0.97      |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Open reference  | strand              | “plus”    |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Open reference  | reference_sequences | “gg_97”   |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | De novo         | ncpus               | 1         |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | De novo         | percent_identity    | 0.97      |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Dada2           | ncpus               | 1         |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Dada2           | big_data            | “FALSE”   |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Deblur          | ncpus               | 1         |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Deblur          | min_reads           | 2         |
+-----------------+-----------------+---------------------+-----------+
| OTU assignment  | Deblur          | min_size            | 2         |
+-----------------+-----------------+---------------------+-----------+
| Chimera         | Remove bimera   | ncpus               | 1         |
| checking        |                 |                     |           |
+-----------------+-----------------+---------------------+-----------+
| Chimera         | Remove bimera   | chimera_method      | “c\       |
| checking        |                 |                     | onsensus” |
+-----------------+-----------------+---------------------+-----------+

Taxonomy Assignment (TA)
++++++++++++++++++++++++

====== =========== ============= ====================
Task   Tool        Parameter     Value
====== =========== ============= ====================
Assign Naive Bayes classifer     “gg_13_8_99_515_806”
Assign Naive Bayes confidence    0.7
Assign Naive Bayes ncpus         1
Assign BLAST       references    “ncbi_refseq”
Assign BLAST       max_accepts   10
Assign BLAST       perc_identity 0.8
Assign BLAST       evalue        0.001
Assign BLAST       min_consensus 0.51
====== =========== ============= ====================

OTU Processing (OP)
+++++++++++++++++++

+-----+-----------+-----------+---------------------------------------+
| Task   | Tool      | Parameter | Value                                 |
+=====+===========+===========+=======================================+
| Tra\ | Fork      | axis      | “sample”                              |
| nsf |           |           |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Fork      | column    | “”                                    |
| nsf |           |           |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Normalize | axis      | “None”                                |
| nsf | & Filter  |           |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Normalize | co\        | 500                                   |
| nsf | & Filter  | unt_thres |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Normalize | prevale\   | 0.05                                  |
| nsf | & Filter  | nce_thres |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Normalize | obs\       | 100                                   |
| nsf | & Filter  | sum_thres |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Normalize | rm_s\      | [true, false]                         |
| nsf | & Filter  | parse_obs |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Normalize | rm_spars\  | true                                  |
| nsf | & Filter  | e_samples |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Normalize | abunda\    | 0.01                                  |
| nsf | & Filter  | nce_thres |                                       |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+
| Tra\ | Group     | t\         | [‘Phylum’, ‘Class’, ‘Order’,          |
| nsf |           | ax_levels | ‘Family’, ‘Genus’, ‘Species’]         |
| orm |           |           |                                       |
+-----+-----------+-----------+---------------------------------------+

Network Inference (NI)
++++++++++++++++++++++

+---------+--------------------------+-------------------+----------+
| Task    | Tool                     | Parameter         | Value    |
+=========+==========================+===================+==========+
| Bo\      | Resample                 | bootstraps        | 1000     |
| otstrap |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Bo\      | Resample                 | ncpus             | 1        |
| otstrap |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Bo\      | Pvalue                   | slim              | false    |
| otstrap |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Bo\      | Pvalue                   | ncpus             | 1        |
| otstrap |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Corr\    | sparcc                   | ncpus             | 1        |
| elation |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Corr\    | sparcc                   | iterations        | 50       |
| elation |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Corr\    | pearson                  | ncpus             | 1        |
| elation |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Corr\    | spearman                 | ncpus             | 1        |
| elation |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Corr\    | propr                    | ncpus             | 1        |
| elation |                          |                   |          |
+---------+--------------------------+-------------------+----------+
| Direct  | spieceasi                | method            | “mb”     |
+---------+--------------------------+-------------------+----------+
| Direct  | spieceasi                | ncpus             | 1        |
+---------+--------------------------+-------------------+----------+
| Direct  | spieceasi                | nreps             | 50       |
+---------+--------------------------+-------------------+----------+
| Direct  | spieceasi                | nlambda           | 20       |
+---------+--------------------------+-------------------+----------+
| Direct  | spieceasi                | lambda_min_ratio  | 1e-2     |
+---------+--------------------------+-------------------+----------+
| Direct  | flashweave               | ncpus             | 1        |
+---------+--------------------------+-------------------+----------+
| Direct  | flashweave               | sensitive         | “true”   |
+---------+--------------------------+-------------------+----------+
| Direct  | flashweave               | heterogeneous     | “false”  |
+---------+--------------------------+-------------------+----------+
| Direct  | flashweave               | fdr_correction    | “true”   |
+---------+--------------------------+-------------------+----------+
| Direct  | mldm                     | Z_mean            | 1        |
+---------+--------------------------+-------------------+----------+
| Direct  | mldm                     | max_iteration     | 1500     |
+---------+--------------------------+-------------------+----------+
| Direct  | cozine                   | lambda_min_ratio  | 0.1      |
+---------+--------------------------+-------------------+----------+
| Direct  | harmonies                | iterations        | 10000    |
+---------+--------------------------+-------------------+----------+
| Direct  | harmonies                | sparsity_cutoff   | 0.5      |
+---------+--------------------------+-------------------+----------+
| Direct  | spring                   | ncpus             | 1        |
+---------+--------------------------+-------------------+----------+
| Direct  | spring                   | nlambda           | 20       |
+---------+--------------------------+-------------------+----------+
| Direct  | spring                   | lambda_min_ratio  | 0.01     |
+---------+--------------------------+-------------------+----------+
| Network | Make network with        | inte\              | 0.3      |
|         | pvalues                  | raction_threshold |          |
+---------+--------------------------+-------------------+----------+
| Network | Make network with        | pvalue_threshold  | 0.05     |
|         | pvalues                  |                   |          |
+---------+--------------------------+-------------------+----------+
| Network | Make network with        | metadata_file     | “”       |
|         | pvalues                  |                   |          |
+---------+--------------------------+-------------------+----------+
| Network | Make network without     | inte\              | 0.3      |
|         | pvalues                  | raction_threshold |          |
+---------+--------------------------+-------------------+----------+
| Network | Make network without     | metadata_file     | “”       |
|         | pvalues                  |                   |          |
+---------+--------------------------+-------------------+----------+
| Network | Merge pvalues            | id_field          | “taxid”  |
+---------+--------------------------+-------------------+----------+
| Network | Create consensus         | method            | “sca     |
|         |                          |                   | led_sum” |
+---------+--------------------------+-------------------+----------+
| Network | Create consensus         | parameter         | 0.3      |
+---------+--------------------------+-------------------+----------+
| Network | Create consensus         | pvalue_filter     | “true”   |
+---------+--------------------------+-------------------+----------+
| Network | Create consensus         | i\                 | “true”   |
|         |                          | nteraction_filter |          |
+---------+--------------------------+-------------------+----------+
| Network | Create consensus         | id_field          | “taxid”  |
+---------+--------------------------+-------------------+----------+
