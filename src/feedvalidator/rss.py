"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from logging import *
from validators import noduplicates
from sets import ImmutableSet

#
# Rss element.  The only valid child element is "channel"
#
class rss(validatorBase):
  def do_channel(self):
    from channel import channel
    return channel(), noduplicates()

  def getExpectedAttrNames(self):
    return ImmutableSet([(None, u'version')])

  def prevalidate(self):
    self.setFeedType(TYPE_RSS2) # could be anything in the 0.9x family, don't really care
    
  def validate(self):
    if not "channel" in self.children:
      self.log(MissingChannel({"parent":self.name, "element":"channel"}))
    if (None,'version') not in self.attrs.getNames():
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"version"}))
    elif [e for e in self.dispatcher.loggedEvents if e.__class__==ValidDoctype]:
      if self.attrs[(None,'version')]<>'0.91':
        self.log(InvalidDoctype({"parent":self.parent.name, "element":self.name, "attr":"version"}))


__history__ = """
$Log$
Revision 1.2  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.1.1.1  2004/02/03 17:33:16  rubys
Initial import.

Revision 1.9  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.8  2003/10/16 15:54:41  rubys
Detect duplicate channels

Revision 1.7  2003/08/09 18:32:27  rubys
Only allow NetScape DocType on RSS 0.91 feeds

Revision 1.6  2003/08/09 17:21:01  rubys
Fix misleading message when rss channel is missing

Revision 1.5  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.4  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.3  2002/10/18 13:06:57  f8dy
added licensing information

"""
