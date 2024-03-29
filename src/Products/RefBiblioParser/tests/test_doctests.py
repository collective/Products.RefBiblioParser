"""
Launching all doctests in the tests directory using:

    - the base layer in testing.py

"""

from Products.RefBiblioParser.tests.base import FunctionalTestCase

################################################################################
# GLOBALS avalaible in doctests
# IMPORT/DEFINE objects there or inside ./user_globals.py (better)
# globals from the testing product are also available.
################################################################################
# example:
# from for import bar
# and in your doctests, you can do:
# >>> bar.something
from Products.RefBiblioParser.tests.globals import *
from Products.RefBiblioParser.testing import PRODUCTS_REFBIBLIOPARSER_FUNCTIONAL_TESTING as FUNCTIONAL_TESTING
################################################################################


import unittest2 as unittest
import glob
import os
import logging
import doctest
from plone.testing import layered

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """."""
    logger = logging.getLogger('Products.RefBiblioParser.tests')
    cwd = os.path.dirname(__file__)
    files = []
    try:
        files = glob.glob(os.path.join(cwd, '*txt'))
    except Exception,e:
        logger.warn('No doctests for Products.RefBiblioParser')
    suite = unittest.TestSuite()
    globs = globals()
    for s in files:
        suite.addTests([
            layered(
                doctest.DocFileSuite(
                    s, 
                    globs = globs,
                    module_relative=False,
                    optionflags=optionflags,         
                ),
                layer=FUNCTIONAL_TESTING
            ),
        ])
    return suite
    


# vim:set ft=python:
