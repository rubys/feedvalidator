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
  if _count(events, UndefinedElement) and rawdata.count('<html'):
    return "html"
  return None
