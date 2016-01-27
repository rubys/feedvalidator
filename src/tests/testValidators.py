#!/usr/bin/python

__author__ = "Joseph Walton <http://www.kafsemo.org/>"
__copyright__ = "Copyright (c) 2011 Joseph Walton"

import os, sys

curdir = os.path.abspath(os.path.dirname(sys.argv[0]))
srcdir = os.path.split(curdir)[0]
if srcdir not in sys.path:
  sys.path.insert(0, srcdir)
basedir = os.path.split(srcdir)[0]

import unittest

from feedvalidator import validators

import re

class ValidatorsTest(unittest.TestCase):
  def testExpectedTldIsAValidDomain(self):
    self.assertTrue(re.compile(validators.addr_spec.domain_re, re.I).match('feedvalidator.org'))

  def testNewerTldIsAValidDomain(self):
    self.assertTrue(re.compile(validators.addr_spec.domain_re, re.I).match('example.aaa'))

def buildTestSuite():
  return unittest.TestLoader().loadTestsFromTestCase(ValidatorsTest)

if __name__ == '__main__':
  unittest.main()
