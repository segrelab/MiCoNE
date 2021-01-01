"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "biom-format",
    "click",
    "decorator",
    "ete3",
    "future",
    "h5py",
    "jinja2",
    "jinja2schema",
    "loguru",
    "markupsafe",
    "networkx",
    "numpy",
    "pandas",
    "patsy",
    "python-dateutil",
    "pytz",
    "schematics",
    "scipy",
    "simplejson",
    "six",
    "statsmodels",
    "toml",
]

setup_requirements = ["numpy", "Cython", "pytest-runner"]

test_requirements = ["pytest", "pytest-cov"]

setup(
    author="Dileep Kishore",
    author_email="dkishore@bu.edu",
    classifiers=[
        "Development Status :: Beta",
        "Intended Audience :: Scientists, Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    description="The pipeline that powers the Microbial Interaction Network Database",
    entry_points={"console_scripts": ["micone=micone.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="micone",
    name="micone",
    packages=find_packages(include=["micone"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/dileep-kishore/micone",
    version="0.5.0",
    zip_safe=False,
)
