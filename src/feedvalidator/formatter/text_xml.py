"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

"""Output class for xml output"""

from base import BaseFormatter
from feedvalidator.logging import *
import feedvalidator

def xmlEncode(value):
  value = value.replace('&', '&amp;')
  value = value.replace('<', '&lt;')
  value = value.replace('>', '&gt;')
  value = value.replace('"', '&quot;')
  value = value.replace("'", '&apos;')
  return value

class Formatter(BaseFormatter):
  def format(self, event):
    params = event.params

    params['type'] = event.__class__.__name__
    params['text'] = self.getMessage(event)

    # determine the level of severity
    level = 'unknown'
    if isinstance(event,Info): level = 'info'
    if isinstance(event,Warning): level = 'warning'
    if isinstance(event,Error): level = 'error'
    params['level'] = level

    # organize fixed elements into a known order
    order = params.keys()
    order.sort()
    for key in ['msgcount', 'text', 'column', 'line', 'type', 'level']:
      if key in order:
        order.remove(key)
        order.insert(0,key)

    # output the elements
    result = "<message>\n"
    for key in order:
      value = xmlEncode(str(params[key]))

      result = result + ("  <%s>%s</%s>\n" % (key, value, key))
    result = result + "</message>\n"

    return result
  
__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:17  rubys
Initial revision

Revision 1.5  2003/12/12 15:53:42  f8dy
renamed source directories

Revision 1.4  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.3  2002/10/18 13:06:57  f8dy
added licensing information

"""
