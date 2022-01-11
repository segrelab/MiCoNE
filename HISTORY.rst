=========
Changelog
=========

Unreleased
----------

0.11.1 (2022-01-11)
-------------------

Added
+++++

- ``slim`` parameter added to ``pvalue`` module to allow the user to forgo storage of correlation bootstrap files


0.11.0 (2021-12-16)
-------------------

Fixed
+++++

- ``Network`` class now uses ``name`` to build the lineage of the node object instead of the ``taxid`` field. This prevents inconsistency between OTU tables and Networks of the same level

0.10.4 (2021-12-04)
-------------------

Fixed
+++++
- ``NetworkGroup`` methods that return ``NetworkGroup`` objects now make use of the ``id_field`` parameter

0.10.3 (2021-12-03)
-------------------

Fixed
+++++
- ``Network.get_adjacency_table`` now retrieves ids correctly
- ``simple_voting`` consensus method now takes sign of the edge into account
- ``propr`` modules now assigns correlation file name similar to other modules
- Fixed bug in ``mldm`` when sample metadata is a single column


0.10.2 (2021-12-01)
-------------------

Added
+++++
- ``NetworkGroup`` object now supports the ``id_field`` parameter in constructor. Allowing combination of networks on fields other than ``taxid``
- ``merge_pvalues`` and ``create_consensus`` now support the ``id_field`` parameter

Fixed
+++++
- ``remove_bimera`` module now uses external ``biom`` command to construct OTU table


0.10.0 (2021-11-23)
-------------------

Added
+++++
- ``HARMONIES`` network inference method
- ``COZINE`` network inference method
- ``SPRING`` network inference method
- Pipeline output checking functionality - ``micone validate-results``
- Parametrize some of the pipeline settings

Changed
+++++++
- ``mldm`` runtime limit

Fixed
+++++
- ``normalize`` module is turned off by default
- Many bugs in the pipeline


0.9.0 (2021-10-30)
------------------

- Major overhaul of the pipeline to enable workflow to be implemented purely in ``nextflow``
- As of writing the pipeline modules in the package do not work. Currently, to run the pipeline one needs to copy the contents of the ``pipelines`` folder to the destination, update the ``nextflow.config`` and run the pipeline.


0.7.0 (2021-03-04)
------------------

Added
+++++
- ``NetworkGroup`` method now supports an ``__add__`` method
- ``FlashWeave.jl`` for network inference
- ``propr`` for network inference
- ``make_network`` module split into ``make_network_with_pvalue`` and ``make_network_wo_pvalue``

Changed
+++++++
- ``MAGMA`` network inference was removed because it has not been updated
- ``network_inference.direct`` modules will not support bootstrapping and pvalues in the future

Fixed
+++++
- Threading error due to database connection with ``NCBITaxa``


0.6.0 (2021-02-04)
------------------

Stable update! All the tests pass and the pipelines work as expected

0.5.0 (2019-01-02)
------------------

Major update! Implemeting the core pipeline functionality

Added
+++++
- ``NetworkGroup`` class represents a group of networks
- ``Config`` class to extract, process and store pipeline settings
- ``Command`` class is a wrapper for running subprocesses
- ``Process`` class for executing a pipeline process
- ``Pipeline`` class defines the pipeline and methods to run the pipeline
- ``Environments`` class that creates, lists and loads conda environments
- Logging functionality
- CLI interface for micone


0.4.2 (2018-10-08)
------------------

Added
+++++
-  ``dict`` property to ``Params``class
- ``verify_io`` method to ``Params``class
- ``update_location`` method to ``Params`` class
- ``get`` method to ``Params`` class
- ``Params`` class to config namespace

Changed
+++++++
- ``ScriptTemplate.render`` now uses a default value of '{}' for ``template_data`` parameter
- Rename ``template_renderer.py`` to ``template.py``

Fixed
+++++
- ``Input.location`` and ``Output.location`` are now of type ``pathlib.Path``


0.4.1 (2018-10-08)
------------------

Changed
+++++++
- Renamed ``ExternalProcessParamsSet`` class to ``ExternalParamsSet`` class
- Renamed ``InternalProcessParamsSet`` class to ``InternalParamsSet`` class
- Renamed ``ProcessParamsSet`` class to ``ParamsSet`` class
- Renamed ``ProcessParams`` class to ``Params`` class
- Updated dependencies - ``biom-format``, ``dask``, ``toml``

Fixed
+++++
- Flake8 errors


0.4.0 (2018-10-06)
------------------

Pipeline settings parser and template render have been implemented.

Added
+++++
- ``Config`` - A class to store all the pipeline configuration
- ``InternalProcessParamsSet`` and ``ExternalProcessParamsSet`` for loading internal and external process params
- ``ProcessParams`` - A class to process and store parameters of pipeline processes
- ``DataTypes`` - A class to process and store datatypes
- ``external.toml`` to store the list of external pipeline processes
- ``internal.toml`` to store the list of internal pipeline processes
- ``datatypes.toml`` to store the list of pipeline supported datatypes
- ``ScriptTemplate`` - A class for templating nextflow scripts
- ``ConfigTemplate`` - A class for templating nextflow config files

Changed
+++++++
- Simplified the internal and external settings files to contain minimum information
- ``correlation_table`` datatype renamed to ``interaction_table``
- Modularize the default settings into separate files - datatypes.toml, internal.toml and external.toml

Fixed
+++++
- Filter ``DeprecationWarning`` and ``PendingDeprecationWarning`` in pytest configuration


0.3.0 (2018-08-28)
------------------

Added
+++++
- ``Network.__repr__`` - object representation for the ``Network`` class
- ``Network.json`` method to convert network to a ``JSON`` string
- ``Network.write`` method to write network to a json file
- ``Network.graph`` property to return the ``nx.Graph`` representation of the network
- ``Network.load_json`` classmethod to load network from json file
- ``ElistType`` - Schema for edgelist
- ``NETWORK_CONVERTERS`` to convert networks to and from various formats
- ``Network.load_elist`` classmethod to load network from edge list file

Changed
+++++++
- Type of "computational_metadata" to ``DictType(UnionType((StringType, FloatType)))``
- "computational_metadata" now includes 'interaction_threshold', 'pvalue_threshold' and 'pvalue_correction'
- "abundance" is now not a required field for a node
- Refactor network models into 'network_schema' module

Fixed
+++++
- Type annotation for link_set in ``Network._create_network``
- Test data is now from the same source (all FMT datasets are from deblur)
- Prevent re-correction of pvalues when loading from json or elist file


0.2.4 (2018-08-23)
------------------

Added
+++++
- ``travis-sphinx`` to automatically deploy 'sphinx' docs to ``gh-pages``
- Custom ``JsonEncoder`` class to encode json network data

Changed
+++++++
- sphix theme to ``sphinx_rtd_theme``

Fixed
+++++
- ``Network._create_network`` now removes complementary links in undirected networks


0.2.3 (2018-08-23)
------------------

Added
+++++
- ``Network.load_data`` to create networks from files
- 'computational_metadata' to test data

Changed
+++++++
- Add 'computational_metadata' to 'correlation_data' fixtures and tests


0.2.2 (2018-08-22)
------------------

Added
+++++
- ``Lineage.taxid`` property and tests
- ``NodesModel``, ``LinksModel`` and ``NetworkmetadataModel``
- ``Network`` class to read, write and manipulate networks and tests
- 'network_files' and 'correlation_data' fixtures for tests

Changed
+++++++
- Keys for ``MetadataType`` class
- Incorporate new keys in 'metadata.json' in test data
- Changed ``MetadataType`` from 'BaseType' to 'Model'
- Renamed ``MetadataType`` -> ``MetadataModel``


0.2.1 (2018-08-17)
------------------

Added
+++++
- ``ChildrenmapType`` class and tests

Changed
+++++++
- Network metadata files for tests


0.2.0 (2018-08-17)
------------------

Added
+++++
- ``Lineage`` class
- ``Otu`` class
- ``OtuValidator`` class
- ``OtuSchema`` class
- ``taxmetadata_converter`` functions to convert to and from ``qiime1`` and ``qiime2`` taxonomy formats


0.1.0 (2018-06-30)
------------------

Added
+++++
- First release and initial commits


.. _[0.2.3]: https://github.com/dileep-kishore/micone/compare/v0.2.2...v0.2.3
.. _[0.2.2]: https://github.com/dileep-kishore/micone/compare/v0.2.1...v0.2.2
.. _[0.2.1]: https://github.com/dileep-kishore/micone/compare/v0.2.0...v0.2.1
.. _[0.2.0]: https://github.com/dileep-kishore/micone/compare/v0.1.0...v0.2.0

