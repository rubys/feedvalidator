"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

import feedvalidator
import unittest, new, os, sys, glob, re

class TestCase(unittest.TestCase):
  def failUnlessContainsInstanceOf(self, theClass, params, theList, msg=None):
    """Fail if there are no instances of theClass in theList with given params"""
    failure=(msg or 'no %s instances in %s' % (theClass.__name__, `theList`))
    for item in theList:
      if item.__class__.__name__ == theClass.__name__:
        if not params: return
        for k, v in params.items():
          if item.params[k] <> v:
            failure=("%s.%s value was %s, expected %s" %
               (theClass.__name__, k, item.params[k], v))
            break
        else:
          return
    raise self.failureException, failure

  def failIfContainsInstanceOf(self, theClass, params, theList, msg=None):
    """Fail if there are instances of theClass in theList with given params"""
    for item in theList:
      if item.__class__.__name__ == theClass.__name__:
        if not params:
          raise self.failureException, \
             (msg or 'unexpected %s' % (theClass.__name__))
        allmatch = 1
        for k, v in params.items():
          if item.params[k] != v:
            allmatch = 0
        if allmatch:
          raise self.failureException, \
             "unexpected %s.%s with a value of %s" % \
             (theClass.__name__, k, v)

desc_re = re.compile("<!--\s*Description:\s*(.*?)\s*Expect:\s*(!?)(\w*)(?:{(.*?)})?\s*-->")

def getDescription(xmlfile):
  """Extract description and exception from XML file

  The deal here is that each test case is an XML file which contains
  not only a possibly invalid RSS feed but also the description of the
  test, i.e. the exception that we would expect the RSS validator to
  raise (or not) when it validates the feed.  The expected exception and
  the human-readable description are placed into an XML comment like this:

  <!--
    Description:  channel must include title
    Expect:     MissingTitle
  -->

  """

  stream = open(xmlfile)
  xmldoc = stream.read()
  stream.close()

  search_results = desc_re.search(xmldoc)
  if search_results:
    description, cond, excName, plist = list(search_results.groups())
  else:
    raise RuntimeError, "can't parse %s" % xmlfile

  if cond == "":
    method = TestCase.failUnlessContainsInstanceOf
  else:
    method = TestCase.failIfContainsInstanceOf

  params = {}
  if plist:
    for entry in plist.split(','):
      name,value = entry.lstrip().split(':',1)
      params[name] = value

  exc = getattr(feedvalidator, excName)

  description = xmlfile + ": " + description

  return method, description, params, exc

def buildTestCase(xmlfile, description, method, exc, params):
  """factory to create functions which validate `xmlfile`

  the returned function asserts that validating `xmlfile` (an XML file)
  will return a list of exceptions that include an instance of
  `exc` (an Exception class)
  """
  func = lambda self, xmlfile=xmlfile, exc=exc, params=params: \
       method(self, exc, params, feedvalidator.validateString(open(xmlfile).read())['loggedEvents'])
  func.__doc__ = description
  return func

if __name__ == "__main__":
  curdir = os.path.abspath(os.path.dirname(sys.argv[0]))
  basedir = os.path.split(curdir)[0]
  for xmlfile in glob.glob(os.path.join(basedir, 'testcases', '**', '**', '*.xml')):
    method, description, params, exc = getDescription(xmlfile)
    testName = 'test_' + os.path.basename(xmlfile)
    testFunc = buildTestCase(xmlfile, description, method, exc, params)
    instanceMethod = new.instancemethod(testFunc, None, TestCase)
    setattr(TestCase, testName, instanceMethod)
  unittest.main()

__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:14  rubys
Initial revision

Revision 1.2  2003/12/12 15:53:42  f8dy
renamed source directories

Revision 1.1  2003/08/06 16:56:14  f8dy
combined pievalidtest and rssvalidtest, renamed rssdemo to demo

Revision 1.20  2003/07/20 00:25:41  rubys
Search for *any* instance of a matching class/params in the log

Revision 1.19  2003/07/19 22:25:10  f8dy
fixed bug in test case suite runner, if an element in the expected params didn't match the expected value, it would set the failure message but not raise the appropriate exception, so rssvalidtest.py would claim that certain test cases passed when they didn't (this affected 7 test cases out of 700)

Revision 1.18  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.17  2003/07/07 10:35:50  rubys
Complete first pass of echo/pie tests

Revision 1.16  2003/07/06 21:20:02  rubys
Refactor so test cases are organized by protocol

Revision 1.15  2002/10/18 14:17:30  f8dy
added tests for language/dc:language (must be valid ISO-639 language code
plus optional country code) and passed them

Revision 1.14  2002/10/18 13:06:57  f8dy
added licensing information

"""
