========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-xbrl-us/badge/?style=flat
    :target: https://python-xbrl-us.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/hamid-vakilzadeh/python-xbrl-us/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/hamid-vakilzadeh/python-xbrl-us/actions

.. |version| image:: https://img.shields.io/pypi/v/xbrl-us.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/xbrl-us

.. |wheel| image:: https://img.shields.io/pypi/wheel/xbrl-us.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/xbrl-us

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/xbrl-us.svg
    :alt: Supported versions
    :target: https://pypi.org/project/xbrl-us

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/xbrl-us.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/xbrl-us

.. |commits-since| image:: https://img.shields.io/github/commits-since/hamid-vakilzadeh/python-xbrl-us/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/hamid-vakilzadeh/python-xbrl-us/compare/v0.0.0...main



.. end-badges

APython wrapper for xbrl-us API

* Free software: MIT license

Installation
============

::

    pip install xbrl-us

You can also install the in-development version with::

    pip install https://github.com/hamid-vakilzadeh/python-xbrl-us/archive/main.zip


Documentation
=============


https://python-xbrl-us.readthedocs.io/en/latest/


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
