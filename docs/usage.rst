=====
Usage
=====

The ``mindpipe`` pipeline comes with an easy to use CLI. To get a list of supported subcommands you can type:

.. code-block:: console

    mindpipe --help

Supported subcommands:
1. init - Creates ``conda`` environments for various pipeline processes
2. run - The main subcommand that runs the pipeline
3. clean - Cleans temporary data, log files and other extraneous files


Running the pipeline
--------------------

.. code-block:: console

    mindpipe run -p local -c run.toml -m 4

This runs the pipeline in the ``local`` machine using ``run.toml`` for the pipeline configuration and with a maximum of ``4`` processes in parallel at a time.
