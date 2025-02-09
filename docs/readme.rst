======================
XBRL-US Python Library
======================

About
=====

The XBRL US Python Wrapper is a powerful tool for interacting with the XBRL US API,
providing seamless integration of XBRL data into Python applications.
This wrapper simplifies the process of retrieving and analyzing financial data in XBRL format,
enabling users to access a wide range of financial information for companies registered with the U.S.
Securities and Exchange Commission (SEC).

It's important to note that while the XBRL US Python Wrapper is free and distributed under the permissive MIT license,
the usage of the underlying XBRL US API is subject to the policies and terms defined by XBRL US.
These policies govern the access, usage, and restrictions imposed on the API data and services.
Users of the XBRL US Python Wrapper should review and comply with the XBRL US policies to ensure appropriate
usage of the API and adherence to any applicable licensing terms.

.. important::

    Any and all use of the XBRL APIs to return
    data from the XBRL US Database of Public Filings is in explicit consent and
    agreement with the `XBRL API Terms of Agreement <https://xbrl.us/home/about/legal/xbrl-api-clientid/>`_.

.. note::
    If you are utilizing the XBRL US Python Wrapper for research purposes, we kindly request that you cite the following paper:

    [FILL: Insert Paper Title]

    [FILL: Authors]

    [FILL: Publication Details]


Tutorial ✏️📖📚
================

This tutorial will guide you through using the XBRL-US Python library to interact with the XBRL API.
The XBRL-US library provides a convenient way to query and retrieve financial data from the XBRL API using Python.

1. Prerequisites
~~~~~~~~~~~~~~~~

Before you begin, ensure you have the following:

* **Python installed on your system**.
  The XBRL-US library supports Python 3.8 and above.
* **XBRL-US API credentials**.
  You can obtain your credentials by registering for a
  free XBRL-US account at https://xbrl.us/home/use/xbrl-api/.
* **XBRL-US OAuth2 Access**.
  You can obtain your client ID and client secret by registering for a
  filling the request form at https://xbrl.us/home/use/xbrl-api/access-token/.

You can install this package using pip:

.. list-table::
    :widths: 30 70
    :stub-columns: 1

    * - Command Line
      - .. code-block:: bash

            pip install xbrl-us

    * - Jupyter Notebook
      - .. code-block:: bash

            !pip install xbrl-us

If ``!`` does not work in Jupyter Notebook, use ``%`` instead.

.. caution::

        The XBRL US Python Wrapper is currently in beta and is subject to change.
        We welcome your feedback and suggestions for improvement.
        Please submit any issues or feature requests to
        the `GitHub repository <https://github.com/hamid-vakilzadeh/python-xbrl-us/issues>`_.


**Documentation**

For detailed information about the XBRL-US Python
library, you can refer to the documentation at https://python-xbrl-us.readthedocs.io/en/latest/.

**Official Documentation**

For more information about the XBRL API and its endpoints, refer to the original API documentation at https://xbrlus.github.io/xbrl-api.


2. Choose Your Preferred Approach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two distinct ways to use the XBRL-US Python package:

* **Code-Based Approach**: Import the XBRL-US Python package directly into your Python
  environment for in-depth, custom analysis (see :ref:`Code-Based Approach <code-based approach>`)

* **Browser Interface**: For a no-code experience, navigate to the :ref:`Browser Interface section <browser interface>`.
  This interface allows for easy exploration and analysis of XBRL data directly in your web
  browser.

.. _code-based approach:

2.1. Code-Based Approach
~~~~~~~~~~~~~~~~~~~~~~~~

Import the XBRL Library
-------------------------------

To start using the XBRL-US library,
you need to import it into your Python script:

.. code-block:: python

    from xbrl_us import XBRL

Create an Instance of XBRL Class
----------------------------------------

Next, you need to create an instance of the ``XBRL`` class,
providing your authentication credentials
(client ID, client secret, username, and password) as parameters:

.. code-block:: python

    xbrl = XBRL(
    client_id='Your client id',
    client_secret='Your client secret',
    username='Your username',
    password='Your password'
    )

Make sure to replace ``Your client id``,
``Your client secret``, ``Your username``, and
``Your password`` with your actual credentials.

Query the XBRL API
------------------

The XBRL-US library provides a query method to search
for data from the XBRL API. You can specify various
parameters and fields to filter and retrieve the
desired data.

Here's an example of using the query method to search
for specific financial facts:

.. code-block:: python

    response = xbrl.query(
        method='fact search',
        parameters={
            "concept.local-name": [
                'OperatingIncomeLoss',
                'GrossProfit',
                'OperatingExpenses',
                'OtherOperatingIncomeExpenseNet'
            ],
            "period.fiscal-year": [2009, 2010],
            "report.sic-code": range(2800, 2899)
        },
        fields=[
            'report.accession',
            'period.fiscal-year',
            'period.end',
            'period.fiscal-period',
            'fact.ultimus',
            'unit',
            'concept.local-name',
            'fact.value',
            'fact.id',
            'entity.id',
            'entity.cik',
            'entity.name',
            'report.sic-code',
        ],
        limit=100,
        as_dataframe=True
    )

In this example, we are searching for facts related
to specific concepts, fiscal years, and SIC codes.
We are also specifying the fields we want to retrieve
in the response. The ``limit`` parameter restricts the
number of facts returned to 100, and ``as_dataframe=True``
ensures the response is returned as a ``Pandas DataFrame``.

Alternatively, you can use the ``Parameters`` and ``Fields``
classes provided by the library to make the query more
readable, less prone to errors, and easier to maintain:

.. code-block:: python

    from xbrl_us.utils import Parameters, Fields

    response = xbrl.query(
        method='fact search',
        parameters=Parameters(
            concept_local_name=[
                'OperatingIncomeLoss',
                'GrossProfit',
                'OperatingExpenses',
                'OtherOperatingIncomeExpenseNet'
            ],
            period_fiscal_year=[2009, 2010],
            report_sic_code=range(2800, 2899)
        ),
        fields=[
            Fields.REPORT_ACCESSION,
            Fields.PERIOD_FISCAL_YEAR,
            Fields.PERIOD_END,
            Fields.PERIOD_FISCAL_PERIOD,
            Fields.FACT_ULTIMUS,
            Fields.UNIT,
            Fields.CONCEPT_LOCAL_NAME,
            Fields.FACT_VALUE,
            Fields.FACT_ID,
            Fields.ENTITY_ID,
            Fields.ENTITY_CIK,
            Fields.ENTITY_NAME,
            Fields.REPORT_SIC_CODE,
        ],
        limit=100,
        as_dataframe=True
    )


This alternative approach also allows you to
take advantage of the autocomplete feature of your IDE to
easily find the parameters and fields.

Perform Additional Queries
----------------------------------

You can use the same query method to call other API
endpoints by changing the method parameter and
providing the relevant parameters and fields.

Here's an example of using the query method to
search for a specific fact by its ID:

.. code-block:: python

    response = xbrl.query(
    method='fact id',
    parameters={'fact.id': 123},
    fields=[
        'report.accession',
        'period.fiscal-year',
        'period.end',
        'period.fiscal-period',
        'fact.ultimus',
        'unit',
        'concept.local-name',
        'fact.value',
        'fact.id',
        'entity.id',
        'entity.cik',
        'entity.name',
        'report.sic-code',
    ],
    as_dataframe=False
    )

Congratulations! You have learned how to use the XBRL-US Python library to interact with the XBRL API.
In this example you will receive the data in json format as the ``as_dataframe`` parameter is set to ``False``.

.. _browser interface:

2.2 Browser Interface 🖥️
~~~~~~~~~~~~~~~~~~~~~~~~

This feature is designed to make our package even more user-friendly, allowing users to interact and work with XBRL data
directly through a graphical interface, in addition to the existing code-based methods.

The browser interface streamlines data visualization, simplifies navigation, and enhances user interactions.
With this intuitive, user-friendly interface, you can easily explore, interpret, and analyze XBRL data in real-time,
right from your web browser.

Key Features:

* Create Real-time queries right in your browser
* Intuitive navigation and search features
* Filtering and sorting options
* Seamless integration with the existing XBRL-US Python API

Getting started is as simple as ever.
Update your XBRL-US Python package to the latest version and launch the new Browser Interface from the package menu.

Getting Started with the Browser Interface
------------------------------------------

Getting started is as simple as ever.
First, ensure you have the latest version of ``xbrl-us`` installed by running the following code:

.. list-table::
    :widths: 30 70
    :stub-columns: 1

    * - Command Line
      - .. code-block:: bash

            pip install xbrl-us --upgrade

    * - Jupyter Notebook
      - .. code-block:: bash

            !pip install xbrl-us --upgrade

Next, launch the new Browser Interface from the package menu from the command line by running the following code:

.. list-table::
    :widths: 30 70
    :stub-columns: 1

    * - Command Line
      - .. code-block:: bash

            python -m xbrl_us

    * - Jupyter Notebook
      - .. code-block:: bash

            !python -m xbrl_us

That is it!
You should now see the new Browser Interface open in your default web browser.

Happy data exploring!

.. note::

    Please note, while we have tested the interface extensively, this is its initial release.
    We encourage users to provide feedback to help us further improve the tool. We value your input!
    You can also find tutorials, example codes, and more resources to help you get started.



Development
===========

To run all the tests run:

.. code-block:: bash

    tox


Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    * - Windows
      - .. code-block:: bash

            set PYTEST_ADDOPTS=--cov-append
            tox


    * - Other
      - .. code-block:: bash

            PYTEST_ADDOPTS=--cov-append tox
