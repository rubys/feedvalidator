"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from logging import *
from validators import rdfAbout, noduplicates, text, eater
from root import rss11_namespace as rss11_ns
from extension import extension

rdfNS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

#
# rdf:RDF element.  The valid children include "channel", "item", "textinput", "image"
#
class rdf(validatorBase,object):

  def do_rss090_channel(self):
    from channel import channel
    self.defaultNamespaces.append("http://my.netscape.com/rdf/simple/0.9/")
    return channel(), noduplicates()

  def do_channel(self):
    from channel import rss10Channel
    return rdfAbout(), rss10Channel(), noduplicates()

  def _is_090(self):
    return "http://my.netscape.com/rdf/simple/0.9/" in self.defaultNamespaces

  def _withAbout(self,v):
    if self._is_090():
      return v
    else:
      return v, rdfAbout()
      
  def do_item(self):
    from item import rss10Item
    return self._withAbout(rss10Item())

  def do_textinput(self):
    from textInput import textInput
    return self._withAbout(textInput())

  def do_image(self):
    return self._withAbout(rss10Image())
  
  def do_cc_License(self):
    return eater()

  def do_taxo_topic(self):
    return eater()

  def prevalidate(self):
    self.setFeedType(TYPE_RSS1)
    
  def validate(self):
    if not "channel" in self.children and not "rss090_channel" in self.children:
      self.log(MissingChannel({"parent":self.name, "element":"channel"}))

from validators import rfc2396_full

class rss10Image(validatorBase, extension):
  def validate(self):
    if not "title" in self.children:
      self.log(MissingTitle({"parent":self.name, "element":"title"}))
    if not "link" in self.children:
      self.log(MissingLink({"parent":self.name, "element":"link"}))
    if not "url" in self.children:
      self.log(MissingElement({"parent":self.name, "element":"url"}))

  def do_title(self):
    from image import title
    return title(), noduplicates()

  def do_link(self):
    return rfc2396_full(), noduplicates()

  def do_url(self):
    return rfc2396_full(), noduplicates()

  def do_dc_creator(self):
    return text()

  def do_dc_subject(self):
    return text() # duplicates allowed

  def do_dc_date(self):
    from validators import w3cdtf
    return w3cdtf(), noduplicates()

  def do_cc_license(self):
    return eater()

#
# This class performs RSS 1.x specific validations on extensions.
#
class rdfExtension(validatorBase):
  def __init__(self, parent, name, qname, attrs, literal=False):
    validatorBase.__init__(self)
    self.name=name
    self.parent=parent
    self.dispatcher=parent.dispatcher
    self.attrs=attrs
    self.literal=literal

    if attrs.has_key((rdfNS,"parseType")):
      if attrs[(rdfNS,"parseType")] == "Literal": self.literal=True

    if not self.literal:

      # ensure no rss11 children
      if qname==rss11_ns:
        from logging import UndefinedElement
        self.log(UndefinedElement({"parent":parent.name, "element":name}))

      # no duplicate rdf:abouts
      if attrs.has_key((rdfNS,"about")):
        about = attrs[(rdfNS,"about")]
        if not "abouts" in self.dispatcher.__dict__:
          self.dispatcher.__dict__["abouts"] = []
        if about in self.dispatcher.__dict__["abouts"]:
          self.log(DuplicateValue(
            {"parent":parent.name, "element":"rdf:about", "value":about}))
        else:
          self.dispatcher.__dict__["abouts"].append(about)

  def getExpectedAttrNames(self):
    # no rss11 attributes
    if self.literal or not self.attrs: return self.attrs.keys()
    return [(ns,n) for ns,n in self.attrs.keys() if ns!=rss11_ns]

  def validate(self):
    # rdflib 2.0.5 does not catch mixed content errors
    if self.value.strip() and self.children and not self.literal:
      self.log(InvalidRDF({"message":"mixed content"}))

  def startElementNS(self, name, qname, attrs):
    # ensure element is "namespace well formed"
    if name.find(':') != -1:
      from logging import MissingNamespace
      self.log(MissingNamespace({"parent":self.name, "element":name}))

    # ensure all attribute namespaces are properly defined
    for (namespace,attr) in attrs.keys():
      if ':' in attr and not namespace:
        from logging import MissingNamespace
        self.log(MissingNamespace({"parent":self.name, "element":attr}))

    # eat children
    self.children.append((qname,name))
    self.push(rdfExtension(self, name, qname, attrs, self.literal))

  def characters(self, string):
    if not self.literal: validatorBase.characters(self, string)

__history__ = """
$Log$
Revision 1.14  2005/07/05 16:07:02  philor
Minimal mod_taxonomy support

Revision 1.13  2005/07/04 22:54:31  philor
Support rest of dc, dcterms, geo, geourl, icbm, and refactor out common extension elements

Revision 1.12  2005/06/29 23:53:56  rubys
Fixes:
  channel level dc:subject and foaf:maker
  item level dc:language and rdfs:seeAlso
  rdf:RDF level cc:License

Revision 1.11  2005/01/28 14:43:38  rubys
Avoid spurious errors in Literal content

Revision 1.10  2005/01/28 00:06:25  josephw
Use separate 'item' and 'channel' classes to reject RSS 2.0 elements in
 RSS 1.0 feeds (closes 1037785).

Revision 1.9  2005/01/27 11:43:58  rubys
Add back in RDF specific extensibility checks.  In particular, validate
that mixed content is not present (except for rdf:parseType="Literal")
as rdflib 2.0.5 apparently does not make this check.

Revision 1.8  2005/01/27 01:09:25  josephw
Don't allow RSS 2.0 elements in RSS 1.0 image elements.

Revision 1.7  2005/01/26 17:54:34  rubys
Remove hacky rdf validation - this will temporarily make two RSS 1.1 tests
fail.  Better fix based on rdflib forthcoming.

Revision 1.6  2005/01/25 22:39:50  josephw
Require rdf:about for RSS 1.0 image, and all second-level elements.

Revision 1.5  2005/01/22 23:45:36  rubys
pass last rss11 test case (neg-ext-notrdf.xml)

Revision 1.4  2005/01/21 13:52:54  rubys
Better fix for Mozilla bug 279202

Revision 1.2  2004/06/28 23:34:46  rubys
Support RSS 0.90

Revision 1.1.1.1  2004/02/03 17:33:16  rubys
Initial import.

Revision 1.10  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.9  2003/10/16 15:54:41  rubys
Detect duplicate channels

Revision 1.8  2003/08/12 00:26:30  rubys
Misleading error message if a channel is missing in an RSS 1.0 feed

Revision 1.7  2003/08/10 13:49:14  rubys
Add support for chanel and item level rdf:about.  Ensure that http and
ftp URLs have exactly two slashes after the scheme.

Revision 1.6  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.5  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.4  2002/10/22 14:11:36  f8dy
initial attempts to handle RSS 1.0 vs. 2.0 images and textinputs; test
cases still fail

Revision 1.3  2002/10/22 13:16:03  f8dy
passed lowercase textinput test

Revision 1.2  2002/10/18 13:06:57  f8dy
added licensing information

"""
