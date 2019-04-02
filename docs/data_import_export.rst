======================
Data Import and Export
======================

1. Importing a network from a Table
-----------------------------------

If you have an interaction matrix stored in a ``tsv`` or ``csv`` format, you can load it into a ``Network`` object. Additionally we require:
    1. ``obsmeta_file`` - A ``csv`` file containing the taxonomy information for the microbes that are a part of the matrix
    2.  ``meta_file`` - A ``json`` file containing the experimental metadata for the network
    3. ``cmeta_file`` - A ``json`` file containing the details about the computational processing done on the data

.. code-block:: python

    from mindpipe import Network, NetworkGroup
    network = Network.load_data(
        interaction_file,
        meta_file,
        cmeta_file,
        obsmeta_file,
    )
    network_group = NetworkGroup([network])

Additionally, you can specify the matrix of pvalues and thesholds if any to be applied to the data

.. note::

    1. The indices of the ``interaction_file`` and ``obsmeta_file`` must match
    2. The order of indicies of ``interaction_file`` and ``pvalue_file`` must match

2. Importing a network from an edge list
----------------------------------------

If you have interaction data stored in the form of an edge list

.. code-block:: python

    from mindpipe import Network. NetworkGroup
    network = Network.load_elist(
        elist_file,
        meta_file,
        cmeta_file,
        obsmeta_file,
    )
    network_group = NetworkGroup([network])

.. note::

    1. The headers of the ``elist_file`` must contain "source", "target", "weight"


3. Exporting your Network object into JSON file
-----------------------------------------------

.. code-block:: python

    network_group.write("network.json", pvalue_filter=True, interaction_filter=False)

This ``JSON`` file is compatible with the ``MIND`` database and can be uploaded and visualized directly on the website.
