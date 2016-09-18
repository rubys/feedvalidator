__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"

"""Output class for plain text output"""

from .base import BaseFormatter
import feedvalidator

class Formatter(BaseFormatter):
  def format(self, event):
    return '%s %s%s' % (self.getLineAndColumn(event), self.getMessage(event),
      self.getCount(event))
