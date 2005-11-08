"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import Locator
from logging import NonCanonicalURI, NotUTF8
import re

# references:
# http://web.resource.org/rss/1.0/modules/standard.html
# http://web.resource.org/rss/1.0/modules/proposed.html
# http://dmoz.org/Reference/Libraries/Library_and_Information_Science/Technical_Services/Cataloguing/Metadata/RDF/Applications/RSS/Specifications/RSS1.0_Modules/
namespaces = {
  "http://webns.net/mvcb/":                         "admin",
  "http://purl.org/rss/1.0/modules/aggregation/":   "ag",
  "http://purl.org/rss/1.0/modules/annotate/":      "annotate",
  "http://media.tangent.org/rss/1.0/":              "audio",
  "http://backend.userland.com/blogChannelModule":  "blogChannel",
  "http://web.resource.org/cc/":                    "cc",
  "http://backend.userland.com/creativeCommonsRssModule": "creativeCommons",
  "http://purl.org/rss/1.0/modules/company":        "company",
  "http://purl.org/rss/1.0/modules/content/":       "content",
  "http://my.theinfo.org/changed/1.0/rss/":         "cp",
  "http://purl.org/dc/elements/1.1/":               "dc",
  "http://purl.org/dc/terms/":                      "dcterms",
  "http://purl.org/rss/1.0/modules/email/":         "email",
  "http://purl.org/rss/1.0/modules/event/":         "ev",
  "http://www.w3.org/2003/01/geo/wgs84_pos#":       "geo",
  "http://geourl.org/rss/module/":                  "geourl",
  "http://postneo.com/icbm":                        "icbm",
  "http://purl.org/rss/1.0/modules/image/":         "image",
  "http://www.itunes.com/dtds/podcast-1.0.dtd":     "itunes",
  "http://xmlns.com/foaf/0.1/":                     "foaf",
  "http://purl.org/rss/1.0/modules/link/":          "l",
  "http://www.w3.org/1999/02/22-rdf-syntax-ns#":    "rdf",
  "http://www.w3.org/2000/01/rdf-schema#":          "rdfs",
  "http://purl.org/rss/1.0/modules/reference/":     "ref",
  "http://purl.org/rss/1.0/modules/richequiv/":     "reqv",
  "http://purl.org/rss/1.0/modules/rss091#":        "rss091",
  "http://purl.org/rss/1.0/modules/search/":        "search",
  "http://purl.org/rss/1.0/modules/slash/":         "slash",
  "http://purl.org/rss/1.0/modules/servicestatus/": "ss",
  "http://hacks.benhammersley.com/rss/streaming/":  "str",
  "http://purl.org/rss/1.0/modules/subscription/":  "sub",
  "http://purl.org/rss/1.0/modules/syndication/":   "sy",
  "http://purl.org/rss/1.0/modules/taxonomy/":      "taxo",
  "http://purl.org/rss/1.0/modules/threading/":     "thr",
  "http://madskills.com/public/xml/rss/module/trackback/": "trackback",
  "http://purl.org/rss/1.0/modules/wiki/":          "wiki",
  "http://schemas.xmlsoap.org/soap/envelope/":      "soap",
  "http://purl.org/atom/ns#":                       "atom",
  "http://www.w3.org/2005/Atom":                    "atom",
  "http://www.w3.org/1999/xhtml":                   "xhtml",
  "http://my.netscape.com/rdf/simple/0.9/":         "rss090",
  "http://purl.org/net/rss1.1#":                    "rss11",
}

def near_miss(ns):
  try:
    return re.match(".*\w", ns).group().lower()
  except:
    return ns

nearly_namespaces = dict([(near_miss(u),p) for u,p in namespaces.items()])

stdattrs = [(u'http://www.w3.org/XML/1998/namespace', u'base'), 
            (u'http://www.w3.org/XML/1998/namespace', u'lang'),
            (u'http://www.w3.org/XML/1998/namespace', u'space')]

#
# From the SAX parser's point of view, this class is the one responsible for
# handling SAX events.  In actuality, all this class does is maintain a
# pushdown stack of the *real* content handlers, and delegates sax events
# to the current one.
#
class SAXDispatcher(ContentHandler):

  firstOccurrenceOnly = 0

  def __init__(self, base, selfURIs, encoding):
    from root import root
    ContentHandler.__init__(self)
    self.lastKnownLine = 1
    self.lastKnownColumn = 0
    self.loggedEvents = []
    self.feedType = 0
    self.xmlBase = base
    self.selfURIs = selfURIs
    self.encoding = encoding
    self.handler_stack=[[root(self, base)]]
    validatorBase.defaultNamespaces = []

  def setDocumentLocator(self, locator):
    self.locator = locator
    ContentHandler.setDocumentLocator(self, self.locator)

  def setFirstOccurrenceOnly(self, firstOccurrenceOnly=1):
    self.firstOccurrenceOnly = firstOccurrenceOnly

  def startPrefixMapping(self, prefix, uri):
    if namespaces.has_key(uri):
      if not namespaces[uri] == prefix and prefix:
        from logging import NonstdPrefix
        self.log(NonstdPrefix({'preferred':namespaces[uri], 'ns':uri}))
    elif prefix in namespaces.values():
      from logging import ReservedPrefix
      preferredURI = [key for key, value in namespaces.items() if value == prefix][0]
      self.log(ReservedPrefix({'prefix':prefix, 'ns':preferredURI}))

  def startElementNS(self, name, qname, attrs):
    self.lastKnownLine = self.locator.getLineNumber()
    self.lastKnownColumn = self.locator.getColumnNumber()
    qname, name = name
    for handler in iter(self.handler_stack[-1]):
      handler.startElementNS(name, qname, attrs)

    if len(attrs):
      present = attrs.getNames()
      unexpected = filter(lambda x: x not in stdattrs, present)
      for handler in iter(self.handler_stack[-1]):
        ean = handler.getExpectedAttrNames()
        if ean: unexpected = filter(lambda x: x not in ean, unexpected)
      for u in unexpected:
        if u[0] and near_miss(u[0]) not in nearly_namespaces: continue
        from logging import UnexpectedAttribute
        if not u[0]: u=u[1]
        self.log(UnexpectedAttribute({"parent":name, "attribute":u, "element":name}))

  def resolveEntity(self, publicId, systemId):
    if not publicId and not systemId:
      import cStringIO
      return cStringIO.StringIO()

    try:
      def log(exception):
        from logging import SAXError
        self.log(SAXError({'exception':str(exception)}))
      if self.xmlvalidator:
        self.xmlvalidator(log)
      self.xmlvalidator=0
    except:
      pass

    if (publicId=='-//Netscape Communications//DTD RSS 0.91//EN' and
        systemId=='http://my.netscape.com/publish/formats/rss-0.91.dtd'):
      from logging import ValidDoctype
      self.log(ValidDoctype({}))
    else:
      from logging import ContainsSystemEntity
      self.lastKnownLine = self.locator.getLineNumber()
      self.lastKnownColumn = self.locator.getColumnNumber()
      self.log(ContainsSystemEntity({}))
    from StringIO import StringIO
    return StringIO()

  def skippedEntity(self, name):
    from logging import UndefinedNamedEntity
    self.log(UndefinedNamedEntity({'value':name}))

  def characters(self, string):
    self.lastKnownLine = self.locator.getLineNumber()
    self.lastKnownColumn = self.locator.getColumnNumber()
    for handler in iter(self.handler_stack[-1]):
      handler.characters(string)

  def endElementNS(self, name, qname):
    self.lastKnownLine = self.locator.getLineNumber()
    self.lastKnownColumn = self.locator.getColumnNumber()
    qname, name = name
    for handler in iter(self.handler_stack[-1]):
      handler.endElementNS(name, qname)
    del self.handler_stack[-1]

  def push(self, handlers, name, attrs, parent):
    try:
      for handler in iter(handlers):
        handler.setElement(name, attrs, parent)
        handler.value=""
        handler.prevalidate()
    except:
      handlers.setElement(name, attrs, parent)
      handlers.value=""
      handlers.prevalidate()
      handlers = [handlers]
    self.handler_stack.append(handlers)

  def log(self, event, offset=(0,0)):
    def findDuplicate(self, event):
      duplicates = [e for e in self.loggedEvents if e.__class__ == event.__class__]
      if duplicates and (event.__class__ in [NonCanonicalURI]):
        return duplicates[0]

      for dup in duplicates:
        for k, v in event.params.items():
          if k != 'value':
            if not k in dup.params or dup.params[k] != v: break
        else:
          return dup
          
    if event.params.has_key('element') and event.params['element']:
      event.params['element'] = event.params['element'].replace('_', ':')
    if self.firstOccurrenceOnly:
      dup = findDuplicate(self, event)
      if dup:
        dup.params['msgcount'] = dup.params['msgcount'] + 1
        return
      event.params['msgcount'] = 1
    try:
      line = self.locator.getLineNumber() + offset[0]
      backupline = self.lastKnownLine
      column = (self.locator.getColumnNumber() or 0) + offset[1]
      backupcolumn = self.lastKnownColumn
    except AttributeError:
      line = backupline = column = backupcolumn = 1
    event.params['line'] = line
    event.params['backupline'] = backupline
    event.params['column'] = column
    event.params['backupcolumn'] = backupcolumn
    self.loggedEvents.append(event)

  def error(self, exception):
    from logging import SAXError
    self.log(SAXError({'exception':str(exception)}))
    raise exception
  fatalError=error
  warning=error

  def getFeedType(self):
    return self.feedType

  def setFeedType(self, feedType):
    self.feedType = feedType

#
# This base class for content handlers keeps track of such administrative
# details as the parent of the current element, and delegating both log
# and push events back up the stack.  It will also concatenate up all of
# the SAX events associated with character data into a value, handing such
# things as CDATA and entities.
#
# Subclasses are expected to declare "do_name" methods for every
# element that they support.  These methods are expected to return the
# appropriate handler for the element.
#
# The name of the element and the names of the children processed so
# far are also maintained.
#
# Hooks are also provided for subclasses to do "prevalidation" and
# "validation".
#
from logging import TYPE_RSS2

class validatorBase(ContentHandler):
  defaultNamespaces = []
  
  def __init__(self):
    ContentHandler.__init__(self)
    self.value = ""
    self.attrs = None
    self.children = []
    self.isValid = 1
    self.name = None
    self.itunes = False

  def setElement(self, name, attrs, parent):
    self.name = name
    self.attrs = attrs
    self.parent = parent
    self.dispatcher = parent.dispatcher
    self.xmlLang = parent.xmlLang

    if attrs and attrs.has_key((u'http://www.w3.org/XML/1998/namespace', u'base')):
      self.xmlBase=attrs.getValue((u'http://www.w3.org/XML/1998/namespace', u'base'))
      from validators import rfc2396
      if not rfc2396.rfc2396_re.match(self.xmlBase):
        from logging import InvalidURI
        self.log(InvalidURI({"element":"xml:base", "parent":name}))
      from urlparse import urljoin
      self.xmlBase = urljoin(parent.xmlBase, self.xmlBase)
    else:
      self.xmlBase = parent.xmlBase

    return self

  def getExpectedAttrNames(self):
    None

  def unknown_starttag(self, name, qname, attrs):
    from validators import any
    return any(self, name, qname, attrs)

  def startElementNS(self, name, qname, attrs):
    if attrs.has_key((u'http://www.w3.org/XML/1998/namespace', u'lang')):
      self.xmlLang=attrs.getValue((u'http://www.w3.org/XML/1998/namespace', u'lang'))
      from validators import iso639_validate
      iso639_validate(self.log, self.xmlLang, "xml:lang", name)

    from validators import eater
    feedtype=self.getFeedType()
    if (not qname) and feedtype and (feedtype!=TYPE_RSS2):
       from logging import InvalidNamespace
       self.log(InvalidNamespace({"parent":self.name, "element":name, "namespace":'""'}))
    if qname in self.defaultNamespaces: qname=None
    hasNS = (qname<>None)

    nm_qname = near_miss(qname)
    if nearly_namespaces.has_key(nm_qname):
      prefix = nearly_namespaces[nm_qname]
      qname, name = None, prefix + "_" + name
      if prefix == 'itunes' and not self.itunes and not self.parent.itunes:
        if hasattr(self, 'setItunes'): self.setItunes(True)

    # ensure all attribute namespaces are properly defined
    for (namespace,attr) in attrs.keys():
      if ':' in attr and not namespace:
        from logging import MissingNamespace
        self.log(MissingNamespace({"parent":self.name, "element":attr}))

    if qname:
      handler = self.unknown_starttag(name, qname, attrs)
      name="unknown_"+name
    else:
      try:
        self.child=name
        handler = getattr(self, "do_" + name.replace("-","_"))()
      except AttributeError:
        if name.find(':') != -1:
          from logging import MissingNamespace
          self.log(MissingNamespace({"parent":self.name, "element":name}))
          handler = eater()
        elif not qname:
          from logging import UndefinedElement
          self.log(UndefinedElement({"parent":self.name.replace("_",":"), "element":name}))
          handler = eater()
	else:
          handler = self.unknown_starttag(name, qname, attrs)
	  name="unknown_"+name

    self.push(handler, name, attrs)

     # MAP - always append name, even if already exists (we need this to
     # check for too many hour elements in skipHours, and it doesn't
     # hurt anything else)
    self.children.append(name)

  def normalizeWhitespace(self):
    self.value = self.value.strip()

  def endElementNS(self, name, qname):
    self.normalizeWhitespace()
    self.validate()
    if self.isValid and self.name: 
      from validators import ValidElement
      self.log(ValidElement({"parent":self.parent.name, "element":name}))

  def characters(self, string):
    if string.strip() and self.children:
      from validators import UnexpectedText
      self.log(UnexpectedText({"element":self.name,"parent":self.parent.name}))
    line=column=0
    for c in string:
      if 0x80 <= ord(c) <= 0x9F:
        from validators import BadCharacters
        self.log(BadCharacters({"parent":self.parent.name, "element":self.name}), offset=(line,column))
      column=column+1
      if ord(c) in (10,13):
        column=0
	line=line+1

    self.value = self.value + string

  def log(self, event, offset=(0,0)):
    self.dispatcher.log(event, offset)
    self.isValid = 0

  def setFeedType(self, feedType):
    self.dispatcher.setFeedType(feedType)
    
  def getFeedType(self):
    return self.dispatcher.getFeedType()
    
  def push(self, handler, name, value):
    self.dispatcher.push(handler, name, value, self)

  def leaf(self):
    from validators import text
    return text()

  def prevalidate(self):
    pass
  
  def validate(self):
    pass

__history__ = """
$Log$
Revision 1.43  2005/11/08 18:27:42  rubys
Warn on missing language, itunes:explicit, or itunes:category if any itunes
elements are present.

Revision 1.42  2005/11/07 16:39:20  rubys
Warning on itunes elements in non-utf-8 feeds

Revision 1.41  2005/11/07 03:55:40  rubys
Add support for new-feed-url

Revision 1.40  2005/11/07 03:12:34  rubys
Itunes update:
http://lists.apple.com/archives/syndication-dev/2005/Nov/msg00002.html

Revision 1.39  2005/08/28 18:58:00  rubys
Don't issue a warning if content-negotiation presents an alias

Revision 1.38  2005/08/20 03:58:58  rubys
white-space + xml:base

Revision 1.37  2005/08/03 04:40:08  rubys
whitespace

Revision 1.36  2005/08/01 14:23:44  rubys
Provide more helpful advice when people attempt to use XHTML named entity
references inside their feeds.

Addresses bugs: 1242762, 1243771, 1249420

Revision 1.35  2005/07/28 10:18:02  rubys
Only report first occurance of NonCanonicalURI

Revision 1.34  2005/07/24 20:11:21  rubys
Log skipped entities (initially as an error, but may get downgraded to
a warning or info as I learn more)

Revision 1.33  2005/07/24 19:55:30  rubys
Atom 1.0 4.2.11

Revision 1.32  2005/07/19 19:57:45  rubys
Few things I spotted...

Revision 1.31  2005/07/18 18:53:28  rubys
Atom 1.0 section 4.1.3

Revision 1.30  2005/07/16 00:24:34  rubys
Through section 2

Revision 1.29  2005/07/15 11:17:24  rubys
Baby steps towards Atom 1.0 support

Revision 1.28  2005/07/05 17:15:35  rubys
Provide more information on namespace errors; also try to recover from
common mistakes.

Revision 1.27  2005/07/04 22:54:31  philor
Support rest of dc, dcterms, geo, geourl, icbm, and refactor out common extension elements

Revision 1.26  2005/07/03 04:23:41  philor
Support Trackback module

Revision 1.25  2005/07/01 23:55:23  rubys
Initial support for itunes

Revision 1.24  2005/06/28 22:14:58  rubys
Catch errors involving unknown elements in known namespaces

Revision 1.23  2005/05/10 22:11:36  rubys
Unknown attribute in unknown namespace is valid

Revision 1.22  2005/04/04 20:23:51  josephw
Workaround for locator.getColumnNumber() sometimes returning None.

Revision 1.21  2005/01/22 23:45:36  rubys
pass last rss11 test case (neg-ext-notrdf.xml)

Revision 1.20  2005/01/21 13:52:54  rubys
Better fix for Mozilla bug 279202

Revision 1.19  2005/01/20 13:37:32  rubys
neg-anyarss test case from rss 1.1

Revision 1.18  2005/01/19 01:28:13  rubys
Initial support for rss 1.1

Revision 1.17  2004/07/28 12:24:25  rubys
Partial support for verifing xml:lang

Revision 1.16  2004/06/28 23:34:46  rubys
Support RSS 0.90

Revision 1.15  2004/06/21 22:28:50  rubys
Fix 976875: XML Validation
Validation is only performed if libxml2 is installed (libxml2 is installed
on both feeds.archive.org and feedvalidator.org) and a DOCTYPE is present.

Revision 1.14  2004/04/30 11:50:02  rubys
Detect stray text outside of elements

Revision 1.13  2004/04/19 18:00:18  rubys
Detect rss10 feeds with incorrect namespaces

Revision 1.12  2004/02/20 15:35:46  rubys
Feature 900555: RSS+Atom support

Revision 1.11  2004/02/19 12:37:40  rubys
Remove debugging print statement

Revision 1.10  2004/02/19 12:36:03  rubys
Report encoding errors more precisely

Revision 1.9  2004/02/18 19:09:23  rubys
Add xml:space to the list of expected attributes

Revision 1.8  2004/02/18 15:38:17  rubys
rdf:resource and rdf:about attributes are flagged on image tags in rss 1.0

Revision 1.7  2004/02/17 22:42:02  rubys
Remove dependence on Python 2.3

Revision 1.6  2004/02/16 18:36:03  rubys
Don't display 'None' for attributes without a namespace

Revision 1.5  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.4  2004/02/16 01:41:05  rubys
Fix for 893709: Detected an unknown type feed reported by Les Orchard

Revision 1.3  2004/02/07 14:23:19  rubys
Fix for bug 892178: must reject xml 1.1

Revision 1.2  2004/02/06 18:43:18  rubys
Apply patch 886675 from Joseph Walton:
"Warn about windows-1252 presented as ISO-8859-1"

Revision 1.1.1.1  2004/02/03 17:33:15  rubys
Initial import.

Revision 1.41  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.40  2003/08/23 23:25:14  rubys
Allow unprefixed elements (like xhtml) to pass through without warning

Revision 1.39  2003/08/23 21:01:00  rubys
Validate that content, content:encoded, and xhtml:body are safe

Revision 1.38  2003/08/12 02:02:26  rubys
Detect unknown elements even if they have underscores.  Reported by
Brent Simmons.

Revision 1.37  2003/08/09 18:18:03  rubys
Permit NetScape's 0.91 DOCTYPE

Revision 1.36  2003/08/05 05:32:35  f8dy
0.2 snapshot - change version number and default namespace

Revision 1.35  2003/08/04 00:54:35  rubys
Log every valid element (for better self validation in test cases)

Revision 1.34  2003/07/28 21:56:52  rubys
Check attributes for valid namespaces

Revision 1.33  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.32  2003/07/07 00:54:00  rubys
Rough in some pie/echo support

Revision 1.31  2003/06/26 18:03:04  f8dy
add workaround for case where SAX throws UnicodeError but locator.getLineNumber() is screwy

Revision 1.30  2003/04/07 19:49:22  rubys
Handle ignorable whitespace in elements such as comments

Revision 1.29  2003/03/01 13:53:22  rubys
Improved duplicate checking

Revision 1.28  2002/12/20 13:26:00  rubys
CreativeCommons support

Revision 1.27  2002/10/31 00:52:21  rubys
Convert from regular expressions to EntityResolver for detecting
system entity references

Revision 1.26  2002/10/30 23:03:01  f8dy
security fix: external (SYSTEM) entities

Revision 1.25  2002/10/24 14:47:33  f8dy
decoupled "no duplicates" check from individual validator classes,
allow handlers to return multiple validator classes

Revision 1.24  2002/10/24 13:55:58  f8dy
added rdfs namespace

Revision 1.23  2002/10/22 19:20:54  f8dy
passed testcase for foaf:person within dc:creator (or any other text
element)

Revision 1.22  2002/10/22 12:57:35  f8dy
fixed bug setting parameters for ReservedPrefix error

Revision 1.21  2002/10/18 20:31:28  f8dy
fixed namespace for mod_aggregation

Revision 1.20  2002/10/18 13:06:57  f8dy
added licensing information

"""
