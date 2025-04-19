
Changelog
=========

1.0.1 (2025-04-18)
~~~~~~~~~~~~~~~~~~~

* **Enhanced Security for Credentials**:
   - Improved encryption for locally stored credentials
   - Added clearer user feedback for credential storage operations

1.0.0 (2025-04-18)
~~~~~~~~~~~~~~~~~~~

* **API Terminology Alignment**: Renamed parameter ``method`` to ``endpoint`` in ``xbrl.query`` to better align with XBRL US API terminology
* **Enhanced Streamlit Interface**:
   - Updated interface to work with the new ``endpoint`` parameter
   - Added support for many additional XBRL endpoints
   - Added field definitions display for each endpoint directly in the interface
* **Enhanced Async Mode**: Improved asynchronous request handling in app.py for better performance with large queries

0.1.0 (2025-04-14)
~~~~~~~~~~~~~~~~~~~

* **New Specialized Methods**: Added specialized methods for all endpoint types (assertion, concept, cube, dimension, document, dts, entity, label, network, relationship) such as ``xbrl.fact`` and ``xbrl.report`` to replace the generic ``query`` method with more specialized, type-safe alternatives
* **Enhanced Type Hints**: Implemented detailed type suggestions for fields, parameters, and sorting options in specialized methods
* **IDE Integration**: Added comprehensive parameter definitions and documentation that appear directly in your IDE
* **Async Support**: Added ``async_mode`` parameter to all specialized methods for parallel execution of large queries


0.0.44 (2025-02-15)
~~~~~~~~~~~~~~~~~~~

* Bug fixes

0.0.44 (2025-02-09)
~~~~~~~~~~~~~~~~~~~

* added an experimental feaute for async requests
* The Parameters and Fields are no longer available in the API
* Bug fixes


0.0.43 (2024-05-08)
~~~~~~~~~~~~~~~~~~~

* fixed and issue with the offset where the query would not return the correct results

0.0.42 (2023-08-05)
~~~~~~~~~~~~~~~~~~~

* Bug fixes
* Improved Browser Interface
* Added new methods to the API for Browser Interface

0.0.41 (2023-08-04)
~~~~~~~~~~~~~~~~~~~

* Bug fixes

0.0.40 (2023-08-03)
~~~~~~~~~~~~~~~~~~~

* Improved Browser Interface
* improved error handling for requests
* Bug fixes

0.0.32 (2023-07-17)
~~~~~~~~~~~~~~~~~~~

* Improved Browser Interface
* Added ``unique`` keyword to ``query`` method
* Bug fixes

0.0.31 (2023-07-14)
~~~~~~~~~~~~~~~~~~~

* fixed dependency issues
* Bug fixes


0.0.3 (2023-07-14)
~~~~~~~~~~~~~~~~~~

* Backward compatibility with Python 3.8 and 3.9
* Bug fixes

0.0.2 (2023-07-12)
~~~~~~~~~~~~~~~~~~


* Bug fixes
* Enhanced error handling
* Improved ``methods`` attributes
* Added the ability to print the query string
* Implemented a feature to handle queries with large limits
* NEW: Introduced a web interface for the API, making it even easier to use


0.0.1 (2023-07-09)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.
