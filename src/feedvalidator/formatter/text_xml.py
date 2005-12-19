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
    result = "<%s>\n" % level
    for key in order:
      value = xmlEncode(str(params[key]))
      pub_key = key
      if key == "backupcolumn":
        pubkey = "column"
      elif key == "backupline":
        pubkey = "line"
      result = result + ("  <%s>%s</%s>\n" % (key, value, key))
    result = result + "</%s>\n" % level

    return result
  
__history__ = """
$Log$
Revision 1.2  2005/12/19 23:01:21  olivier_t
sending in patch 1368534
https://sourceforge.net/tracker/index.php?func=detail&aid=1368534&group_id=99943&atid=626805

- update the soap template to a soap1.2 format (similar to the one used by markup validator and css validator at w3c)
- (in soap output) group messages by level
- making the soap output available with a simple GET request

Revision 1.1.1.1  2004/02/03 17:33:17  rubys
Initial import.

Revision 1.5  2003/12/12 15:53:42  f8dy
renamed source directories

Revision 1.4  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.3  2002/10/18 13:06:57  f8dy
added licensing information

"""
