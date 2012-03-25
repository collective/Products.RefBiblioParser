import os, sys

from setuptools import setup, find_packages

version = u'1.0'

def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

long_description = "\n\n".join(
    [read('README.rst'),
     read('docs', 'INSTALL.rst'),
     read('docs', 'CHANGES.rst'),
    ]
)

classifiers = [
    "Framework :: Plone",
    "Framework :: Plone :: 4.0",
    "Framework :: Plone :: 4.1",
    "Framework :: Plone :: 4.2",
    "Programming Language :: Python",
    "Topic :: Software Development",]

name = 'Products.RefBiblioParser'
setup(
    name=name,
    namespace_packages=[         'Products',
    ],
    version=version,
    description='Project %s',
    long_description=long_description,
    classifiers=classifiers,
    keywords='ref biblio parser',
    author='kiorky',
    author_email='kiorky@cryptelium.net',
    url='http://pypi.python.org/pypi/%s' % name,
    license='GPL',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'z3c.autoinclude',
        'Plone',
        'plone.app.upgrade',
        # with_ploneproduct_dexterity
        'z3c.blobfile',
        'plone.app.dexterity',
        # -*- Extra requirements: -*-
    ],
    extras_require = {
        'test': ['plone.app.testing',]
    },
    entry_points = {
        'z3c.autoinclude.plugin': ['target = plone',],
    },
)
# vim:set ft=python:
