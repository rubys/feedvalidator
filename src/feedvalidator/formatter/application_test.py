"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

"""Output class for testing that all output messages are defined properly"""

from base import BaseFormatter
import feedvalidator
import os
LANGUAGE = os.environ.get('LANGUAGE', 'en')
lang = __import__('feedvalidator.i18n.%s' % LANGUAGE, globals(), locals(), LANGUAGE)

class Formatter(BaseFormatter):
  def getMessage(self, event):
    classes = [event.__class__]
    while len(classes):
      if lang.messages.has_key(classes[0]):
        return lang.messages[classes[0]] % event.params
      classes = classes + list(classes[0].__bases__)
      del classes[0]
    return None
    
  def format(self, event):
    """returns the formatted representation of a single event"""
    return self.getMessage(event)

__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:17  rubys
Initial revision

Revision 1.3  2003/12/12 15:53:42  f8dy
renamed source directories

Revision 1.2  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.1  2003/08/05 22:09:24  f8dy
added automated message tester


"""
