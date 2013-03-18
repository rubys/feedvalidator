__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"

from .base import validatorBase
from .validators import text
from .logging import *

#
# skipDays element
#
class skipDays(validatorBase):

  def __init__(self):
    self.days = []
    validatorBase.__init__(self)

  def validate(self):
    if "day" not in self.children:
      self.log(MissingElement({"parent":self.name, "element":"day"}))
    if len(self.children) > 7:
      self.log(EightDaysAWeek({}))

  def do_day(self):
    return day()

class day(text):
  def validate(self):
    if self.value not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
      self.log(InvalidDay({"parent":self.parent.name, "element":self.name, "value":self.value}))
    elif self.value in self.parent.days:
      self.log(DuplicateValue({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      self.parent.days.append(self.value)
      self.log(ValidDay({"parent":self.parent.name, "element":self.name, "value":self.value}))
