"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

"""Output class for plain text output"""

from base import BaseFormatter
import feedvalidator
from xml.sax.saxutils import escape

from feedvalidator.logging import Info, Warning, Error

class Formatter(BaseFormatter):
  FRAGMENTLEN = 80
  DOCSURL = 'docs/'
  
  def __init__(self, events, rawdata):
    BaseFormatter.__init__(self, events)
    self.rawdata = rawdata
    
  def getRootClass(self, aClass):
    base = aClass.__bases__[0]
    if base.__name__.split('.')[-1] == 'LoggedEvent':
      return aClass
    else:
      return self.getRootClass(base)

  def getHelpURL(self, event):
    rootClass = self.getRootClass(event.__class__).__name__
    rootClass = rootClass.split('.')[-1]
    rootClass = rootClass.lower()
#    messageClass = self.getMessageClass(event).__name__.split('.')[-1]
    messageClass = event.__class__.__name__.split('.')[-1]
    return self.DOCSURL + rootClass + '/' + messageClass
    
  def mostSeriousClass(self):
    ms=0
    for event in self.data:
      level = -1
      if isinstance(event,Info): level = 1
      if isinstance(event,Warning): level = 2
      if isinstance(event,Error): level = 3
      ms = max(ms, level)
    return [None, Info, Warning, Error][ms]
      
  def format(self, event):
    if event.params.has_key('line'):
      line = event.params['line']
      if line >= len(self.rawdata.split('\n')):
        # For some odd reason, UnicodeErrors tend to trigger a bug
        # in the SAX parser that misrepresents the current line number.
        # We try to capture the last known good line number/column as
        # we go along, and now it's time to fall back to that.
        line = event.params['line'] = event.params['backupline']
        column = event.params['column'] = event.params['backupcolumn']
      column = event.params['column']
      codeFragment = self.rawdata.split('\n')[line-1]
      markerColumn = column
      if column > self.FRAGMENTLEN:
        codeFragment = '... ' + codeFragment[column-(self.FRAGMENTLEN/2):]
        markerColumn = 5 + (self.FRAGMENTLEN/2)
      if len(codeFragment) > self.FRAGMENTLEN:
        codeFragment = codeFragment[:(self.FRAGMENTLEN-4)] + ' ...'
    else:
      codeFragment = ''

    # convert high bit characters to numeric equivalents
    html=escape(codeFragment)
    for i in range(len(html)-1,-1,-1):
      if ord(html[i])>=128:
	html = '%s&#%d;%s' % (html[:i], ord(html[i]), html[i+1:])

    rc = u'''<li><p><a href="#l%s">''' % line
    rc += u'''%s</a>, ''' % self.getLine(event)
    rc += u'''%s: ''' % self.getColumn(event)
    rc += u'''<span class="message">%s</span>''' % escape(self.getMessage(event))
    rc += u'''%s ''' % self.getCount(event)
    rc += u'''[<a title="more information about this error" href="%s.html">help</a>]</p>''' % self.getHelpURL(event)
    rc += u'''<blockquote><p><code>''' + html + '''<br />'''
    rc += u'&nbsp;' * (markerColumn - 1)
    rc += u'''<span class="marker">^</span></code></p></blockquote></li>'''
    return rc

__history__ = """
$Log$
Revision 1.4  2004/03/26 11:47:22  rubys
Fix for [ 923703 ] CGI should not flag warnings as failure
Committing patch submitted by Joseph Walton - josephw

Revision 1.3  2004/02/07 01:52:07  rubys
Unicode bulletproofing

Revision 1.2  2004/02/04 14:22:24  rubys
Remove the requirement for MultiViews Option

Fix for bug 890200
Patch provided by Ross Karchner

Revision 1.1.1.1  2004/02/03 17:33:17  rubys
Initial import.

Revision 1.14  2003/12/12 15:53:42  f8dy
renamed source directories

Revision 1.13  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.12  2003/09/01 21:28:03  f8dy
changes related to new server

Revision 1.11  2003/09/01 21:20:44  f8dy
changes related to new server

Revision 1.10  2003/06/26 18:03:04  f8dy
add workaround for case where SAX throws UnicodeError but locator.getLineNumber() is screwy

Revision 1.9  2002/10/30 23:03:01  f8dy
security fix: external (SYSTEM) entities

Revision 1.8  2002/10/30 06:07:18  f8dy
version 1.0.5

Revision 1.7  2002/10/18 13:06:57  f8dy
added licensing information

"""
