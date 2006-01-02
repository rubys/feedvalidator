"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *

#
# Atom generator element
#
class generator(nonhtml,rfc2396):
  def getExpectedAttrNames(self):
    return [(None, u'uri'), (None, u'version')]

  def prevalidate(self):
    if self.attrs.has_key((None, "url")):
      self.value = self.attrs.getValue((None, "url"))
      rfc2396.validate(self, extraParams={"attr": "url"})
    if self.attrs.has_key((None, "uri")):
      self.value = self.attrs.getValue((None, "uri"))
      rfc2396.validate(self, errorClass=InvalidURIAttribute, extraParams={"attr": "uri"})
    self.value=''
    
__history__ = """
$Log$
Revision 1.8  2006/01/02 01:26:18  rubys
Remove vestigial Atom 0.3 support

Revision 1.7  2005/08/20 03:58:58  rubys
white-space + xml:base

Revision 1.6  2005/07/16 22:01:14  rubys
Atom 1.0 text constructs and relative URIs

Revision 1.5  2005/07/15 11:17:24  rubys
Baby steps towards Atom 1.0 support

Revision 1.4  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.3  2004/02/17 22:42:02  rubys
Remove dependence on Python 2.3

Revision 1.2  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.1.1.1  2004/02/03 17:33:15  rubys
Initial import.

Revision 1.3  2003/12/11 23:16:32  f8dy
passed new generator test cases

Revision 1.2  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.1  2003/08/03 22:39:40  rubys
Add generator element

Revision 1.2  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.1  2003/07/07 00:54:00  rubys
Rough in some pie/echo support

"""
