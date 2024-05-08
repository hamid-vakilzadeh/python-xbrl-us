#!/usr/bin/env python
import re
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with Path(__file__).parent.joinpath(*names).open(encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


setup(
    name="xbrl-us",
    version="0.0.43",
    license="MIT",
    description="Python wrapper for xbrl.us API",
    long_description_content_type="text/x-rst",
    long_description="{}\n{}".format(
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub("", read("README.rst")),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="hamid-vakilzadeh",
    author_email="vakilzas@uww.edu",
    url="https://github.com/hamid-vakilzadeh/python-xbrl-us",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[path.stem for path in Path("src").glob("*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        # "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # uncomment if you test on these interpreters:
        # "Programming Language :: Python :: Implementation :: IronPython",
        # "Programming Language :: Python :: Implementation :: Jython",
        # "Programming Language :: Python :: Implementation :: Stackless",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://python-xbrl-us.readthedocs.io/",
        "Changelog": "https://python-xbrl-us.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/hamid-vakilzadeh/python-xbrl-us/issues",
    },
    keywords=[
        # eg: "xbrl-us", "xbrl", "sec",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.1",
        "pandas>= 1.3.0, < 3",
        "PyYAML>=5.3",
        "streamlit>=1.32.2",
        "retry>=0.9.2",
        "tqdm>=4.61.2",
        "stqdm>=0.0.5",
    ],
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=="2.6"": ["argparse"],
    },
    entry_points={
        "console_scripts": [
            "xbrl-us = xbrl_us.cli:main",
        ]
    },
)
