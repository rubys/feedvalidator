#!/usr/bin/python
"""$Id$"""

__author__ = "Joseph Walton <http://www.kafsemo.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2004 Joseph Walton"
__license__ = "Python"

import os, sys

curdir = os.path.abspath(os.path.dirname(sys.argv[0]))
srcdir = os.path.split(curdir)[0]
if srcdir not in sys.path:
  sys.path.insert(0, srcdir)
basedir = os.path.split(srcdir)[0]

import unittest, new, glob, re
from feedvalidator import xmlEncoding

class EncodingTestCase(unittest.TestCase):
  def testEncodingMatches(self):
    r = open(self.filename, 'r').read(256)
    try:
      enc = xmlEncoding.detect(r)
    except UnicodeError,u:
      self.fail("'" + self.filename + "' should not cause an exception (" + str(u) + ")")

    self.assert_(enc, 'An encoding must be returned for all valid files ('
        + self.filename + ')')
    self.assertEqual(enc, self.expectedEncoding, 'Encoding for '
        + self.filename + ' should be ' + self.expectedEncoding + ', but was ' + enc)

  def testEncodingFails(self):
    eventLog = []
    r = open(self.filename, 'r').read(256)

    try:
      encoding = xmlEncoding.detect(r, eventLog)
    except UnicodeError,u:
      self.fail("'" + self.filename + "' should not cause an exception (" + str(u) + ")")

    if encoding:
      self.fail("'" + self.filename + "' should not parse successfully (as " + encoding + ")")

    if not(eventLog):
      self.fail("'" + self.filename + "' should give a reason for parse failure")


expectedName = re.compile('/([a-z]+)_([-A-Za-z0-9]+)([-_A-Za-z0-9]*)\.xml')

def makeSuite(basedir):
  suite = unittest.TestSuite()
  allFiles = glob.glob(os.path.join(basedir, 'tmp', '*.xml'))
  assert allFiles,'Run genXmlTestcases first'
  for xmlfile in allFiles:
    m = expectedName.search(xmlfile)
    if m:
      v,enc = m.group(1), m.group(2)
      if v == 'valid':
        t = EncodingTestCase('testEncodingMatches')
        t.expectedEncoding = enc
      elif v == 'invalid':
        t = EncodingTestCase('testEncodingFails')
      t.filename = xmlfile
      suite.addTest(t)
  return suite

if __name__ == "__main__":
  s = makeSuite(basedir)
  unittest.TextTestRunner().run(s)

__history__ = """
$Log$
Revision 1.2  2004/03/30 10:48:27  josephw
Treat UnicodeError as a failure, rather than an error.

Revision 1.1  2004/03/30 08:11:45  josephw
Added a test for xmlEncoding. Made detect() log any problems.

"""
