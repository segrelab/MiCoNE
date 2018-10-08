"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy',
    'pandas',
    'jinja2',
    'dask',
    'cloudpickle',
    'biom-format',
    'ete3',
    'h5py',
    'statsmodels',
    'networkx',
    'toml',
    'schematics'
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'pytest-cov']

setup(
    author="Dileep Kishore",
    author_email='dkishore@bu.edu',
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="The pipeline that powers the Microbial Interaction Network Database",
    entry_points={
        'console_scripts': [
            'mindpipe=mindpipe.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mindpipe',
    name='mindpipe',
    packages=find_packages(include=['mindpipe']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dileep-kishore/mindpipe',
    version='0.4.1',
    zip_safe=False,
)
