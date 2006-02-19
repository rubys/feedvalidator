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
class textConstruct(validatorBase,rfc2396,nonhtml):
  from validators import mime_re
  import re

  def getExpectedAttrNames(self):
      return [(None, u'type'),(None, u'src')]

  def maptype(self):
    if self.type.find('/') > -1:
      self.log(InvalidTextType({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))

  def prevalidate(self):
    if self.attrs.has_key((None,"src")):
      self.type=''
    else:
      self.type='text'

    if self.attrs.has_key((None,"type")):
      self.type=self.attrs.getValue((None,"type"))
      if not self.type:
        self.log(AttrNotBlank({"parent":self.parent.name, "element":self.name, "attr":"type"}))

    self.maptype()

    if self.attrs.has_key((None,"src")):
      self.children.append(True) # force warnings about "mixed" content
      self.value=self.attrs.getValue((None,"src"))
      rfc2396.validate(self, errorClass=InvalidURIAttribute, extraParams={"attr": "src"})
      self.value=""

      if not self.attrs.has_key((None,"type")):
        self.log(MissingTypeAttr({"parent":self.parent.name, "element":self.name, "attr":"type"}))

    if self.type in ['text','html','xhtml'] and not self.attrs.has_key((None,"src")):
      pass
    elif self.type and not self.mime_re.match(self.type):
      self.log(InvalidMIMEType({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))
    else:
      self.log(ValidMIMEAttribute({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))
    
    if not self.xmlLang:
      self.log(MissingDCLanguage({"parent":self.name, "element":"xml:lang"}))

  def validate(self):
    if self.type in ['text','xhtml']:
      if self.type=='xhtml':
        nonhtml.validate(self, NotInline)
      else:
        nonhtml.validate(self, ContainsUndeclaredHTML)
    else:
      if self.type.find('/') > -1 and not (
         self.type.endswith('+xml') or self.type.endswith('/xml') or
         self.type.startswith('text/')):
        import base64
        try:
          self.value=base64.decodestring(self.value)
          if self.type.endswith('/html'): self.type='html'
        except:
          self.log(NotBase64({"parent":self.parent.name, "element":self.name,"value":self.value}))

      if self.type=='html' or self.type.endswith("/html"):
        self.validateSafe(self.value)

        if self.type.endswith("/html"):
          if self.value.find("<html")<0 and not self.attrs.has_key((None,"src")):
            self.log(HtmlFragment({"parent":self.parent.name, "element":self.name,"value":self.value, "type":self.type}))
      else:
        nonhtml.validate(self, ContainsUndeclaredHTML)

    if not self.value and len(self.children)==0 and not self.attrs.has_key((None,"src")):
       self.log(NotBlank({"parent":self.parent.name, "element":self.name}))

  def textOK(self):
    if self.children: validatorBase.textOK(self)

  def characters(self, string):
    if (self.type=='xhtml') and string.strip() and not self.value.strip():
      self.log(MissingXhtmlDiv({"parent":self.parent.name, "element":self.name}))
    validatorBase.characters(self,string)

  def startElementNS(self, name, qname, attrs):
    if (self.type<>'xhtml') and not (
        self.type.endswith('+xml') or self.type.endswith('/xml')):
      self.log(UndefinedElement({"parent":self.name, "element":name}))

    if self.type=="xhtml":
      if name<>'div' and not self.value.strip():
        self.log(MissingXhtmlDiv({"parent":self.parent.name, "element":self.name}))
      elif qname not in ["","http://www.w3.org/1999/xhtml"]:
        self.log(NotHtml({"parent":self.parent.name, "element":self.name, "message":"unexpected namespace: %s" % qname}))

    if self.type=="application/xhtml+xml":
      if name<>'html':
        self.log(HtmlFragment({"parent":self.parent.name, "element":self.name,"value":self.value, "type":self.type}))
      elif qname not in ["","http://www.w3.org/1999/xhtml"]:
        self.log(NotHtml({"parent":self.parent.name, "element":self.name, "message":"unexpected namespace: %s" % qname}))

    if self.attrs.has_key((None,"mode")):
      if self.attrs.getValue((None,"mode")) == 'escaped':
        self.log(NotEscaped({"parent":self.parent.name, "element":self.name}))

    if name=="div" and qname=="http://www.w3.org/1999/xhtml":
      handler=diveater()
    else:
      handler=eater()
    self.children.append(handler)
    self.push(handler, name, attrs)

# treat xhtml:div as part of the content for purposes of detecting escaped html
class diveater(eater):
  def __init__(self):
    eater.__init__(self)
    self.mixed = False
  def textOK(self):
    pass
  def characters(self, string):
    validatorBase.characters(self, string)
  def startElementNS(self, name, qname, attrs):
    self.mixed = True
    eater.startElementNS(self, name, qname, attrs)
  def validate(self):
    if not self.mixed: self.parent.value += self.value

class content(textConstruct):
  def maptype(self):
    if self.type == 'multipart/alternative':
      self.log(InvalidMIMEType({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))

__history__ = """
$Log$
Revision 1.27  2006/02/19 13:57:00  rubys
"The description must be suitable for presentation as HTML"

Revision 1.26  2006/01/02 01:28:51  rubys
More dead code

Revision 1.25  2006/01/02 01:26:18  rubys
Remove vestigial Atom 0.3 support

Revision 1.24  2005/12/27 17:17:09  rubys
Better checking and message for inline html

Revision 1.23  2005/12/19 18:01:20  rubys
Expand checking for unexpected text

Revision 1.22  2005/11/10 13:24:01  rubys
Flag CDATA escaped xhtml content

Revision 1.21  2005/11/08 18:27:42  rubys
Warn on missing language, itunes:explicit, or itunes:category if any itunes
elements are present.

Revision 1.20  2005/09/15 21:42:13  rubys
Fix remote text/html incorrectly being reported as a fragment,
reported by Alex Blewitt

Revision 1.19  2005/08/20 03:58:58  rubys
white-space + xml:base

Revision 1.18  2005/07/28 15:25:12  rubys
Warn on use of html mime types containing fragments

Revision 1.17  2005/07/25 00:40:54  rubys
Convert errors to warnings

Revision 1.16  2005/07/23 00:27:06  rubys
More cleanup

Revision 1.15  2005/07/19 19:57:45  rubys
Few things I spotted...

Revision 1.14  2005/07/18 18:53:29  rubys
Atom 1.0 section 4.1.3

Revision 1.13  2005/07/17 23:22:44  rubys
Atom 1.0 section 4.1.1.1

Revision 1.12  2005/07/17 03:12:26  rubys
Complete Atom 1.0 section 3

Revision 1.11  2005/07/16 22:01:14  rubys
Atom 1.0 text constructs and relative URIs

Revision 1.10  2005/07/16 14:40:09  rubys
More Atom 1.0 support

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
