"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

"""Output class for HTML text output"""

from base import BaseFormatter
import feedvalidator
from xml.sax.saxutils import escape

from feedvalidator.logging import Info, Warning, Error

from config import DOCSURL

def escapeAndMark(x):
  html = escape(x)

  # Double-escape, and highlight, illegal characters.
  for i in range(len(html)-1,-1,-1):
    c = ord(html[i])
    if 0x80 <= c <= 0x9F or c == 0xfffd:
      if c == 0xfffd:
        e = '?'
      else:
        e = '\\x%02x' % (c)
      html = '%s<span class="badOctet">%s</span>%s' % (html[:i], e, html[i+1:])

  return html

class Formatter(BaseFormatter):
  FRAGMENTLEN = 80
 
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
    return DOCSURL + '/' + rootClass + '/' + messageClass
    
  def mostSeriousClass(self):
    ms=0
    for event in self.data:
      level = -1
      if isinstance(event,Info): level = 1
      if isinstance(event,Warning): level = 2
      if isinstance(event,Error): level = 3
      ms = max(ms, level)
    return [None, Info, Warning, Error][ms]
      
  def header(self):
    return '<ul>'

  def footer(self):
    return '</ul>'

  def format(self, event):
    if event.params.has_key('line'):
      line = event.params['line']
      if line >= len(self.rawdata.split('\n')):
        # For some odd reason, UnicodeErrors tend to trigger a bug
        # in the SAX parser that misrepresents the current line number.
        # We try to capture the last known good line number/column as
        # we go along, and now it's time to fall back to that.
        line = event.params['line'] = event.params.get('backupline',0)
        column = event.params['column'] = event.params.get('backupcolumn',0)
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
      line = None
      markerColumn = None

    html = escapeAndMark(codeFragment)

    rc = u'<li><p>'
    if line:
      rc += u'''<a href="#l%s">''' % line
      rc += u'''%s</a>, ''' % self.getLine(event)
      rc += u'''%s: ''' % self.getColumn(event)
    rc += u'''<span class="message">%s</span>''' % escape(self.getMessage(event))
    rc += u'''%s ''' % self.getCount(event)
    rc += u'''[<a title="more information about this error" href="%s.html">help</a>]</p>''' % self.getHelpURL(event)
    rc += u'''<blockquote><pre>''' + html + '''<br />'''
    if markerColumn:
      rc += u'&nbsp;' * (markerColumn - 1)
      rc += u'''<span class="marker">^</span>'''
    rc += u'</pre></blockquote></li>'
    return rc

__history__ = """
$Log$
Revision 1.11  2004/11/24 11:47:03  josephw
Replaced backslash in revision history.

Revision 1.10  2004/11/23 21:31:44  josephw
Use (backslash)xXX, rather than a fake numeric entity, for bad octets in the report.

Revision 1.9  2004/07/09 21:07:06  rubys
Allow aliases of obscure encodings

Revision 1.8  2004/04/30 09:05:15  josephw
Decode Unicode before parsing XML, to cover cases Expat doesn't deal with.
Present the report as UTF-8, to better deal with Unicode feeds.

Revision 1.7  2004/03/30 08:56:37  josephw
Wrap code fragments in <pre>, to keep significant whitespace.

Revision 1.6  2004/03/28 14:07:43  josephw
Put the CSS directory URL in config. Fixed tabs -> spaces.

Revision 1.5  2004/03/28 10:58:07  josephw
Catch and show ValidationFailure in check.cgi. Changed text_html.py
to allow global events, with no specific document location. Moved DOCSURL
into config.py. Moved trivial HTML list-delimiter definitions into
text_html.py.

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
