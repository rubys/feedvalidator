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

import feedvalidator

class FeedValidatorTest(unittest.TestCase):
  def testPlainTextDoesnNotLookLikeAFeed(self):
    self.assertFalse(feedvalidator.sniffPossibleFeed("Not Found"))

  def testTrailingXmlLooksLikeAFeed(self):
    self.assertTrue(feedvalidator.sniffPossibleFeed('</rss>'))
    self.assertTrue(feedvalidator.sniffPossibleFeed('</feed>'))
    self.assertTrue(feedvalidator.sniffPossibleFeed('</rdf:RDF>'))
    self.assertTrue(feedvalidator.sniffPossibleFeed('</kml>'))

  def testLeadingXmlLooksLikeAFeed(self):
    self.assertTrue(feedvalidator.sniffPossibleFeed('<rss>'))
    self.assertTrue(feedvalidator.sniffPossibleFeed('<feed>'))
    self.assertTrue(feedvalidator.sniffPossibleFeed('<rdf:RDF>'))
    self.assertTrue(feedvalidator.sniffPossibleFeed('<kml>'))

  def testHtmlDoesNotLookLikeAFeed(self):
    self.assertFalse(feedvalidator.sniffPossibleFeed("<!DOCTYPE html>"))

def buildTestSuite():
  return unittest.TestLoader().loadTestsFromTestCase(FeedValidatorTest)

if __name__ == '__main__':
  unittest.main()
