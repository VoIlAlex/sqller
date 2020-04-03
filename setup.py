from distutils.core import setup
from setuptools import find_packages
import os

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''


setup(
    # Name of the package
    name='sqller',

    # Packages to include into the distribution
    packages=find_packages('.'),

    # Start with a small number and increase it with every change you make
    # https://semver.org
    version='1.4.2',

    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    # For example: MIT
    license='MIT',

    # Short description of your library
    description='ORM library to build SQLite based application in format model/dao/service.',

    # Long description of your library
    long_description=long_description,
    long_description_content_type='text/markdown',

    # Your name
    author='Ilya Vouk',

    # Your email
    author_email='ilya.vouk@gmail.com',

    # Either the link to your github or to your website
    url='https://github.com/VoIlAlex',

    # Link from which the project can be downloaded
    download_url='https://github.com/VoIlAlex/sqller/archive/v1.4.2.tag.gz',

    # List of keyword arguments
    keywords=['orm', 'sql', 'sqlite', 'query', 'generation'],

    # List of packages to install with this one
    install_requires=[],

    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
