"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from logging import *
import re, time
from uri import canonicalForm, urljoin
from rfc822 import AddressList, parsedate

rdfNS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

#
# Valid mime type
#
mime_re = re.compile('[^\s()<>,;:\\"/[\]?=]+/[^\s()<>,;:\\"/[\]?=]+(\s*;\s*[^\s()<>,;:\\"/[\]?=]+=("(\\"|[^"])*"|[^\s()<>,;:\\"/[\]?=]+))*$')

#
# Extensibility hook: logic varies based on type of feed
#
def any(self, name, qname, attrs):
  if self.getFeedType() != TYPE_RSS1:
    return eater()
  else:
    from rdf import rdfExtension
    return rdfExtension(qname)

#
# This class simply eats events.  Useful to prevent cascading of errors
#
class eater(validatorBase):
  def getExpectedAttrNames(self):
    return self.attrs.getNames()

  def characters(self, string):
    pass

  def startElementNS(self, name, qname, attrs):
    # RSS 2.0 arbitrary restriction on extensions
    feedtype=self.getFeedType()
    if (not qname) and feedtype and (feedtype==TYPE_RSS2):
       from logging import NotInANamespace
       self.log(NotInANamespace({"parent":self.name, "element":name, "namespace":'""'}))

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
    self.push(eater(), name, attrs)

from HTMLParser import HTMLParser, HTMLParseError
class HTMLValidator(HTMLParser):
  htmltags = [
    "a", "abbr", "acronym", "address", "applet", "area", "b", "base",
    "basefont", "bdo", "big", "blockquote", "body", "br", "button", "caption",
    "center", "cite", "code", "col", "colgroup", "dd", "del", "dir", "div",
    "dfn", "dl", "dt", "em", "fieldset", "font", "form", "frame", "frameset",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "head", "hr", "html", "i", "iframe", "img", "input", "ins",
    "isindex", "kbd", "label", "legend", "li", "link", "map", "menu", "meta",
    "noframes", "noscript", "object", "ol", "optgroup", "option", "p",
    "param", "pre", "q", "s", "samp", "script", "select", "small", "span",
    "strike", "strong", "style", "sub", "sup", "table", "tbody", "td",
    "textarea", "tfoot", "th", "thead", "title", "tr", "tt", "u", "ul",
    "var", "xmp", "embed"]
  evilattrs = ['onabort', 'onblur', 'onchange', 'onclick', 'ondblclick',
                'onerror', 'onfocus', 'onkeydown', 'onkeypress', 'onkeyup',
                'onload', 'onmousedown', 'onmouseout', 'onmouseover',
                 'onmouseup', 'onreset', 'onresize', 'onsubmit', 'onunload']
  eviltags = ['script','meta','embed','object','noscript'] 
  def __init__(self,value):
    self.scripts=[]
    self.messages=[]
    HTMLParser.__init__(self)
    try:
      self.feed(value)
      self.close()
    except HTMLParseError:
      import sys
      self.messages.append(sys.exc_info()[1].msg)
  def handle_starttag(self, tag, attributes):
    if tag.lower() not in self.htmltags: 
      self.messages.append("Non-html tag: %s" % tag)
    if tag.lower() in HTMLValidator.eviltags: 
      self.scripts.append(tag)
    for (name,value) in attributes:
      if name.lower() in self.evilattrs: self.scripts.append(name)

#
# This class simply html events.  Identifies unsafe events
#
class htmlEater(validatorBase):
  def getExpectedAttrNames(self):
    if self.attrs and len(self.attrs): 
      return self.attrs.getNames()
  def textOK(self): pass
  def startElementNS(self, name, qname, attrs):
    for evil in HTMLValidator.evilattrs:
      if attrs.has_key((None,evil)):
        self.log(SecurityRisk({"parent":self.parent.name, "element":self.name, "tag":evil}))
    self.push(htmlEater(), self.name, attrs)
    if name in HTMLValidator.eviltags:
      self.log(SecurityRisk({"parent":self.parent.name, "element":self.name, "tag":"script"}))
#    if name=='a' and attrs.get((None,'href'),':').count(':')==0:
#        self.log(ContainsRelRef({"parent":self.parent.name, "element":self.name}))
#    if name=='img' and attrs.get((None,'src'), ':').count(':')==0:
#        self.log(ContainsRelRef({"parent":self.parent.name, "element":self.name}))
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
      if self.value.strip():
        self.log(InvalidRDF({"message":"mixed content"}))
      from rdf import rdfExtension
      self.push(rdfExtension(qname), name, attrs)
    else:
      from base import namespaces
      ns = namespaces.get(qname, '')

      if name.find(':') != -1:
        from logging import MissingNamespace
        self.log(MissingNamespace({"parent":self.name, "element":name}))
      else:
        self.log(UndefinedElement({"parent":self.name, "element":name}))

      self.push(eater(), name, attrs)

#
# noduplicates: no child elements, no duplicate siblings
#
class noduplicates(validatorBase):
  def __init__(self, message=DuplicateElement):
    self.message=message
    validatorBase.__init__(self)
  def startElementNS(self, name, qname, attrs):
    pass
  def characters(self, string):
    pass
  def prevalidate(self):
    if self.name in self.parent.children:
      self.log(self.message({"parent":self.parent.name, "element":self.name}))

#
# valid e-mail addr-spec
#
class addr_spec(text):
  email_re = re.compile('''([a-zA-Z0-9_\-\+\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$''')
  message = InvalidAddrSpec
  def validate(self, value=None):
    if not value: value=self.value
    if not self.email_re.match(value):
      self.log(self.message({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      self.log(ValidContact({"parent":self.parent.name, "element":self.name, "value":self.value}))

#
# iso639 language code
#
def iso639_validate(log,value,element,parent):
  import iso639codes
  if '-' in value:
    lang, sublang = value.split('-', 1)
  else:
    lang = value
  if not iso639codes.isoLang.has_key(unicode.lower(unicode(lang))):
    log(InvalidLanguage({"parent":parent, "element":element, "value":value}))
  else:
    log(ValidLanguage({"parent":parent, "element":element}))

class iso639(text):
  def validate(self):
    iso639_validate(self.log, self.value, self.name, self.parent.name) 

#
# iso8601 dateTime
#
class iso8601(text):
  iso8601_re = re.compile("^\d\d\d\d(-\d\d(-\d\d(T\d\d:\d\d(:\d\d(\.\d*)?)?" +
                       "(Z|([+-]\d\d:\d\d))?)?)?)?$")
  message = InvalidISO8601DateTime

  def validate(self):
    if not self.iso8601_re.match(self.value):
      self.log(self.message({"parent":self.parent.name, "element":self.name, "value":self.value}))
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
        self.log(self.message({"parent":self.parent.name, "element":self.name, "value":self.value}))
        return
    if len(date)>2 and int(date[2])>numdays:
      self.log(self.message({"parent":self.parent.name, "element":self.name, "value":self.value}))
      return

    if len(work) > 1:
      time=work[1].split('Z')[0].split('+')[0].split('-')[0]
      time=time.split(':')
      if int(time[0])>23:
        self.log(self.message({"parent":self.parent.name, "element":self.name, "value":self.value}))
        return
      if len(time)>1 and int(time[1])>60:
        self.log(self.message({"parent":self.parent.name, "element":self.name, "value":self.value}))
        return
      if len(time)>2 and float(time[2])>60.0:
        self.log(self.message({"parent":self.parent.name, "element":self.name, "value":self.value}))
        return

    self.log(ValidW3CDTFDate({"parent":self.parent.name, "element":self.name, "value":self.value}))
    return 1

class w3cdtf(iso8601):
  # The same as in iso8601, except a timezone is not optional when
  #  a time is present
  iso8601_re = re.compile("^\d\d\d\d(-\d\d(-\d\d(T\d\d:\d\d(:\d\d(\.\d*)?)?" +
                           "(Z|([+-]\d\d:\d\d)))?)?)?$")
  message = InvalidW3CDTFDate

class rfc3339(iso8601):
  # The same as in iso8601, except that the only thing that is optional
  # is the seconds
  iso8601_re = re.compile("^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d*)?" +
                           "(Z|([+-]\d\d:\d\d))$")
  message = InvalidRFC3339Date

  def validate(self):
    if iso8601.validate(self):
      tomorrow=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.localtime(time.time()+86400))
      if self.value > tomorrow or self.value < "1970":
        self.log(ImplausibleDate({"parent":self.parent.name,
          "element":self.name, "value":self.value}))
        return 0
      return 1
    return 0

class iso8601_date(iso8601):
  date_re = re.compile("^\d\d\d\d-\d\d-\d\d$")
  def validate(self):
    if iso8601.validate(self):
      if not self.date_re.search(self.value):
        self.log(InvalidISO8601Date({"parent":self.parent.name, "element":self.name, "value":self.value}))

iana_schemes = [
  "ftp", "http", "gopher", "mailto", "news", "nntp", "telnet", "wais",
  "file", "prospero", "z39.50s", "z39.50r", "cid", "mid", "vemmi",
  "service", "imap", "nfs", "acap", "rtsp", "tip", "pop", "data", "dav",
  "opaquelocktoken", "sip", "sips", "tel", "fax", "modem", "ldap",
  "https", "soap.beep", "soap.beeps", "xmlrpc.beep", "xmlrpc.beeps",
  "urn", "go", "h323", "ipp", "tftp", "mupdate", "pres", "im", "mtqp",
  "iris.beep", "dict", "snmp", "crid", "tag", "dns", "info"
]

#
# rfc2396 fully qualified (non-relative) uri
#
class rfc2396(text):
  rfc2396_re = re.compile("([a-zA-Z][0-9a-zA-Z+\\-\\.]*:)?/{0,2}" +
    "[0-9a-zA-Z;/?:@&=+$\\.\\-_!~*'()%,#]*$")
  urn_re = re.compile(r"^urn:[a-zA-Z0-9][a-zA-Z0-9-]{1,31}:([a-zA-Z0-9()+,\.:=@;$_!*'\-]|%[0-9A-Fa-f]{2})+$")
  tag_re = re.compile(r"^tag:([a-z0-9\-\._]+?@)?[a-z0-9\.\-]+?,\d{4}(-\d{2}(-\d{2})?)?:[0-9a-zA-Z;/\?:@&=+$\.\-_!~*'\(\)%,]*(#[0-9a-zA-Z;/\?:@&=+$\.\-_!~*'\(\)%,]*)?$")
  def validate(self, errorClass=InvalidLink, successClass=ValidURI, extraParams={}):
    success = 0
    scheme=self.value.split(':')[0].lower()
    if scheme=='tag':
      if self.tag_re.match(self.value):
        success = 1
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(ValidTAG(logparams))
      else:
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(InvalidTAG(logparams))
    elif scheme=="urn":
      if self.urn_re.match(self.value):
        success = 1
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(ValidURN(logparams))
      else:
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(InvalidURN(logparams))
    elif not self.rfc2396_re.match(self.value):
      logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
      logparams.update(extraParams)
      try:
        if self.rfc2396_re.match(self.value.encode('idna')):
          errorClass=UriNotIri
      except:
        pass
      self.log(errorClass(logparams))
    elif scheme in ['http','ftp']:
      if not re.match('^\w+://[^/].*',self.value):
        logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
        logparams.update(extraParams)
        self.log(errorClass(logparams))
      else:
        success = 1
    elif self.value.find(':')>=0 and self.value.split(':')[0] not in iana_schemes:
      logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
      logparams.update(extraParams)
      self.log(errorClass(logparams))
    else:
      success = 1
    if success:
      logparams = {"parent":self.parent.name, "element":self.name, "value":self.value}
      logparams.update(extraParams)
      self.log(successClass(logparams))
    return success

#
# rfc3987 iri
#
class rfc3987(rfc2396):
  def validate(self, errorClass=InvalidIRI, successClass=ValidURI, extraParams={}):
    try:
      self.value = self.value.encode('idna')
    except:
      pass # apparently '.' produces label too long
    return rfc2396.validate(self, errorClass, successClass, extraParams)

class rfc2396_full(rfc2396): 
  rfc2396_re = re.compile("[a-zA-Z][0-9a-zA-Z+\\-\\.]*:(//)?" +
    "[0-9a-zA-Z;/?:@&=+$\\.\\-_!~*'()%,#]+$")
  def validate(self, errorClass=InvalidFullLink, successClass=ValidURI, extraParams={}):
    return rfc2396.validate(self, errorClass, successClass, extraParams)

#
# URI reference resolvable relative to xml:base
#
class xmlbase(rfc3987):
  def validate(self, errorClass=InvalidIRI, successClass=ValidURI, extraParams={}):
    if rfc3987.validate(self, errorClass, successClass, extraParams):
      if self.dispatcher.xmlBase != self.xmlBase:
        docbase=canonicalForm(self.dispatcher.xmlBase).split('#')[0]
        elembase=canonicalForm(self.xmlBase).split('#')[0]
        value=canonicalForm(urljoin(elembase,self.value)).split('#')[0]
        if (value==elembase) and (elembase!=docbase):
          self.log(SameDocumentReference({"parent":self.parent.name, "element":self.name, "value":self.value}))

#
# rfc822 dateTime (+Y2K extension)
#
class rfc822(text):
  rfc822_re = re.compile("(((Mon)|(Tue)|(Wed)|(Thu)|(Fri)|(Sat)|(Sun))\s*,\s*)?" +
    "\d\d?\s+((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|" +
    "(Nov)|(Dec))\s+\d\d(\d\d)?\s+\d\d:\d\d(:\d\d)?\s+(([+-]?\d\d\d\d)|" +
    "(UT)|(GMT)|(EST)|(EDT)|(CST)|(CDT)|(MST)|(MDT)|(PST)|(PDT)|\w)*$")
  rfc2822_re = re.compile("(((Mon)|(Tue)|(Wed)|(Thu)|(Fri)|(Sat)|(Sun)), *)?" +
    "\d\d? +((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|" +
    "(Nov)|(Dec)) +\d\d\d\d +\d\d:\d\d(:\d\d)? +(([+-]?\d\d\d\d)|" +
    "(UT)|(GMT)|(EST)|(EDT)|(CST)|(CDT)|(MST)|(MDT)|(PST)|(PDT)|Z)$")
  def validate(self):
    value1,value2 = '', self.value
    while value1!=value2: value1,value2=value2,re.sub('\([^)]*\)','',value2)
    if not self.rfc822_re.match(value2.strip()):
      self.log(InvalidRFC2822Date({"parent":self.parent.name, "element":self.name, "value":self.value}))
    elif not self.rfc2822_re.match(self.value):
      self.log(DeprecatedRFC822Date({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      value = parsedate(self.value)
      tomorrow=time.localtime(time.time()+86400)
      if value > tomorrow or value[0] < 1970:
        self.log(ImplausibleDate({"parent":self.parent.name,
          "element":self.name, "value":self.value}))
      else:
        self.log(ValidRFC2822Date({"parent":self.parent.name, "element":self.name, "value":self.value}))

#
# Decode html entityrefs
#
from htmlentitydefs import name2codepoint
def decodehtml(data):
  chunks=re.split('&#?(\w+);',data)

  for i in range(1,len(chunks),2):
    if chunks[i].isdigit():
#      print chunks[i]
      chunks[i]=unichr(int(chunks[i]))
    elif chunks[i] in name2codepoint:
      chunks[i]=unichr(name2codepoint[chunks[i]])
    else:
      chunks[i]='&' + chunks[i] +';'

#  print repr(chunks)
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
  def validateSafe(self,value):
    htmlValidator = HTMLValidator(value)
    if not htmlValidator.messages:
      self.log(ValidHtml({"parent":self.parent.name, "element":self.name,"value":self.value}))
    for message in htmlValidator.messages:
      self.log(NotHtml({"parent":self.parent.name, "element":self.name,"value":self.value, "message": message}))
    for evil in htmlValidator.scripts:
      self.log(SecurityRisk({"parent":self.parent.name, "element":self.name, "tag":evil}))

class safeHtml(text, safeHtmlMixin, absUrlMixin):
  def validate(self):
    self.validateSafe(self.value)
    self.validateAbsUrl(self.value)

#
# Elements for which email addresses are discouraged
#
class nonemail(text):
  email_re = re.compile("<" + addr_spec.email_re.pattern[:-1] + ">")
  def validate(self):
    if self.email_re.search(self.value):
      self.log(ContainsEmail({"parent":self.parent.name, "element":self.name}))

#
# Elements for which html is discouraged, also checks for relative URLs
#
class nonhtml(text,safeHtmlMixin):#,absUrlMixin):
  htmlEndTag_re = re.compile("</(\w+)>")
  htmlEntity_re = re.compile("&#?\w+;")
  def validate(self, message=ContainsHTML):
    if [t for t in self.htmlEndTag_re.findall(self.value) if t in HTMLValidator.htmltags]:
      self.log(message({"parent":self.parent.name, "element":self.name, "value":self.value}))
    elif self.htmlEntity_re.search(self.value):
      self.log(message({"parent":self.parent.name, "element":self.name, "value":self.value}))

#
# valid e-mail addresses
#
class email(addr_spec,nonhtml):
  message = InvalidContact
  def validate(self):
    value=self.value
    list = AddressList(self.value)
    if len(list)==1: value=list[0][1]
    nonhtml.validate(self)
    addr_spec.validate(self, value)

class positiveInteger(text):
  def validate(self):
    if self.value == '': return
    try:
      t = int(self.value)
      if t <= 0:
        raise ValueError
      else:
        self.log(ValidInteger({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidPositiveInteger({"parent":self.parent.name, "element":self.name, "value":self.value}))

class nonNegativeInteger(text):
  def validate(self):
    try:
      t = int(self.value)
      if t < 0:
        raise ValueError
      else:
        self.log(ValidInteger({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidInteger({"parent":self.parent.name, "element":self.name, "value":self.value}))

class percentType(text):
  def validate(self):
    try:
      t = float(self.value)
      if t < 0.0 or t > 100.0:
        raise ValueError
      else:
        self.log(ValidPercentage({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidPercentage({"parent":self.parent.name, "element":self.name, "value":self.value}))

class latitude(text):
  def validate(self):
    try:
      lat = float(self.value)
      if lat > 90 or lat < -90:
        raise ValueError
      else:
        self.log(ValidLatitude({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidLatitude({"parent":self.parent.name, "element":self.name, "value":self.value}))

class longitude(text):
  def validate(self):
    try:
      lon = float(self.value)
      if lon > 180 or lon < -180:
        raise ValueError
      else:
        self.log(ValidLongitude({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidLongitude({"parent":self.parent.name, "element":self.name, "value":self.value}))

#
# mixin to validate URL in attribute
#
class httpURLMixin:
  http_re = re.compile("http://", re.IGNORECASE)
  def validateHttpURL(self, ns, attr):
    value = self.attrs[(ns, attr)]
    if not self.http_re.search(value):
      self.log(InvalidURLAttribute({"parent":self.parent.name, "element":self.name, "attr":attr}))
    elif not rfc2396_full.rfc2396_re.match(value):
      self.log(InvalidURLAttribute({"parent":self.parent.name, "element":self.name, "attr":attr}))
    else:
      self.log(ValidURLAttribute({"parent":self.parent.name, "element":self.name, "attr":attr}))

class rdfResourceURI(rfc2396):
  def getExpectedAttrNames(self):
    return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'resource'),
            (u'http://purl.org/dc/elements/1.1/', u'title')]
  def validate(self):
    if (rdfNS, 'resource') in self.attrs.getNames():
      self.value=self.attrs.getValue((rdfNS, 'resource'))
      rfc2396.validate(self)
    elif self.getFeedType() == TYPE_RSS1:
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"rdf:resource"}))

class rdfAbout(validatorBase):
  def getExpectedAttrNames(self):
    return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'about')]
  def startElementNS(self, name, qname, attrs):
    pass
  def validate(self):
    if (rdfNS, 'about') not in self.attrs.getNames():
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":"rdf:about"}))
    else:
      test=rfc2396().setElement(self.name, self.attrs, self)
      test.value=self.attrs.getValue((rdfNS, 'about'))
      test.validate()

class nonblank(text):
  def validate(self, errorClass=NotBlank, extraParams={}):
    if not self.value:
      logparams={"parent":self.parent.name,"element":self.name}
      logparams.update(extraParams)
      self.log(errorClass(logparams))

class nows(text):
  def __init__(self):
    self.ok = 1
    text.__init__(self)
  def characters(self, string):
    text.characters(self, string)
    if self.ok and (self.value != self.value.strip()):
      self.log(UnexpectedWhitespace({"parent":self.parent.name, "element":self.name}))
      self.ok = 0

class unique(nonblank):
  def __init__(self, name, scope, message=DuplicateValue):
    self.name=name
    self.scope=scope
    self.message=message
    nonblank.__init__(self)
    if not name+'s' in self.scope.__dict__:
      self.scope.__dict__[name+'s']=[]
  def validate(self):
    nonblank.validate(self)
    list=self.scope.__dict__[self.name+'s']
    if self.value in list:
      self.log(self.message({"parent":self.parent.name, "element":self.name,"value":self.value}))
    else:
      list.append(self.value)

class canonicaluri(rfc2396_full):
  def validate(self):
    prestrip = self.value
    self.value = self.value.strip()
    if rfc2396_full.validate(self):
      c = canonicalForm(self.value)
      if c is None or c != prestrip:
        self.log(NonCanonicalURI({"parent":self.parent.name,"element":self.name,"uri":prestrip, "curi":c or 'N/A'}))

class yesno(text):
  def normalizeWhitespace(self):
    pass
  def validate(self):
    if not self.value.lower() in ['yes','no','clean']:
      self.log(InvalidYesNo({"parent":self.parent.name, "element":self.name,"value":self.value}))

class truefalse(text):
  def normalizeWhitespace(self):
    pass
  def validate(self):
    if not self.value.lower() in ['true','false']:
      self.log(InvalidTrueFalse({"parent":self.parent.name, "element":self.name,"value":self.value}))

class duration(text):
  duration_re = re.compile("([0-9]?[0-9]:)?[0-5]?[0-9]:[0-5][0-9]$")
  def validate(self):
    if not self.duration_re.search(self.value):
      self.log(InvalidDuration({"parent":self.parent.name, "element":self.name
      , "value":self.value}))

class lengthLimitedText(nonhtml):
  def __init__(self, max):
    self.max = max
    text.__init__(self)
  def validate(self):
    if len(self.value)>self.max:
      self.log(TooLong({"parent":self.parent.name, "element":self.name,
        "len": len(self.value), "max": self.max}))
    nonhtml.validate(self)

class keywords(text):
  def validate(self):
    if self.value.find(' ')>=0 and self.value.find(',')<0:
      self.log(InvalidKeywords({"parent":self.parent.name, "element":self.name}))

class commaSeparatedIntegers(text):
  def validate(self):
    if not re.match("^\d+(,\s*\d+)*$", self.value):
      self.log(InvalidCommaSeparatedIntegers({"parent":self.parent.name, 
        "element":self.name}))

class formname(text):
  def validate(self):
    if not re.match("^[a-zA-z][a-zA-z0-9:._]*", self.value):
      self.log(InvalidFormComponentName({"parent":self.parent.name, 
        "element":self.name, "value":self.value}))
