.. highlight:: shell

============
Installation
============


Stable release (only Python package)
------------------------------------

To install the MiCoNE Python package, run this command in your terminal:

.. code-block:: console

    $ pip install MiCoNE

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

.. note:: This does not install the `nextflow`_ related pipeline elements. Those can be installed through anaconda (see below).

From anaconda (complete pipeline)
---------------------------------

This is the preferred way to install the complete MiCoNE pipeline.

First clone the public repository:

.. code-block:: console

   $ git clone git://github.com/segrelab/MiCoNE

Then create a conda environment and install the required packages:

.. code-block:: console

   $ cd MiCoNE
   $ conda env create -n micone -f env.yml


From sources (only Python package)
----------------------------------

The sources for Microbial Interaction Database Pipeline can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/segrelab/MiCoNE

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/segrelab/MiCoNE/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install .


.. _Github repo: https://github.com/segrelab/MiCoNE
.. _tarball: https://github.com/segrelab/MiCoNE/tarball/master
