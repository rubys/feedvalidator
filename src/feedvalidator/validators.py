"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from logging import *
import re
from uri import canonicalForm

rdfNS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

#
# Valid mime type
#
mime_re = re.compile('[^\s()<>,;:\\"/[\]?=]+/[^\s()<>,;:\\"/[\]?=]+$')

#
# Extensibility hook: logic varies based on type of feed
#
def any(self, name, qname, attrs):
  if self.getFeedType() != TYPE_RSS1:
    return eater()
  else:
    from rdf import rdfExtension
    return rdfExtension(self, name, qname, attrs)

#
# This class simply eats events.  Useful to prevent cascading of errors
#
class eater(validatorBase):
  def getExpectedAttrNames(self):
    return self.attrs.getNames()

  def startElementNS(self, name, qname, attrs):
    # ensure element is "namespace well formed"
    if name.find(':') != -1:
      from logging import MissingNamespace
      self.log(MissingNamespace({"parent":self.name, "element":name}))

    # ensure all attribute namespaces are properly defined
    for (namespace,attr) in attrs.keys():
      if ':' in attr and not namespace:
        from logging import MissingNamespace
        self.log(MissingNamespace({"parent":self.name, "element":attr}))

    # eat children
    handler=eater()
    handler.name=name
    handler.parent=self
    handler.dispatcher=self.dispatcher
    handler.attrs=attrs
    self.push(handler)

from sgmllib import SGMLParser
class check4evil(SGMLParser):
  evilattrs = ['onabort', 'onblur', 'onchange', 'onclick', 'ondblclick',
                'onerror', 'onfocus', 'onkeydown', 'onkeypress', 'onkeyup',
                'onload', 'onmousedown', 'onmouseout', 'onmouseover',
                 'onmouseup', 'onreset', 'onresize', 'onsubmit', 'onunload']
  def __init__(self,value):
    self.found=[]
    SGMLParser.__init__(self)
    self.feed(value)
    self.close()
  def unknown_starttag(self, tag, attributes):
    for (name,value) in attributes:
      if name.lower() in self.evilattrs: self.found.append(name)

#
# This class simply html events.  Identifies unsafe events
#
class htmlEater(validatorBase):
  def __init__(self,parent,element):
    self.parent=parent
    self.element=element
    validatorBase.__init__(self)
  def getExpectedAttrNames(self):
    if self.attrs and len(self.attrs): 
      return self.attrs.getNames()
  def startElementNS(self, name, qname, attrs):
    for evil in check4evil.evilattrs:
      if attrs.has_key((None,evil)):
        self.log(ContainsScript({"parent":self.parent.name, "element":self.element, "tag":evil}))
    handler=htmlEater(self.parent,self.element)
    handler.parent=self
    handler.dispatcher=self.dispatcher
    handler.attrs=attrs
    self.push(handler)
    if name=='script':
      self.log(ContainsScript({"parent":self.parent.name, "element":self.element, "tag":"script"}))
    if name=='meta':
      self.log(ContainsMeta({"parent":self.parent.name, "element":self.element, "tag":"meta"}))
    if name=='embed':
      self.log(ContainsEmbed({"parent":self.parent.name, "element":self.element, "tag":"embed"}))
    if name=='object':
      self.log(ContainsObject({"parent":self.parent.name, "element":self.element, "tag":"object"}))
#    if name=='a' and attrs.get((None,'href'),':').count(':')==0:
#        self.log(ContainsRelRef({"parent":self.parent.name, "element":self.element}))
#    if name=='img' and attrs.get((None,'src'), ':').count(':')==0:
#        self.log(ContainsRelRef({"parent":self.parent.name, "element":self.element}))
  def endElementNS(self,name,qname):
    pass

#
# text: i.e., no child elements allowed (except rdf:Description).
#
class text(validatorBase):
  def textOK(self): pass
  def getExpectedAttrNames(self):
    if self.getFeedType() == TYPE_RSS1:
      return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'parseType'), 
              (u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'datatype'),
              (u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'resource')]
    else:
      return []
  def startElementNS(self, name, qname, attrs):
    if self.getFeedType() == TYPE_RSS1:
      from rdf import rdfExtension
      self.push(rdfExtension(self, name, qname, attrs))
    else:
      from base import namespaces
      ns = namespaces.get(qname, '')

      if name.find(':') != -1:
        from logging import MissingNamespace
        self.log(MissingNamespace({"parent":self.name, "element":name}))
      else:
        self.log(UndefinedElement({"parent":self.name, "element":name}))

      handler=eater()
      handler.name=name
      handler.parent=self
      handler.dispatcher=self.dispatcher
      handler.attrs=attrs
      self.push(handler)

#
# noduplicates: no child elements, no duplicate siblings
#
class noduplicates(validatorBase):
  def startElementNS(self, name, qname, attrs):
    pass
  def prevalidate(self):
    if self.name in self.parent.children:
      self.log(DuplicateElement({"parent":self.parent.name, "element":self.name}))

#
# valid e-mail addresses
#
class email(text):
#  email_re = re.compile("[\w\-.]+@[\w\-\.]+\s*(\(.*\))?$")
  email_re = re.compile('''([a-zA-Z0-9_\-\+\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$''')
  def validate(self):
    value=self.value
    import rfc822
    list = rfc822.AddressList(self.value)
    if len(list)==1: value=list[0][1]
    if not self.email_re.match(value):
      self.log(InvalidContact({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      self.log(ValidContact({"parent":self.parent.name, "element":self.name, "value":self.value}))

#
# iso639 language code
#
class iso639(text):
  def validate(self):
    import iso639codes
    if '-' in self.value:
      lang, sublang = self.value.split('-', 1)
    else:
      lang = self.value
    if not iso639codes.isoLang.has_key(unicode.lower(unicode(lang))):
      self.log(InvalidLanguage({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      self.log(ValidLanguage({"parent":self.parent.name, "element":self.name}))

#
# iso8601 dateTime
#
class iso8601(text):
  iso8601_re = re.compile("^\d\d\d\d(-\d\d(-\d\d(T\d\d:\d\d(:\d\d(\.\d*)?)?" +
                       "(Z|([+-]\d\d:\d\d))?)?)?)?$")
  def validate(self):
    if not self.iso8601_re.match(self.value):
      self.log(InvalidISO8601Date({"parent":self.parent.name, "element":self.name, "value":self.value}))
      return

    work=self.value.split('T')

    date=work[0].split('-')
    year=int(date[0])
    if len(date)>1:
      month=int(date[1])
      try:
        import calendar
        numdays=calendar.monthrange(year,month)[1]
      except:
        self.log(InvalidW3CDTFDate({"parent":self.parent.name, "element":self.name, "value":self.value}))
        return
    if len(date)>2 and int(date[2])>numdays:
      self.log(InvalidW3CDTFDate({"parent":self.parent.name, "element":self.name, "value":self.value}))
      return

    if len(work) > 1:
      time=work[1].split('Z')[0].split('+')[0].split('-')[0]
      time=time.split(':')
      if int(time[0])>23:
        self.log(InvalidW3CDTFDate({"parent":self.parent.name, "element":self.name, "value":self.value}))
        return
      if len(time)>1 and int(time[1])>60:
        self.log(InvalidW3CDTFDate({"parent":self.parent.name, "element":self.name, "value":self.value}))
        return
      if len(time)>2 and float(time[2])>60.0:
        self.log(InvalidW3CDTFDate({"parent":self.parent.name, "element":self.name, "value":self.value}))
        return

    self.log(ValidW3CDTFDate({"parent":self.parent.name, "element":self.name}))
    return 1

class w3cdtf(iso8601):
  # The same as in iso8601, except a timezone is not optional when
  #  a time is present
  iso8601_re = re.compile("^\d\d\d\d(-\d\d(-\d\d(T\d\d:\d\d(:\d\d(\.\d*)?)?" +
                           "(Z|([+-]\d\d:\d\d)))?)?)?$")

  def validate(self):
    if not self.iso8601_re.search(self.value):
      self.log(InvalidW3CDTFDate({"parent":self.parent.name, "element":self.name
      , "value":self.value}))
      return

    iso8601.validate(self)
    return 1

class iso8601_z(w3cdtf):
  tz_re = re.compile("Z|([+-]\d\d:\d\d)$")
  def validate(self):
    if w3cdtf.validate(self):
      if not self.tz_re.search(self.value):
        self.log(W3CDTFDateNoTimezone({"parent":self.parent.name, "element":self.name, "value":self.value}))
      elif not 'Z' in self.value:
        self.log(W3CDTFDateNonUTC({"parent":self.parent.name, "element":self.name, "value":self.value}))

class iso8601_l(iso8601):
  def validate(self):
    if iso8601.validate(self):
      if 'Z' in self.value:
        self.log(W3CDTFDateNonLocal({"parent":self.parent.name, "element":self.name, "value":self.value}))

iana_schemes = [
  "ftp", "http", "gopher", "mailto", "news", "nntp", "telnet", "wais",
  "file", "prospero", "z39.50s", "z39.50r", "cid", "mid", "vemmi",
  "service", "imap", "nfs", "acap", "rtsp", "tip", "pop", "data", "dav",
  "opaquelocktoken", "sip", "sips", "tel", "fax", "modem", "ldap",
  "https", "soap.beep", "soap.beeps", "xmlrpc.beep", "xmlrpc.beeps",
  "urn", "go", "h323", "ipp", "tftp", "mupdate", "pres", "im", "mtqp"
]

#
# rfc2396 fully qualified (non-relative) uri
#
class rfc2396(text):
  rfc2396_re = re.compile("([a-zA-Z][0-9a-zA-Z+\\-\\.]*:)?/{0,2}" +
    "[0-9a-zA-Z;/?:@&=+$\\.\\-_!~*'()%,#]+$")
  urn_re = re.compile(r"^urn:[a-zA-Z0-9][a-zA-Z0-9-]{1,31}:([a-zA-Z0-9()+,\.:=@;$_!*'\-]|%[0-9A-Fa-f]{2})+$")
  tag_re = re.compile(r"^tag:([a-z0-9\-\._]+?@)?[a-z0-9\.\-]+?,\d{4}(-\d{2}(-\d{2})?)?:[0-9a-zA-Z;/\?:@&=+$\.\-_!~*'\(\)%,]+$")
  def validate(self, errorClass=InvalidLink, successClass=ValidURI, extraParams={}):
    success = 0
    if self.value.startswith('tag:'):
      if self.tag_re.match(self.value):
        success = 1
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(ValidTAG(logparams))
      else:
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(InvalidTAG(logparams))
    elif self.value.startswith('urn:'):
      if self.urn_re.match(self.value):
        success = 1
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(ValidURN(logparams))
      else:
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(InvalidURN(logparams))
    elif (not self.value) or (not self.rfc2396_re.match(self.value)):
      logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
      logparams.update(extraParams)
      self.log(errorClass(logparams))
    elif self.value.startswith('http:') or self.value.startswith('ftp:'):
      if not re.match('^\w+://[^/].*',self.value):
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(errorClass(logparams))
      else:
        success = 1
    elif self.value.split(':')[0] not in iana_schemes:
      logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
      logparams.update(extraParams)
      self.log(errorClass(logparams))
    else:
      success = 1
    if success:
      logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
      logparams.update(extraParams)
      self.log(successClass(logparams))

class rfc2396_full(rfc2396): 
  rfc2396_re = re.compile("[a-zA-Z][0-9a-zA-Z+\\-\\.]*:(//)?" +
    "[0-9a-zA-Z;/?:@&=+$\\.\\-_!~*'()%,#]+$")
  def validate(self, errorClass=InvalidFullLink, successClass=ValidURI, extraParams={}):
    return rfc2396.validate(self, errorClass, successClass, extraParams)

#
# rfc822 dateTime (+Y2K extension)
#
class rfc822(text):
  rfc822_re = re.compile("(((Mon)|(Tue)|(Wed)|(Thu)|(Fri)|(Sat)|(Sun)), *)?" +
    "\d\d? +((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|" +
    "(Nov)|(Dec)) +\d\d(\d\d)? +\d\d:\d\d(:\d\d)? +(([+-]?\d\d\d\d)|" +
    "(UT)|(GMT)|(EST)|(EDT)|(CST)|(CDT)|(MST)|(MDT)|(PST)|(PDT)|\w)$")
  def validate(self):
    if not self.rfc822_re.match(self.value):
      self.log(InvalidRFC2822Date({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      self.log(ValidRFC2822Date({"parent":self.parent.name, "element":self.name, "value":self.value}))

#
# Decode html entityrefs
#
from htmlentitydefs import entitydefs
def decodehtml(data):
  chunks=re.split('&#?(\w+);',data)

  for i in range(1,len(chunks),2):
    if chunks[i].isdigit():
#      print chunks[i]
      chunks[i]=unichr(int(chunks[i]))
    elif chunks[i] in entitydefs:
      chunks[i]=entitydefs[chunks[i]]
    else:
      chunks[i]='&' + chunks[i] +';'

  return u"".join(map(unicode,chunks))

#
# Scan HTML for relative URLs
#
class absUrlMixin:
  anchor_re = re.compile('<a\s+href=(?:"(.*?)"|\'(.*?)\'|([\w-]+))\s*>', re.IGNORECASE)
  img_re = re.compile('<img\s+[^>]*src=(?:"(.*?)"|\'(.*?)\'|([\w-]+))[\s>]', re.IGNORECASE)
  absref_re = re.compile("\w+:")
  def validateAbsUrl(self,value):
    refs = self.img_re.findall(self.value) + self.anchor_re.findall(self.value)
    for ref in [reduce(lambda a,b: a or b, x) for x in refs]:
      if not self.absref_re.match(decodehtml(ref)):
        self.log(ContainsRelRef({"parent":self.parent.name, "element":self.name}))

#
# Scan HTML for 'devious' content
#
class safeHtmlMixin:
  scriptTag_re = re.compile("<script[>\s]", re.IGNORECASE)
  metaTag_re = re.compile("<meta[>\s]", re.IGNORECASE)
  embedTag_re = re.compile("<embed[>\s]", re.IGNORECASE)
  objectTag_re = re.compile("<object[>\s]", re.IGNORECASE)
  def validateSafe(self,value):
    for evil in check4evil(value).found:
      self.log(ContainsScript({"parent":self.parent.name, "element":self.name, "tag":evil}))
    if self.scriptTag_re.search(value):
      self.log(ContainsScript({"parent":self.parent.name, "element":self.name, "tag":"script"}))
    if self.metaTag_re.search(value):
      self.log(ContainsMeta({"parent":self.parent.name, "element":self.name, "tag":"meta"}))
    if self.embedTag_re.search(value):
      self.log(ContainsEmbed({"parent":self.parent.name, "element":self.name, "tag":"embed"}))
    if self.objectTag_re.search(value):
      self.log(ContainsObject({"parent":self.parent.name, "element":self.name, "tag":"object"}))

class safeHtml(text, safeHtmlMixin, absUrlMixin):
  def validate(self):
    self.validateSafe(self.value)
    self.validateAbsUrl(self.value)

#
# Elements for which html is discouraged, also checks for relative URLs
#
class nonhtml(text,safeHtmlMixin):#,absUrlMixin):
  htmlEndTag_re = re.compile("</\w+>")
  def validate(self):
    if self.htmlEndTag_re.search(self.value):
      self.log(ContainsHTML({"parent":self.parent.name, "element":self.name}))
    self.validateSafe(self.value)
#    self.validateAbsUrl(self.value)

class positiveInteger(text):
  def validate(self):
    try:
      t = int(self.value)
      if t <= 0:
        raise ValueError
      else:
        self.log(ValidInteger({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidInteger({"parent":self.parent.name, "element":self.name, "value":self.value}))
  
#
# mixin to validate URL in attribute
#
class httpURLMixin:
  http_re = re.compile("http://", re.IGNORECASE)
  def validateHttpURL(self, ns, attr):
    value = self.attrs[(ns, attr)]
    if not self.http_re.search(value):
      self.log(InvalidURLAttribute({"parent":self.parent.name, "element":self.name, "attr":attr}))
    else:
      self.log(ValidURLAttribute({"parent":self.parent.name, "element":self.name, "attr":attr}))

class rdfResourceURI(rfc2396):
  def getExpectedAttrNames(self):
    return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'resource')]
  def validate(self):
    if (rdfNS, 'resource') not in self.attrs.getNames():
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"rdf:resource"}))
    else:
      self.value=self.attrs.getValue((rdfNS, 'resource'))
      rfc2396.validate(self)

class rdfAbout(validatorBase):
  def getExpectedAttrNames(self):
    return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'about')]
  def startElementNS(self, name, qname, attrs):
    pass
  def validate(self):
    if (rdfNS, 'about') not in self.attrs.getNames():
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"rdf:about"}))
    else:
      test=rfc2396()
      test.parent=self
      test.dispatcher=self.dispatcher
      test.name=self.name
      test.value=self.attrs.getValue((rdfNS, 'about'))
      test.validate()

class nonblank(text):
  def validate(self, errorClass=NotBlank, extraParams={}):
    if not self.value:
      logparams={"parent":self.parent.name,"element":self.name}
      logparams.update(extraParams)
      self.log(errorClass(logparams))

class unique(nonblank):
  def __init__(self, name, scope):
    self.name=name
    self.scope=scope
    nonblank.__init__(self)
    if not name+'s' in self.scope.__dict__:
      self.scope.__dict__[name+'s']=[]
  def validate(self):
    nonblank.validate(self)
    list=self.scope.__dict__[self.name+'s']
    if self.value in list:
      self.log(DuplicateValue({"parent":self.parent.name, "element":self.name,"value":self.value}))
    else:
      list.append(self.value)

class canonicaluri(text):
  def validate(self, errorClass=NonCanonicalURI, extraParams={}):
    c = canonicalForm(self.value)
    if c is None or c != self.value:
      logparams={"parent":self.parent.name,"element":self.name,"uri":self.value, "curi":c or 'N/A'}
      logparams.update(extraParams)
      self.log(errorClass(logparams))

__history__ = """
$Log$
Revision 1.30  2005/04/04 22:36:17  josephw
Deal with Unicode when escaping HTML.

Revision 1.29  2005/04/04 20:38:10  josephw
Recombine decoded HTML as unicode, rather than byte strings.

Revision 1.28  2005/03/01 16:29:22  rubys
Restore relative uri warnings

Revision 1.27  2005/02/05 12:31:24  rubys
Allow rdf:resource on rdf properties

Revision 1.26  2005/01/27 22:59:25  rubys
Replace "_rdfStuffToIgnore" with rdfExtension

Revision 1.25  2005/01/27 11:43:58  rubys
Add back in RDF specific extensibility checks.  In particular, validate
that mixed content is not present (except for rdf:parseType="Literal")
as rdflib 2.0.5 apparently does not make this check.

Revision 1.24  2005/01/25 11:05:39  josephw
Don't rely on Attributes being directly iterable.

Revision 1.23  2005/01/22 23:45:36  rubys
pass last rss11 test case (neg-ext-notrdf.xml)

Revision 1.22  2005/01/22 05:43:24  rubys
Pass testcases/rss11/must/neg-ext-inode.xml

Revision 1.21  2005/01/22 01:22:39  rubys
pass testcases/rss11/must/neg-ext-adupabout.xml

Revision 1.20  2005/01/21 23:18:43  josephw
Add logging, documentation and tests for canonical URIs.

Revision 1.19  2005/01/21 02:55:35  rubys
Pass neg-anyerss.xml

Revision 1.18  2005/01/20 13:37:32  rubys
neg-anyarss test case from rss 1.1

Revision 1.17  2004/08/15 11:18:13  rubys
Fix for bug 1009404

Revision 1.16  2004/07/28 18:40:15  f8dy
[ 961747 ] tag specific can not contain # character

Revision 1.15  2004/07/12 04:15:11  rubys
s/W3DTF/W3CDTF/g

Revision 1.14  2004/07/07 11:27:27  rubys
Detect unbound prefixes even when the XML parser does not

Revision 1.13  2004/07/02 16:38:10  rubys
Add support for rdf:datatype from http://www.w3.org/TR/rdf-syntax-grammar/

Revision 1.12  2004/04/30 11:50:02  rubys
Detect stray text outside of elements

Revision 1.11  2004/04/19 22:14:28  rubys
Support rdf:parseType="Literal" in text fields

Revision 1.10  2004/02/18 16:12:14  rubys
Make the distiction between W3CDTF and ISO8601 clearer in the docs.

Revision 1.9  2004/02/18 14:30:50  rubys
Don't flag attributes in content with mode="xml"

Revision 1.8  2004/02/18 02:06:46  rubys
Fix for bug 892693: detecting scripting attributes

Revision 1.7  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.6  2004/02/17 22:42:02  rubys
Remove dependence on Python 2.3

Revision 1.5  2004/02/17 19:18:04  rubys
Commit patch 886668: ISO 8601 times with no timezone shouldn't be valid

Revision 1.4  2004/02/17 15:38:39  rubys
Remove email_lax which previously accepted an email address anyplace
within the element

Revision 1.3  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.2  2004/02/13 16:42:46  rubys
Add support for iso-639-2 language codes, as reported by Ian Davis
http://sourceforge.net/mailarchive/forum.php?thread_id=3890007&forum_id=37659

Revision 1.1.1.1  2004/02/03 17:33:17  rubys
Initial import.

Revision 1.71  2003/12/13 21:39:48  f8dy
added test case for tags with dashes or digits

Revision 1.70  2003/12/12 20:37:05  f8dy
oops, URNs can contain letters after all

Revision 1.69  2003/12/12 15:00:22  f8dy
changed blank link attribute tests to new error AttrNotBlank to distinguish them from elements that can not be blank

Revision 1.68  2003/12/12 11:25:56  rubys
Validate mime type in link tags

Revision 1.67  2003/12/12 05:42:05  rubys
Rough in some support for the new link syntax

Revision 1.66  2003/12/11 23:16:32  f8dy
passed new generator test cases

Revision 1.65  2003/12/11 18:20:46  f8dy
passed all content-related testcases

Revision 1.64  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.63  2003/12/11 06:00:51  f8dy
added tag: testcases, passed

Revision 1.62  2003/12/11 04:50:53  f8dy
added test cases for invalid letters in urn NSS, fixed RE to match

Revision 1.61  2003/10/16 15:54:41  rubys
Detect duplicate channels

Revision 1.60  2003/10/16 15:42:36  rubys
Fix regression, allowing the relative URL tests inside xhtml to pass
again.

Revision 1.59  2003/09/18 18:57:31  f8dy
fixed typo in htmlEater

Revision 1.58  2003/09/13 00:16:43  f8dy
change check for relative references to be compatible with pyxml

Revision 1.57  2003/08/24 00:05:34  f8dy
removed iframe tests, after further discussion this is not enough of a security risk to keep feeds from validating

Revision 1.56  2003/08/23 21:01:00  rubys
Validate that content, content:encoded, and xhtml:body are safe

Revision 1.55  2003/08/11 21:39:39  rubys
Support for rdf:About elements caused a regression whereby spurious
error messages were generated for missing titles for RSS 1.0 feeds.

Revision 1.54  2003/08/10 13:49:14  rubys
Add support for chanel and item level rdf:about.  Ensure that http and
ftp URLs have exactly two slashes after the scheme.

Revision 1.53  2003/08/04 01:59:33  rubys
Full http and ftp URIs require two slashes

Revision 1.52  2003/08/04 00:54:35  rubys
Log every valid element (for better self validation in test cases)

Revision 1.51  2003/08/04 00:03:14  rubys
Implement more strict email check for pie

Revision 1.50  2003/07/30 01:33:31  f8dy
tightened up test cases, added explicit parent checks, changed negative tests to positive

Revision 1.49  2003/07/29 20:57:39  f8dy
tightened up test cases, check for parent element, explicitly test for success

Revision 1.48  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.47  2003/07/29 16:44:56  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.46  2003/07/29 16:14:21  rubys
Validate urns

Revision 1.45  2003/07/29 15:46:31  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.44  2003/07/20 17:44:27  rubys
Detect duplicate ids and guids

Revision 1.43  2003/07/13 00:32:13  rubys
Don't bother checking for local/UTC unless the date is valid...

Revision 1.42  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.41  2003/07/07 20:33:50  rubys
Unicode in HTML problem

Revision 1.40  2003/07/07 10:35:50  rubys
Complete first pass of echo/pie tests

Revision 1.39  2003/07/07 02:44:13  rubys
Further progress towards pie

Revision 1.38  2003/07/07 00:54:00  rubys
Rough in some pie/echo support

Revision 1.37  2003/02/25 22:50:20  rubys
allow urls to be html entity encoded

Revision 1.36  2002/11/10 14:32:53  rubys
it is foaf:Person (not foaf:person)

Revision 1.35  2002/11/03 23:33:44  rubys
Noduplicates validator was causing the handler stack to get
momentarily out of synch

Revision 1.34  2002/11/03 22:46:41  rubys
Patch from Christian Schmidt:
"According to RFC-822 section 3.4.2 multiple white-space characters are
treated as one."

Revision 1.33  2002/10/30 15:44:48  rubys
Improve error messages for relative references: error message should
be gramatically correct.  Remove "hidden" fields prevented duplicate
errors from being flagged as such.

Revision 1.32  2002/10/30 09:18:08  rubys
Double encoded &'s in query strings cause mutlple '#' to exist in a URL

Revision 1.31  2002/10/27 22:09:41  rubys
src need not be the last attribute in an <img>

Revision 1.30  2002/10/27 18:54:30  rubys
Issue warnings for relative references in descriptions

Revision 1.29  2002/10/25 15:08:15  rubys
Minor cleanup.  It is zero or one occurances of a double slash.  Also make
it clear that this routine has been repurposed to be a non-relative URI.
Reinstated the original regex which includes relative URIs as a comment.

Revision 1.28  2002/10/24 18:24:36  rubys
Prevent mere mention of <scriptingNews> from causing an error to be flagged.
http://radio.weblogs.com/0001018/2002/10/24.html#a1760

Revision 1.27  2002/10/24 14:47:33  f8dy
decoupled "no duplicates" check from individual validator classes,
allow handlers to return multiple validator classes

Revision 1.26  2002/10/24 14:05:06  f8dy
refactored simpleText() to include list of RDF stuff to ignore

Revision 1.25  2002/10/23 14:47:18  f8dy
added test cases for email address in parentheses (and passed)

Revision 1.24  2002/10/22 20:11:19  f8dy
added test case for RFC 822 date with no seconds (and passed)

Revision 1.23  2002/10/22 19:20:54  f8dy
passed testcase for foaf:person within dc:creator (or any other text
element)

Revision 1.22  2002/10/22 17:29:52  f8dy
loosened restrictions on link/docs/url protocols; RSS now allows any
IANA protocol, not just http:// and ftp://

Revision 1.21  2002/10/22 16:43:55  rubys
textInput vs textinput: don't reject valid 1.0 feeds, but don't allow
invalid textinput fields in RSS 2.0 either...

Revision 1.20  2002/10/22 13:06:41  f8dy
fixed bug with links containing commas

Revision 1.19  2002/10/20 13:36:59  rubys
Permit rdf:Description anywhere text is allowed

Revision 1.18  2002/10/18 19:28:43  f8dy
added testcases for mod_syndication and passed them

Revision 1.17  2002/10/18 15:41:33  f8dy
added (and passed) testcases for unallowed duplicates of the same element

Revision 1.16  2002/10/18 14:17:30  f8dy
added tests for language/dc:language (must be valid ISO-639 language code
plus optional country code) and passed them

Revision 1.15  2002/10/18 13:06:57  f8dy
added licensing information

"""
