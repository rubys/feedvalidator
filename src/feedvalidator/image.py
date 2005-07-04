"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *
from extension import extension

#
# image element.
#
class image(validatorBase, extension):
  def getExpectedAttrNames(self):
    return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'resource'),
            (u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'about'),
            (u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'parseType')]
  def validate(self):
    if self.attrs.has_key((rdfNS,"resource")):
      return # looks like an RSS 1.0 feed
    if not "title" in self.children:
      self.log(MissingTitle({"parent":self.name, "element":"title"}))
    if not "url" in self.children:
      self.log(MissingElement({"parent":self.name, "element":"url"}))
    if self.attrs.has_key((rdfNS,"parseType")):
      return # looks like an RSS 1.1 feed
    if not "link" in self.children:
      self.log(MissingLink({"parent":self.name, "element":"link"}))

  def do_title(self):
    return title(), noduplicates()

  def do_link(self):
    return rfc2396_full(), noduplicates()

  def do_url(self):
    return rfc2396_full(), noduplicates()

  def do_width(self):
    return width(), noduplicates()

  def do_height(self):
    return height(), noduplicates()

  def do_description(self):
    return text(), noduplicates()
  
  def do_dc_creator(self):
    return text()

  def do_dc_subject(self):
    return text() # duplicates allowed

  def do_dc_date(self):
    return w3cdtf(), noduplicates()

  def do_cc_license(self):
    return eater()

class title(text, noduplicates):
  def validate(self):
    if not self.value.strip():
      self.log(NotBlank({"parent":self.parent.name, "element":self.name}))
    else:
      self.log(ValidTitle({"parent":self.parent.name, "element":self.name}))
    return nonhtml()

class width(text, noduplicates):
  def validate(self):
    try:
      w = int(self.value)
      if (w <= 0) or (w > 144):
        self.log(InvalidWidth({"parent":self.parent.name, "element":self.name, "value":self.value}))
      else:
        self.log(ValidWidth({"parent":self.parent.name, "element":self.name}))
    except ValueError:
      self.log(InvalidWidth({"parent":self.parent.name, "element":self.name, "value":self.value}))

class height(text, noduplicates):
  def validate(self):
    try:
      h = int(self.value)
      if (h <= 0) or (h > 400):
        self.log(InvalidHeight({"parent":self.parent.name, "element":self.name, "value":self.value}))
      else:
        self.log(ValidHeight({"parent":self.parent.name, "element":self.name}))
    except ValueError:
      self.log(InvalidHeight({"parent":self.parent.name, "element":self.name, "value":self.value}))

__history__ = """
$Log$
Revision 1.7  2005/07/04 22:54:31  philor
Support rest of dc, dcterms, geo, geourl, icbm, and refactor out common extension elements

Revision 1.6  2005/07/02 19:26:44  rubys
Issue warnings for itunes tags which appear to contain HTML.

Note: this will also cause warnings to appear for titles and a
few other select tags (not descriptions!).  Previously, only
informational messages (which, by default, are not displayed)
were generated.

If this is a problem, we can change some individual tags, or
split this into two messages (one a warning, one informational).

Revision 1.5  2005/01/19 01:28:13  rubys
Initial support for rss 1.1

Revision 1.4  2004/07/28 02:23:41  rubys
Remove some experimental rules

Revision 1.3  2004/02/18 15:38:17  rubys
rdf:resource and rdf:about attributes are flagged on image tags in rss 1.0

Revision 1.2  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.1.1.1  2004/02/03 17:33:15  rubys
Initial import.

Revision 1.11  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.10  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.9  2002/10/24 14:47:33  f8dy
decoupled "no duplicates" check from individual validator classes,
allow handlers to return multiple validator classes

Revision 1.8  2002/10/22 17:29:52  f8dy
loosened restrictions on link/docs/url protocols; RSS now allows any
IANA protocol, not just http:// and ftp://

Revision 1.7  2002/10/22 16:43:55  rubys
textInput vs textinput: don't reject valid 1.0 feeds, but don't allow
invalid textinput fields in RSS 2.0 either...

Revision 1.6  2002/10/18 15:41:33  f8dy
added (and passed) testcases for unallowed duplicates of the same element

Revision 1.5  2002/10/18 13:06:57  f8dy
added licensing information

"""
