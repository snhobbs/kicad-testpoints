#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'numpy',
    'pandas',
    'spreadsheet_wrangler>=0.1.3'
]

test_requirements = [ ]

setup(
    author="Simon Hobbs",
    author_email='simon.hobbs@electrooptical.net',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Extract pad positions from a kicad PCBNEW file with net data.",
    entry_points={
        'console_scripts': [
            'kicad_testpoints=kicad_testpoints.cli:main',
            'dataframe-to-openscad=kicad_testpoints.cli:dataframe_to_openscad',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='kicad_testpoints',
    name='kicad_testpoints',
    packages=find_packages(include=['kicad_testpoints', 'kicad_testpoints.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/snhobbs/kicad-testpoints',
    version='0.1.0',
    zip_safe=False,
)
