__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"

from .logging import *

def _must(event):
  return isinstance(event, Error)

def _should(event):
  return isinstance(event, Warning)

def _may(event):
  return isinstance(event, Info)

def A(events):
  return [event for event in events if _must(event)]

def AA(events):
  return [event for event in events if _must(event) or _should(event)]

def AAA(events):
  return [event for event in events if _must(event) or _should(event) or _may(event)]

def AAAA(events):
  return events

def analyze(events, rawdata):
  block = rawdata[0:512].strip().upper()
  if block.startswith('<HTML'): return 'html'
  if block.startswith('<!DOCTYPE HTML'): return 'html'

  for event in events:
    if isinstance(event,UndefinedElement):
      if event.params['parent'] == 'root':
        if event.params['element'].lower() in ['html','xhtml:html']:
          return "html"
  return None
