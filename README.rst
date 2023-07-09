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

If you are utilizing the XBRL US Python Wrapper for research purposes, we kindly request that you cite the following paper:

[FILL: Insert Paper Title]

[FILL: Authors]

[FILL: Publication Details]



Tutorial ✏️📖📚
================

This tutorial will guide you through using the XBRL-US Python library to interact with the XBRL API. The XBRL-US library provides a convenient way to query and retrieve financial data from the XBRL API using Python.

Prerequisites
~~~~~~~~~~~~~

Before you begin, ensure you have the following:

* **Python installed on your system**.
  Right now, the XBRL-US library supports Python 3.10 and above.
  Backwards compatibility with Python 3.7 and above is planned for a future release.
* **XBRL-US library installed**.
* **XBRL-US API credentials**.
  You can obtain your credentials by registering for a
  free XBRL-US account at https://xbrl.us/home/use/xbrl-api/.
* **XBRL-US OAuth2 Access**.
  You can obtain your client ID and client secret by registering for a
  free XBRL-US account at https://xbrl.us/home/use/xbrl-api/access-token/.

You can install it using pip:

.. code-block:: bash

    pip install xbrl-us


**Documentation**

For detailed information about the XBRL-US Python
library, you can refer to the documentation at https://python-xbrl-us.readthedocs.io/en/latest/.

**Official Documentation**

For more information about the XBRL API and its endpoints, refer to the original API documentation at https://xbrlus.github.io/xbrl-api.

Step 1: Import the XBRL Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To start using the XBRL-US library,
you need to import it into your Python script::

    from xbrl_us import XBRL

Step 2: Create an Instance of XBRL Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, you need to create an instance of the ``XBRL`` class,
providing your authentication credentials
(client ID, client secret, username, and password) as parameters::

    xbrl = XBRL(
    client_id='Your client id',
    client_secret='Your client secret',
    username='Your username',
    password='Your password'
    )

Make sure to replace ``Your client id``,
``Your client secret``, ``Your username``, and
``Your password`` with your actual credentials.

Step 3: Query the XBRL API
~~~~~~~~~~~~~~~~~~~~~~~~~~

The XBRL-US library provides a query method to search
for data from the XBRL API. You can specify various
parameters and fields to filter and retrieve the
desired data.

Here's an example of using the query method to search
for specific financial facts::

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
        limit={'fact': 100},
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
readable, less prone to errors, and easier to maintain::

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
        limit={'fact': 100},
        as_dataframe=True
    )


This alternative approach also allows you to
take advantage of the autocomplete feature of your IDE to
easily find the parameters and fields.

Step 4: Perform Additional Queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the same query method to call other API
endpoints by changing the method parameter and
providing the relevant parameters and fields.

Here's an example of using the query method to
search for a specific fact by its ID::

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


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
