"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *

#
# author element.
#
class category(validatorBase, rfc2396_full, nonhtml):
  def getExpectedAttrNames(self):
    return [(None,u'term'),(None,u'scheme'),(None,u'label')]

  def prevalidate(self):
    self.children.append(True) # force warnings about "mixed" content

    if not self.attrs.has_key((None,"term")):
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"term"}))

    if self.attrs.has_key((None,"scheme")):
      self.value=self.attrs.getValue((None,"scheme"))
      rfc2396_full.validate(self, extraParams={"element": "scheme"})

    if self.attrs.has_key((None,"label")):
      self.value=self.attrs.getValue((None,"label"))
      nonhtml.validate(self)

__history__ = """
$Log$
Revision 1.4  2005/08/20 03:58:58  rubys
white-space + xml:base

Revision 1.3  2005/08/18 11:49:12  rubys
atom:category/@scheme is supposed to be an IRI, not even an IRI-reference
Thanks to David Powell for noticing this.

Revision 1.2  2005/07/18 23:22:12  rubys
Atom 4.2.2.1, 4.2.4, 4.2.5

Revision 1.1  2005/07/16 14:40:09  rubys
More Atom 1.0 support

Revision 1.3  2005/07/15 11:17:23  rubys
Baby steps towards Atom 1.0 support

Revision 1.2  2004/02/20 15:35:46  rubys
Feature 900555: RSS+Atom support

Revision 1.1.1.1  2004/02/03 17:33:14  rubys
Initial import.

Revision 1.5  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.4  2003/09/01 21:27:48  f8dy
remove weblog, homepage

Revision 1.3  2003/08/03 18:46:04  rubys
support author(url,email) and feed(author,copyright,generator)

Revision 1.2  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.1  2003/07/07 00:54:00  rubys
Rough in some pie/echo support

"""
