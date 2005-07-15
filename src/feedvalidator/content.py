"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *
from logging import *

#
# item element.
#
class content(validatorBase,safeHtmlMixin):
  from validators import mime_re
  htmlEndTag_re = re.compile("</\w+>")
  HTMLTYPES = ('text/html', 'application/xhtml+xml')

  def getExpectedAttrNames(self):
      return [(None, u'type')]

  def prevalidate(self):
    self.mode='xml'
    self.type='text/plain'
    self.mixed=0
    self.multitypes=[]
    if self.attrs.has_key((None,"mode")):
      self.mode=self.attrs.getValue((None,"mode"))
    if self.attrs.has_key((None,"type")):
      self.type=self.attrs.getValue((None,"type"))

    if not self.mode in ['xml','escaped','base64']:
      self.log(InvalidContentMode({"parent":self.parent.name, "element":self.name, "mode":self.mode}))
    else:
      self.log(ValidContentMode({"parent":self.parent.name, "element":self.name, "mode":self.mode}))

    if self.type == 'text':
      self.mode = 'xml'
    elif self.type == 'html':
      self.type = 'text/html'
      self.mode = 'escaped'
    elif self.type == 'xhtml':
      self.mode = 'xml'
    elif not self.mime_re.match(self.type):
      self.log(InvalidMIMEType({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))
    else:
      self.log(ValidMIMEAttribute({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))
    
    if not self.dispatcher.xmlLang:
      self.log(MissingDCLanguage({"parent":self.name, "element":"xml:lang"}))

  def validate(self):
    if self.mode == 'xml':
      import re
      if self.htmlEndTag_re.search(self.value):
        if self.type in self.HTMLTYPES:
          self.log(NotInline({"parent":self.parent.name, "element":self.name,"value":self.value}))
        else:
          self.log(ContainsUndeclaredHTML({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      if self.mode == 'base64':
        import base64
        try:
          self.value=base64.decodestring(self.value)
        except:
          self.log(NotBase64({"parent":self.parent.name, "element":self.name,"value":self.value}))

      if self.type in self.HTMLTYPES:
        self.validateSafe(self.value)
        from HTMLParser import HTMLParser, HTMLParseError

        try:
          p=HTMLParser()
          p.feed(self.value)
          p.close()
          self.log(ValidHtml({"parent":self.parent.name, "element":self.name,"value":self.value}))
        except HTMLParseError:
          import sys
          self.log(NotHtml({"parent":self.parent.name, "element":self.name,"value":self.value, "message": sys.exc_info()[1].msg}))
      else:
        if self.htmlEndTag_re.search(self.value):
          self.log(ContainsUndeclaredHTML({"parent":self.parent.name, "element":self.name, "value":self.value}))

    if self.type == 'multipart/alternative':
      if len(self.children)==0:
        self.log(MultipartMissing({"parent":self.parent.name, "element":self.name}))

  def startElementNS(self, name, qname, attrs):
    if (self.type=='text/plain') or (self.mode <> 'xml'):
      self.log(UndefinedElement({"parent":self.name, "element":name}))
    if self.type in self.HTMLTYPES:
      if qname not in ["","http://www.w3.org/1999/xhtml"]:
        self.log(NotHtml({"parent":self.parent.name, "element":self.name, "message":"unexpected namespace: %s" % qname}))
    if self.type == 'multipart/alternative':
      if name<>'content':
        self.log(MultipartInvalid({"parent":self.parent.name, "element":self.name, "name":name}))
      else:
        validatorBase.startElementNS(self, name, qname, attrs)
        if attrs.has_key((None,'type')):
          type=attrs.getValue((None,'type'))
          if type=='multipart/alternative':
            self.log(MultipartRecursion({"parent":self.parent.name, "element":self.name, "name":name}))
          if type in self.multitypes:
            self.log(MultipartDuplicate({"parent":self.parent.name, "element":self.name, "type":type}))
          else:
            self.multitypes += [type]
        return

    self.mixed=1
    if self.attrs.has_key((None,"mode")):
      if self.attrs.getValue((None,"mode")) == 'escaped':
        self.log(NotEscaped({"parent":self.parent.name, "element":self.name}))
    handler=eater()
    handler.parent=self
    handler.dispatcher=self
    handler.attrs=attrs
    self.push(handler)

class pie_content(content):

  def getExpectedAttrNames(self):
      return [(None, u'type'), (None, u'mode')]

  def do_content(self):
    return pie_content()

__history__ = """
$Log$
Revision 1.9  2005/07/15 11:17:24  rubys
Baby steps towards Atom 1.0 support

Revision 1.8  2004/07/28 12:24:25  rubys
Partial support for verifing xml:lang

Revision 1.7  2004/07/17 21:47:53  rubys
Fix for bug 975199: check summary content type

Revision 1.6  2004/07/17 12:37:30  rubys
Detect content declared as xhtml but not placed in the xhtml namespace

Revision 1.5  2004/02/18 14:30:50  rubys
Don't flag attributes in content with mode="xml"

Revision 1.4  2004/02/17 22:42:02  rubys
Remove dependence on Python 2.3

Revision 1.3  2004/02/17 02:03:06  rubys
Fix for bug 892199: malicious tags within base64 content

Revision 1.2  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.1.1.1  2004/02/03 17:33:15  rubys
Initial import.

Revision 1.14  2003/12/12 11:25:55  rubys
Validate mime type in link tags

Revision 1.13  2003/12/12 01:24:36  rubys
Multipart/alternative tests

Revision 1.12  2003/12/11 18:20:46  f8dy
passed all content-related testcases

Revision 1.11  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.10  2003/12/11 15:18:51  f8dy
type is now optional

Revision 1.9  2003/08/23 21:01:00  rubys
Validate that content, content:encoded, and xhtml:body are safe

Revision 1.8  2003/08/23 00:28:04  rubys
Validate escaped text/HTML content

Revision 1.7  2003/08/05 15:03:19  rubys
Handle complex (nested) content.  Remove copy/paste error in handing
of copyright.

Revision 1.6  2003/07/29 21:48:10  f8dy
tightened up test cases, added parent element check, changed negative test cases to positive

Revision 1.5  2003/07/11 16:36:08  rubys
Attempt to detect improper use of inline xml

Revision 1.4  2003/07/10 21:16:33  rubys
Get rssdemo back on its feet...

Revision 1.3  2003/07/10 21:02:16  rubys
Verify base64 and escaped

Revision 1.2  2003/07/07 10:35:50  rubys
Complete first pass of echo/pie tests

Revision 1.1  2003/07/07 02:44:13  rubys
Further progress towards pie

"""
