"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from logging import *
from validators import *
from itunes import itunes_channel
from extension import *

#
# channel element.
#
class channel(validatorBase, rfc2396, extension_channel, itunes_channel):
  def validate(self):
    if not "description" in self.children:
      self.log(MissingDescription({"parent":self.name,"element":"description"}))
    if not "link" in self.children:
      self.log(MissingLink({"parent":self.name, "element":"link"}))
    if not "title" in self.children:
      self.log(MissingTitle({"parent":self.name, "element":"title"}))
    if not "dc_language" in self.children and not "language" in self.children:
      if not self.xmlLang:
        self.log(MissingDCLanguage({"parent":self.name, "element":"language"}))
    if self.children.count("image") > 1:
      self.log(DuplicateElement({"parent":self.name, "element":"image"}))
    if self.children.count("textInput") > 1:
      self.log(DuplicateElement({"parent":self.name, "element":"textInput"}))
    if self.children.count("skipHours") > 1:
      self.log(DuplicateElement({"parent":self.name, "element":"skipHours"}))
    if self.children.count("skipDays") > 1:
      self.log(DuplicateElement({"parent":self.name, "element":"skipDays"}))
    if self.attrs.has_key((rdfNS,"about")):
      self.value = self.attrs.getValue((rdfNS, "about"))
      rfc2396.validate(self, extraParams={"attr": "rdf:about"})
      if not "items" in self.children:
        self.log(MissingElement({"parent":self.name, "element":"items"}))

    if self.itunes: itunes_channel.validate(self)

  def do_image(self):
    from image import image
    return image(), noduplicates()

  def do_textInput(self):
    from textInput import textInput
    return textInput(), noduplicates()

  def do_textinput(self):
    if not self.attrs.has_key((rdfNS,"about")):
      # optimize for RSS 2.0.  If it is not valid RDF, assume that it is
      # a simple misspelling (in other words, the error message will be
      # less than helpful on RSS 1.0 feeds.
      self.log(UndefinedElement({"parent":self.name, "element":"textinput"}))
    return eater(), noduplicates()
  
  def do_link(self):
    return rfc2396_full(), noduplicates()

  def do_title(self):
    return nonhtml(), noduplicates(), nonblank()

  def do_description(self):
    return nonhtml(), noduplicates()

  def do_blink(self):
    return blink(), noduplicates()

  def do_atom_author(self):
    self.metadata()
    from author import author
    return author()

  def do_atom_category(self):
    self.metadata()
    from category import category
    return category()

  def do_atom_contributor(self):
    self.metadata()
    from author import author
    return author()

  def do_atom_generator(self):
    self.metadata()
    from generator import generator
    return generator(), nonblank(), noduplicates()

  def do_atom_id(self):
    return rfc2396_full(), noduplicates()

  def do_atom_icon(self):
    self.metadata()
    return nonblank(), rfc2396(), noduplicates()

  def do_atom_link(self):
    from link import link
    return link()

  def do_atom_logo(self):
    self.metadata()
    return nonblank(), rfc2396(), noduplicates()

  def do_atom_title(self):
    self.metadata()
    from content import textConstruct
    return textConstruct(), noduplicates()
  
  def do_atom_subtitle(self):
    self.metadata()
    from content import textConstruct
    return textConstruct(), noduplicates()
  
  def do_atom_rights(self):
    self.metadata()
    from content import textConstruct
    return textConstruct(), noduplicates()

  def do_atom_updated(self):
    self.metadata()
    return rfc3339(), noduplicates()

  def do_dc_creator(self):
    if "managingEditor" in self.children:
      self.log(DuplicateSemantics({"core":"managingEditor", "ext":"dc:creator"}))
    return text() # duplicates allowed

  def do_dc_subject(self):
    if "category" in self.children:
      self.log(DuplicateSemantics({"core":"category", "ext":"dc:subject"}))
    return text() # duplicates allowed

  def do_dc_date(self):
    if "pubDate" in self.children:
      self.log(DuplicateSemantics({"core":"pubDate", "ext":"dc:date"}))
    return w3cdtf(), noduplicates()

  def do_cc_license(self):
    if "creativeCommons_license" in self.children:
      self.log(DuplicateSemantics({"core":"creativeCommons:license", "ext":"cc:license"}))
    return eater()

  def do_creativeCommons_license(self):
    if "cc_license" in self.children:
      self.log(DuplicateSemantics({"core":"creativeCommons:license", "ext":"cc:license"}))
    return rfc2396_full()

class rss20Channel(channel):
  def do_item(self):
    from item import rss20Item
    return rss20Item()

  def do_category(self):
    return category()

  def do_cloud(self):
    return cloud(), noduplicates()
  
  do_rating = validatorBase.leaf # TODO test cases?!?

  def do_ttl(self):
    return positiveInteger(), nonblank(), noduplicates()
  
  def do_docs(self):
    return rfc2396_full(), noduplicates()
    
  def do_generator(self):
    if "admin_generatorAgent" in self.children:
      self.log(DuplicateSemantics({"core":"generator", "ext":"admin:generatorAgent"}))
    return text(), noduplicates()

  def do_pubDate(self):
    if "dc_date" in self.children:
      self.log(DuplicateSemantics({"core":"pubDate", "ext":"dc:date"}))
    return rfc822(), noduplicates()

  def do_managingEditor(self):
    if "dc_creator" in self.children:
      self.log(DuplicateSemantics({"core":"managingEditor", "ext":"dc:creator"}))
    return email(), noduplicates()

  def do_webMaster(self):
    if "dc_publisher" in self.children:
      self.log(DuplicateSemantics({"core":"webMaster", "ext":"dc:publisher"}))
    return email(), noduplicates()

  def do_language(self):
    if "dc_language" in self.children:
      self.log(DuplicateSemantics({"core":"language", "ext":"dc:language"}))
    return iso639(), noduplicates()

  def do_copyright(self):
    if "dc_rights" in self.children:
      self.log(DuplicateSemantics({"core":"copyright", "ext":"dc:rights"}))
    return text(), noduplicates()

  def do_lastBuildDate(self):
    if "dcterms_modified" in self.children:
      self.log(DuplicateSemantics({"core":"lastBuildDate", "ext":"dcterms:modified"}))
    return rfc822(), noduplicates()

  def do_skipHours(self):
    from skipHours import skipHours
    return skipHours()

  def do_skipDays(self):
    from skipDays import skipDays
    return skipDays()

class rss10Channel(channel):
  def getExpectedAttrNames(self):
    return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'about'),
      (u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'about')]
 
  def prevalidate(self):
    if self.attrs.has_key((rdfNS,"about")):
      if not "abouts" in self.dispatcher.__dict__:
        self.dispatcher.__dict__["abouts"] = []
      self.dispatcher.__dict__["abouts"].append(self.attrs[(rdfNS,"about")])

  def do_items(self): # this actually should be from the rss1.0 ns
    if not self.attrs.has_key((rdfNS,"about")):
      self.log(MissingAttribute({"parent":self.name, "element":self.name, "attr":"rdf:about"}))
    from item import items
    return items(), noduplicates()

  def do_rdfs_label(self):
      return text()

  def do_rdfs_comment(self):
      return text()



class blink(text):
  def validate(self):
    self.log(NoBlink({}))
 
class category(nonhtml):
  def getExpectedAttrNames(self):
    return [(None, u'domain')]

class cloud(validatorBase):
  def getExpectedAttrNames(self):
    return [(None, u'domain'), (None, u'path'), (None, u'registerProcedure'),
      (None, u'protocol'), (None, u'port')]
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

__history__ = """
$Log$
Revision 1.30  2006/02/12 03:43:57  rubys
rss20 channel test cases

Revision 1.29  2006/02/05 02:12:33  rubys
More thorough testing of HTML in various RSS 2.0 elements

Revision 1.28  2006/01/22 16:54:49  rubys
Separate message for invalid ISO8601 date time

Revision 1.27  2006/01/01 17:17:18  rubys
Eliminate several unexpected "UnexpectedText" errors

Revision 1.26  2005/11/20 00:36:00  rubys
Initial support for gbase namespace

Revision 1.25  2005/11/08 18:27:42  rubys
Warn on missing language, itunes:explicit, or itunes:category if any itunes
elements are present.

Revision 1.24  2005/07/26 19:59:59  rubys
More RSS+Atom support

Revision 1.23  2005/07/04 22:54:31  philor
Support rest of dc, dcterms, geo, geourl, icbm, and refactor out common extension elements

Revision 1.22  2005/07/03 21:09:03  philor
Support mod_changedpage, mod_threading, mod_aggregation

Revision 1.21  2005/07/02 19:26:44  rubys
Issue warnings for itunes tags which appear to contain HTML.

Note: this will also cause warnings to appear for titles and a
few other select tags (not descriptions!).  Previously, only
informational messages (which, by default, are not displayed)
were generated.

If this is a problem, we can change some individual tags, or
split this into two messages (one a warning, one informational).

Revision 1.20  2005/07/02 07:39:38  philor
Support blogChannel_changes

Revision 1.19  2005/07/01 23:55:30  rubys
Initial support for itunes

Revision 1.18  2005/06/29 23:53:56  rubys
Fixes:
  channel level dc:subject and foaf:maker
  item level dc:language and rdfs:seeAlso
  rdf:RDF level cc:License

Revision 1.17  2005/06/29 17:33:29  rubys
Fix for bug 1229805

Revision 1.16  2005/06/28 22:14:59  rubys
Catch errors involving unknown elements in known namespaces

Revision 1.15  2005/01/28 00:06:25  josephw
Use separate 'item' and 'channel' classes to reject RSS 2.0 elements in
 RSS 1.0 feeds (closes 1037785).

Revision 1.14  2005/01/22 05:28:02  rubys
Channel titles must be non-blank

Revision 1.13  2005/01/22 01:22:39  rubys
pass testcases/rss11/must/neg-ext-adupabout.xml

Revision 1.12  2005/01/19 01:28:13  rubys
Initial support for rss 1.1

Revision 1.11  2004/07/28 12:24:25  rubys
Partial support for verifing xml:lang

Revision 1.10  2004/07/28 02:23:41  rubys
Remove some experimental rules

Revision 1.9  2004/04/06 22:32:07  rubys
Fix for bug 930536: missing items element in an rss 1.0 feed

Revision 1.8  2004/02/26 22:41:57  rubys
Enforce cardinality on items element

Revision 1.7  2004/02/18 16:12:14  rubys
Make the distiction between W3CDTF and ISO8601 clearer in the docs.

Revision 1.6  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.5  2004/02/17 22:42:02  rubys
Remove dependence on Python 2.3

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
