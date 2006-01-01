"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import text
from logging import *

#
# skipHours element
#
class skipHours(validatorBase):
    
  def validate(self):
    if "hour" not in self.children:
      self.log(MissingElement({"parent":self.name, "element":"hour"}))
    if len(self.children) > 24:
      self.log(NotEnoughHoursInTheDay({}))

  def do_hour(self):
    return hour()

class hour(text):
  def validate(self):
    try:
      h = int(self.value)
      if (h < 0) or (h > 24):
        raise ValueError
      else:
        self.log(ValidHour({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidHour({"parent":self.parent.name, "element":self.name, "value":self.value}))

__history__ = """
$Log$
Revision 1.3  2006/01/01 17:17:18  rubys
Eliminate several unexpected "UnexpectedText" errors

Revision 1.2  2004/07/28 02:23:41  rubys
Remove some experimental rules

Revision 1.1.1.1  2004/02/03 17:33:16  rubys
Initial import.

Revision 1.6  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.5  2003/07/30 01:54:59  f8dy
tighten test cases, add explicit params

Revision 1.4  2003/07/29 20:57:39  f8dy
tightened up test cases, check for parent element, explicitly test for success

Revision 1.3  2002/11/11 19:12:17  rubys
Allow zero for hours

Revision 1.2  2002/10/18 13:06:57  f8dy
added licensing information

"""
