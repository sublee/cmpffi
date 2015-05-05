# -*- coding: utf-8 -*-
"""
"""
from __future__ import with_statement
import re
from setuptools import setup


# detect the current version
with open('cmpffi.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version


import cmpffi


setup(
    name='cmpffi',
    version=version,
    license='BSD',
    author='Heungsub Lee',
    author_email=re.sub('((sub).)(.*)', r'\2@\1.\3', 'sublee'),
    url='https://github.com/sublee/cmpffi',
    description='CMP, an alternative MsgPack C implementation, for Python',
    long_description=__doc__,
    platforms='any',
    py_modules=['cmpffi'],
    ext_modules=[cmpffi.ffi.verifier.get_extension()],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Topic :: Games/Entertainment'],
    install_requires=['cffi'],
)
