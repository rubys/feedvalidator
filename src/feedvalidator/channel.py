"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from logging import *
from validators import *
from sets import ImmutableSet

#
# channel element.
#
class channel(validatorBase):
  def getExpectedAttrNames(self):
    return ImmutableSet([(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'about'),
    	(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'about')])
 
  def validate(self):
    if not "description" in self.children:
      self.log(MissingDescription({"parent":self.name,"element":"description"}))
    if not "link" in self.children:
      self.log(MissingLink({"parent":self.name, "element":"link"}))
    if not "title" in self.children:
      self.log(MissingTitle({"parent":self.name, "element":"title"}))
    if not "dc_date" in self.children:
      self.log(MissingDCDate({"parent":self.name, "element":"dc:date"}))
    if not "dc_rights" in self.children:
      self.log(MissingDCRights({"parent":self.name, "element":"dc:rights"}))
    if not "dc_language" in self.children:
      self.log(MissingDCLanguage({"parent":self.name, "element":"dc:language"}))
    if self.children.count("image") > 1:
      self.log(DuplicateElement({"parent":self.name, "element":"image"}))
    if self.children.count("textInput") > 1:
      self.log(DuplicateElement({"parent":self.name, "element":"textInput"}))
    if self.children.count("skipHours") > 1:
      self.log(DuplicateElement({"parent":self.name, "element":"skipHours"}))
    if self.children.count("skipDays") > 1:
      self.log(DuplicateElement({"parent":self.name, "element":"skipDays"}))

  def do_image(self):
    from image import image
    return image()

  def do_item(self):
    from item import item
    return item()

  def do_items(self): # this actually should be from the rss1.0 ns
    return eater()

  def do_textInput(self):
    from textInput import textInput
    return textInput()

  def do_textinput(self):
    if not self.attrs.has_key((rdfNS,"about")):
      # optimize for RSS 2.0.  If it is not valid RDF, assume that it is
      # a simple misspelling (in other words, the error message will be
      # less than helpful on RSS 1.0 feeds.
      self.log(UndefinedElement({"parent":self.name, "element":"textinput"}))
    return eater()
  
  def do_category(self):
    return category()

  def do_cloud(self):
    return cloud()
  
  do_rating = validatorBase.leaf # TODO test cases?!?

  def do_ttl(self):
    return ttl(), noduplicates()
  
  def do_docs(self):
    return rfc2396(), noduplicates()
    
  def do_link(self):
    return rfc2396(), noduplicates()

  def do_title(self):
    return nonhtml(), noduplicates()

  def do_description(self):
    return nonhtml(), noduplicates()

  def do_generator(self):
    if "admin_generatorAgent" in self.children:
      self.log(DuplicateSemantics({"core":"generator", "ext":"admin:generatorAgent"}))
    self.log(UseAdminGeneratorAgent({"core":"generator", "ext":"admin:generatorAgent"}))
    return text(), noduplicates()

  def do_pubDate(self):
    if "dc_date" in self.children:
      self.log(DuplicateSemantics({"core":"pubDate", "ext":"dc:date"}))
    self.log(UseDCDate({"core":"pubDate", "ext":"dc:date"}))
    return rfc822(), noduplicates()

  def do_managingEditor(self):
    if "dc_creator" in self.children:
      self.log(DuplicateSemantics({"core":"managingEditor", "ext":"dc:creator"}))
    self.log(UseDCCreator({"core":"managingEditor", "ext":"dc:creator"}))
    return email(), noduplicates()

  def do_webMaster(self):
    if "dc_publisher" in self.children:
      self.log(DuplicateSemantics({"core":"webMaster", "ext":"dc:publisher"}))
    self.log(UseDCPublisher({"core":"webMaster", "ext":"dc:publisher"}))
    return email(), noduplicates()

  def do_dc_creator(self):
    if "managingEditor" in self.children:
      self.log(DuplicateSemantics({"core":"managingEditor", "ext":"dc:creator"}))
    return text() # duplicates allowed

  def do_dc_language(self):
    if "language" in self.children:
      self.log(DuplicateSemantics({"core":"language", "ext":"dc:language"}))
    return iso639(), noduplicates()

  def do_language(self):
    if "dc_language" in self.children:
      self.log(DuplicateSemantics({"core":"language", "ext":"dc:language"}))
    self.log(UseDCLanguage({"core":"language", "ext":"dc:language"}))
    return iso639(), noduplicates()

  def do_dcterms_modified(self):
    if "lastBuildDate" in self.children:
      self.log(DuplicateSemantics({"core":"lastBuildDate", "ext":"dcterms:modified"}))
    return iso8601_strict(), noduplicates()

  def do_dc_publisher(self):
    if "webMaster" in self.children:
      self.log(DuplicateSemantics({"core":"webMaster", "ext":"dc:publisher"}))
    return text() # duplicates allowed

  def do_copyright(self):
    if "dc_rights" in self.children:
      self.log(DuplicateSemantics({"core":"copyright", "ext":"dc:rights"}))
    self.log(UseDCRights({"core":"copyright", "ext":"dc:rights"}))
    return text(), noduplicates()

  def do_dc_rights(self):
    if "copyright" in self.children:
      self.log(DuplicateSemantics({"core":"copyright", "ext":"dc:rights"}))
    return text(), noduplicates()

  def do_dc_date(self):
    if "pubDate" in self.children:
      self.log(DuplicateSemantics({"core":"pubDate", "ext":"dc:date"}))
    return iso8601_strict(), noduplicates()

  def do_admin_generatorAgent(self):
    if "generator" in self.children:
      self.log(DuplicateSemantics({"core":"generator", "ext":"admin:generatorAgent"}))
    return admin_generatorAgent(), noduplicates()

  def do_admin_errorReportsTo(self):
    return admin_errorReportsTo(), noduplicates()

  def do_lastBuildDate(self):
    if "dcterms_modified" in self.children:
      self.log(DuplicateSemantics({"core":"lastBuildDate", "ext":"dcterms:modified"}))
    self.log(UseDCTermsModified({"core":"lastBuildDate", "ext":"dcterms:modified"}))
    return rfc822(), noduplicates()

  def do_skipHours(self):
    from skipHours import skipHours
    return skipHours()

  def do_skipDays(self):
    from skipDays import skipDays
    return skipDays()

  def do_blogChannel_blogRoll(self):
    return rfc2396(), noduplicates()

  def do_blogChannel_mySubscriptions(self):
    return rfc2396(), noduplicates()

  def do_blogChannel_blink(self):
    return rfc2396(), noduplicates()

  def do_cc_license(self):
    if "creativeCommons_license" in self.children:
      self.log(DuplicateSemantics({"core":"creativeCommons:license", "ext":"cc:license"}))
    return eater()

  def do_creativeCommons_license(self):
    if "cc_license" in self.children:
      self.log(DuplicateSemantics({"core":"creativeCommons:license", "ext":"cc:license"}))
    return rfc2396()

  def do_blink(self):
    return blink(), noduplicates()

  def do_sy_updatePeriod(self):
    return sy_updatePeriod(), noduplicates()

  def do_sy_updateFrequency(self):
    return sy_updateFrequency(), noduplicates()

  def do_sy_updateBase(self):
    return iso8601_strict(), noduplicates()

class blink(validatorBase):
  def validate(self):
    self.log(NoBlink({}))
 
class category(text):
  def getExpectedAttrNames(self):
    return ImmutableSet([(None, u'domain')])

class cloud(validatorBase):
  def getExpectedAttrNames(self):
    return ImmutableSet([(None, u'domain'), (None, u'path'), (None, u'registerProcedure'),
    	(None, u'protocol'), (None, u'port')])
  def prevalidate(self):
    if (None, 'domain') not in self.attrs.getNames():
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"domain"}))
    else:
      self.log(ValidCloud({"parent":self.parent.name, "element":self.name, "attr":"domain"}))

    try:
      if int(self.attrs.getValue((None, 'port'))) <= 0:
        self.log(InvalidIntegerAttribute({"parent":self.parent.name, "element":self.name, "attr":'port'}))
      else:
        self.log(ValidCloud({"parent":self.parent.name, "element":self.name, "attr":'port'}))
    except KeyError:
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":'port'}))
    except ValueError:
      self.log(InvalidIntegerAttribute({"parent":self.parent.name, "element":self.name, "attr":'port'}))

    if (None, 'path') not in self.attrs.getNames():
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"path"}))
    else:
      self.log(ValidCloud({"parent":self.parent.name, "element":self.name, "attr":"path"}))

    if (None, 'registerProcedure') not in self.attrs.getNames():
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"registerProcedure"}))
    else:
      self.log(ValidCloud({"parent":self.parent.name, "element":self.name, "attr":"registerProcedure"}))

    if (None, 'protocol') not in self.attrs.getNames():
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"protocol"}))
    else:
      self.log(ValidCloud({"parent":self.parent.name, "element":self.name, "attr":"protocol"}))
    ## TODO - is there a list of accepted protocols for this thing?

    return validatorBase.prevalidate(self)

class ttl(positiveInteger): pass

class admin_generatorAgent(rdfResourceURI): pass
class admin_errorReportsTo(rdfResourceURI): pass

class sy_updateFrequency(positiveInteger): pass

class sy_updatePeriod(text):
  def validate(self):
    if self.value not in ('hourly', 'daily', 'weekly', 'monthly', 'yearly'):
      self.log(InvalidUpdatePeriod({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      self.log(ValidUpdatePeriod({"parent":self.parent.name, "element":self.name, "value":self.value}))

__history__ = """
$Log$
Revision 1.4  2004/02/17 19:18:04  rubys
Commit patch 886668: ISO 8601 times with no timezone shouldn't be valid

Revision 1.3  2004/02/17 15:38:39  rubys
Remove email_lax which previously accepted an email address anyplace
within the element

Revision 1.2  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.1.1.1  2004/02/03 17:33:15  rubys
Initial import.

Revision 1.30  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.29  2003/08/04 00:03:14  rubys
Implement more strict email check for pie

Revision 1.28  2003/07/30 01:54:59  f8dy
tighten test cases, add explicit params

Revision 1.27  2003/07/29 20:57:39  f8dy
tightened up test cases, check for parent element, explicitly test for success

Revision 1.26  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.25  2003/07/29 16:44:56  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.24  2002/12/20 13:26:00  rubys
CreativeCommons support

Revision 1.23  2002/10/24 14:47:33  f8dy
decoupled "no duplicates" check from individual validator classes,
allow handlers to return multiple validator classes

Revision 1.22  2002/10/22 17:29:52  f8dy
loosened restrictions on link/docs/url protocols; RSS now allows any
IANA protocol, not just http:// and ftp://

Revision 1.21  2002/10/22 16:43:55  rubys
textInput vs textinput: don't reject valid 1.0 feeds, but don't allow
invalid textinput fields in RSS 2.0 either...

Revision 1.20  2002/10/22 14:11:36  f8dy
initial attempts to handle RSS 1.0 vs. 2.0 images and textinputs; test
cases still fail

Revision 1.19  2002/10/22 13:16:03  f8dy
passed lowercase textinput test

Revision 1.18  2002/10/18 19:28:43  f8dy
added testcases for mod_syndication and passed them

Revision 1.17  2002/10/18 15:41:33  f8dy
added (and passed) testcases for unallowed duplicates of the same element

Revision 1.16  2002/10/18 14:17:30  f8dy
added tests for language/dc:language (must be valid ISO-639 language code
plus optional country code) and passed them

Revision 1.15  2002/10/18 13:06:57  f8dy
added licensing information

"""
