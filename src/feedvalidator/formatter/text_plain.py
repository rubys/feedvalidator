"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

"""Output class for plain text output"""

from base import BaseFormatter
import feedvalidator

class Formatter(BaseFormatter):
  def format(self, event):
    return '%s %s%s' % (self.getLineAndColumn(event), self.getMessage(event),
      self.getCount(event))

__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:17  rubys
Initial revision

Revision 1.7  2003/12/12 15:53:42  f8dy
renamed source directories

Revision 1.6  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.5  2002/10/18 13:06:57  f8dy
added licensing information

"""
