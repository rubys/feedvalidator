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
class generator(rfc2396):
  def validate(self):
    if self.attrs.has_key((None, "url")):
      self.value = self.attrs.getValue((None, "url"))
      rfc2396.validate(self, extraParams={"attr": "url"})
    
__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:15  rubys
Initial revision

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
