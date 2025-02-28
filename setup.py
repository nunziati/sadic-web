#!/usr/bin/env python

from setuptools import setup, find_packages
import sadicweb.core.sadicapp as sadicapp

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sadicweb',
    version=sadicapp.VERSION,
    description='sadicweb',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='blabla',
    url='https://lalal.com',
    project_urls={
        'Bug Tracker': 'https://github.com/',
        'Documentation': 'https://',
        'Source Code': 'https://'
    },
    author='gente',
    license='GNU General Public License v3 (GPLv3)',
    python_requires='>=3.10',
    packages=find_packages(),
    install_requires=[
        'Django==4.2.11',
        'django-crispy-forms==2.1',
        'crispy-bootstrap4==2024.1',
        'django-environ==0.11.2',
        'django-model-utils==4.4.0',
        'django-picklefield==3.1',
        'django-split-settings==1.3.0',
    ],
    entry_points={
        'console_scripts': [
            'sadicweb = sadicweb:manage',
        ],
    },
    include_package_data = True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Systems Administration',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ]
)