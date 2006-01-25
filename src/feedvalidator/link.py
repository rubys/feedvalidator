"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *

#
# Atom link element
#
class link(nonblank,xmlbase,iso639,nonhtml,positiveInteger,nonblank):
  validRelations = ['alternate', 'enclosure', 'related', 'self', 'via',
    "previous", "next", "first", "last", "current", "payment"]
    # http://www.imc.org/atom-protocol/mail-archive/msg04095.html

  def getExpectedAttrNames(self):
    return [(None, u'type'), (None, u'title'), (None, u'rel'), (None, u'href'), (None, u'length'), (None, u'hreflang'), (u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'type'), (u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'resource')]
	      
  def validate(self):
    self.type = ""
    self.rel = "alternate"
    self.hreflang = ""
    self.title = ""

    if self.attrs.has_key((None, "rel")):
      self.value = self.rel = self.attrs.getValue((None, "rel"))
      if self.rel in self.validRelations: 
        self.log(ValidAtomLinkRel({"parent":self.parent.name, "element":self.name, "attr":"rel", "value":self.rel}))
      elif rfc2396_full.rfc2396_re.match(self.rel):
        self.log(ValidAtomLinkRel({"parent":self.parent.name, "element":self.name, "attr":"rel", "value":self.rel}))
      else:
        self.log(InvalidAtomLinkRel({"parent":self.parent.name, "element":self.name, "attr":"rel", "value":self.rel}))
      nonblank.validate(self, errorClass=AttrNotBlank, extraParams={"attr": "rel"})

    if self.attrs.has_key((None, "type")):
      self.value = self.type = self.attrs.getValue((None, "type"))
      if not mime_re.match(self.type):
        self.log(InvalidMIMEType({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))
      else:
        self.log(ValidMIMEAttribute({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))

    if self.attrs.has_key((None, "title")):
      self.log(ValidTitle({"parent":self.parent.name, "element":self.name, "attr":"title"}))
      self.value = self.title = self.attrs.getValue((None, "title"))
      nonblank.validate(self, errorClass=AttrNotBlank, extraParams={"attr": "title"})
      nonhtml.validate(self)

    if self.attrs.has_key((None, "length")):
      self.value = self.hreflang = self.attrs.getValue((None, "length"))
      positiveInteger.validate(self)
      nonblank.validate(self)

    if self.attrs.has_key((None, "hreflang")):
      self.value = self.hreflang = self.attrs.getValue((None, "hreflang"))
      iso639.validate(self)

    if self.attrs.has_key((None, "href")):
      self.value = self.attrs.getValue((None, "href"))
      xmlbase.validate(self, extraParams={"attr": "href"})

      if self.rel == "self" and self.parent.name == "feed":
        from urlparse import urljoin
        if urljoin(self.xmlBase,self.value) not in self.dispatcher.selfURIs:
          if urljoin(self.xmlBase,self.value).split('#')[0] != self.xmlBase.split('#')[0]:
            self.log(SelfDoesntMatchLocation({"parent":self.parent.name, "element":self.name}))

    else:
      self.log(MissingHref({"parent":self.parent.name, "element":self.name, "attr":"href"}))

  def startElementNS(self, name, qname, attrs):
    self.push(eater(), name, attrs)

  def characters(self, text):
    if text.strip():
      self.log(AtomLinkNotEmpty({"parent":self.parent.name, "element":self.name}))
    
__history__ = """
$Log$
Revision 1.23  2006/01/25 19:38:39  rubys
Additional LinkRelations approved by the IESG

Revision 1.22  2006/01/02 01:26:18  rubys
Remove vestigial Atom 0.3 support

Revision 1.21  2005/11/20 00:36:00  rubys
Initial support for gbase namespace

Revision 1.20  2005/08/28 18:58:00  rubys
Don't issue a warning if content-negotiation presents an alias

Revision 1.19  2005/08/20 18:46:35  rubys
Don't issue both "Same-document reference" and "Self reference doesn't match
document location" on the same link.

Revision 1.18  2005/08/20 17:04:43  rubys
check rel="self": fix bug 1255184

Revision 1.17  2005/08/20 03:58:58  rubys
white-space + xml:base

Revision 1.16  2005/07/21 14:19:53  rubys
unregistered Atom 1.0 link rel

Revision 1.15  2005/07/19 13:12:43  rubys
Complete basic coverage for Atom 1.0

Revision 1.14  2005/07/18 10:14:48  rubys
Warn on same document references

Revision 1.13  2005/07/17 23:56:04  rubys
link extensions

Revision 1.12  2005/07/17 18:49:18  rubys
Atom 1.0 section 4.1

Revision 1.11  2005/07/16 22:01:14  rubys
Atom 1.0 text constructs and relative URIs

Revision 1.10  2005/07/16 01:14:12  rubys
Fix for James Snell

Revision 1.9  2005/07/15 11:17:24  rubys
Baby steps towards Atom 1.0 support

Revision 1.8  2005/06/29 17:33:29  rubys
Fix for bug 1229805

Revision 1.7  2004/05/26 18:36:49  f8dy
added test cases for link rel="related", rel="via", and rel="parent"

Revision 1.6  2004/03/05 13:54:03  rubys
Report missing link attributes on the start of the element instead on the end.
Example: testcases/atom/must/entry_link_not_empty.xml

Revision 1.5  2004/02/17 22:42:02  rubys
Remove dependence on Python 2.3

Revision 1.4  2004/02/17 01:25:12  rubys
Resynch with http://intertwingly.net/wiki/pie/LinkTagMeaning

Revision 1.3  2004/02/16 20:24:00  rubys
Fix for bug 892843: FeedValidator allows arbitrary Atom link rel values

Revision 1.2  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.1.1.1  2004/02/03 17:33:16  rubys
Initial import.

Revision 1.5  2003/12/12 15:00:22  f8dy
changed blank link attribute tests to new error AttrNotBlank to distinguish them from elements that can not be blank

Revision 1.4  2003/12/12 11:25:56  rubys
Validate mime type in link tags

Revision 1.3  2003/12/12 06:24:05  rubys
link type validation

Revision 1.2  2003/12/12 06:10:58  rubys
link rel/type checking

Revision 1.1  2003/12/12 05:42:05  rubys
Rough in some support for the new link syntax


"""
