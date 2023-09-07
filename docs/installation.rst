.. highlight:: shell

============
Installation
============

From anaconda (complete pipeline)
---------------------------------

This is the preferred way to install the complete MiCoNE pipeline.

First clone the public repository:

.. code:: sh

   git clone git://github.com/segrelab/MiCoNE

Then create a conda environment and install the required packages:

.. code:: sh

   cd MiCoNE
   mamba env create -n micone -f env.yml

Or you can directly install from the repository:

.. code:: sh

   mamba env create -n micone -f https://raw.githubusercontent.com/segrelab/MiCoNE/master/env.yml

..

   NOTE: 1. MiCoNE requires the ``mamba`` package manager, otherwise
   ``micone init`` will not work. 2. Direct installation via anaconda
   cloud will be available soon.


From pip (only Python package)
------------------------------------

To install the MiCoNE Python package, run this command in your terminal:

.. code:: sh

    pip install MiCoNE

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

.. note:: This does not install the ``nextflow`` related pipeline elements, and does not provide the functionality to execute pipelines. Those can be installed through anaconda (see above).


From sources (only Python package)
----------------------------------

The sources for Microbial Interaction Database Pipeline can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code:: sh

    git clone git://github.com/segrelab/MiCoNE

Or download the `tarball`_:

.. code:: sh

    curl  -OL https://github.com/segrelab/MiCoNE/tarball/master

Once you have a copy of the source, you can install it with:

.. code:: sh

    pip install .


.. _Github repo: https://github.com/segrelab/MiCoNE
.. _tarball: https://github.com/segrelab/MiCoNE/tarball/master
