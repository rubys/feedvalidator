"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *

validRelations = ['alternate', 'start', 'next', 'prev', 'enclosure',
  'service.edit', 'service.post', 'service.feed',
  'comments', 'related', 'transform', 'icon', 'source', 'via', 'parent', 'self'] #unapproved

#
# Atom link element
#
class link(nonblank,rfc2396,iso639):
  def getExpectedAttrNames(self):
    return [(None, u'type'), (None, u'title'), (None, u'rel'), (None, u'href'), (None, u'length'), (None, u'hreflang')]
	      
  def validate(self):
    self.type = ""
    self.rel = "alternate"
    self.hreflang = ""
    self.title = ""

    if self.attrs.has_key((None, "rel")):
      self.value = self.rel = self.attrs.getValue((None, "rel"))
      if self.rel in validRelations: 
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

    if self.attrs.has_key((None, "hreflang")):
      self.value = self.hreflang = self.attrs.getValue((None, "hreflang"))
      iso639.validate(self)

    if self.attrs.has_key((None, "href")):
      self.value = self.attrs.getValue((None, "href"))
      rfc2396.validate(self, extraParams={"attr": "href"})
    else:
      self.log(MissingHref({"parent":self.parent.name, "element":self.name}))

  def characters(self, text):
    self.log(AtomLinkNotEmpty({"parent":self.parent.name, "element":self.name}))
    
__history__ = """
$Log$
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
