"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from logging import *

def _must(event):
  return isinstance(event, Error)

def _should(event):
  return isinstance(event, Warning)

def _may(event):
  return isinstance(event, Info)

def _count(events, eventclass):
  return len([e for e in events if isinstance(e, eventclass)])

def A(events):
  return [event for event in events if _must(event)]

def AA(events):
  return [event for event in events if _must(event) or _should(event)]

def AAA(events):
  return [event for event in events if _must(event) or _should(event) or _may(event)]

def AAAA(events):
  return events

def analyze(events, rawdata):
  if _count(events, InvalidContact) and \
     (_count(events, InvalidRFC2822Date) > 1):
    return "oldmt"
  if _count(events, UndefinedElement) and rawdata.count('<html'):
    return "html"
  return None

__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:14  rubys
Initial revision

Revision 1.6  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.5  2003/08/03 18:46:04  rubys
support author(url,email) and feed(author,copyright,generator)

Revision 1.4  2002/10/22 02:18:33  f8dy
added RSS autodiscovery support

Revision 1.3  2002/10/19 21:08:02  f8dy
added "special case" functionality for the web front end

Revision 1.2  2002/10/18 13:06:57  f8dy
added licensing information

"""
