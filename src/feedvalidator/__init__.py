"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

import socket
if hasattr(socket, 'setdefaulttimeout'):
  socket.setdefaulttimeout(10)
  Timeout = socket.timeout
else:
  import timeoutsocket
  timeoutsocket.setDefaultSocketTimeout(10)
  Timeout = timeoutsocket.Timeout

import urllib2
import logging
from logging import *
from xml.sax import SAXParseException
from xml.sax.xmlreader import InputSource
import re
import xmlEncoding
import mediaTypes

MAXDATALENGTH = 200000

def _validate(aString, firstOccurrenceOnly, loggedEvents, base):
  """validate RSS from string, returns validator object"""
  from xml.sax import make_parser, handler
  from base import SAXDispatcher
  from exceptions import UnicodeError
  from cStringIO import StringIO

  # By now, aString should be Unicode
  source = InputSource()
  source.setByteStream(StringIO(xmlEncoding.asUTF8(aString)))

  validator = SAXDispatcher(base)
  validator.setFirstOccurrenceOnly(firstOccurrenceOnly)

  validator.loggedEvents += loggedEvents

  xmlver = re.match("^<\?\s*xml\s+version\s*=\s*['\"]([-a-zA-Z0-9_.:]*)['\"]",aString)
  if xmlver and xmlver.group(1)<>'1.0':
    validator.log(logging.BadXmlVersion({"version":xmlver.group(1)}))

  try:
    from xml.sax.expatreader import ExpatParser
    class fake_dtd_parser(ExpatParser):
      def reset(self):
        ExpatParser.reset(self)
        self._parser.UseForeignDTD(1)
    parser = fake_dtd_parser()
  except:
    parser = make_parser()

  parser.setFeature(handler.feature_namespaces, 1)
  parser.setContentHandler(validator)
  parser.setErrorHandler(validator)
  parser.setEntityResolver(validator)
  if hasattr(parser, '_ns_stack'):
    # work around bug in built-in SAX parser (doesn't recognize xml: namespace)
    # PyXML doesn't have this problem, and it doesn't have _ns_stack either
    parser._ns_stack.append({'http://www.w3.org/XML/1998/namespace':'xml'})

  def xmlvalidate(log):
    import libxml2
    from StringIO import StringIO
    from random import random

    prefix="...%s..." % str(random()).replace('0.','')
    msg=[]
    libxml2.registerErrorHandler(lambda msg,str: msg.append(str), msg)

    input = libxml2.inputBuffer(StringIO(xmlEncoding.asUTF8(aString)))
    reader = input.newTextReader(prefix)
    reader.SetParserProp(libxml2.PARSER_VALIDATE, 1)
    ret = reader.Read()
    while ret == 1: ret = reader.Read()

    msg=''.join(msg)
    for line in msg.splitlines():
      if line.startswith(prefix): log(line.split(':',4)[-1].strip())
  validator.xmlvalidator=xmlvalidate

  try:
    parser.parse(source)
  except SAXParseException:
    pass
  except UnicodeError:
    import sys
    exctype, value = sys.exc_info()[:2]
    validator.log(logging.UnicodeError({"exception":value}))

  if validator.getFeedType() == TYPE_RSS1:
    try:
      from rdflib.syntax.parsers.RDFXMLHandler import RDFXMLHandler

      class Handler(RDFXMLHandler):
        ns_prefix_map = {}
        prefix_ns_map = {}
        def add(self, triple): pass
        def __init__(self, dispatcher):
          RDFXMLHandler.__init__(self, self)
          self.dispatcher=dispatcher
        def error(self, message):
          self.dispatcher.log(InvalidRDF({"message": message}))
    
      source.getByteStream().reset()
      parser.reset()
      parser.setContentHandler(Handler(parser.getContentHandler()))
      parser.setErrorHandler(handler.ErrorHandler())
      parser.parse(source)
    except:
      pass

  return validator

def validateStream(aFile, firstOccurrenceOnly=0, contentType=None, base=""):
  loggedEvents = []

  if contentType:
    (mediaType, charset) = mediaTypes.checkValid(contentType, loggedEvents)
  else:
    (mediaType, charset) = (None, None)

  rawdata = aFile.read(MAXDATALENGTH)
  if aFile.read(1):
    raise ValidationFailure(logging.ValidatorLimit({'limit': 'feed length > ' + str(MAXDATALENGTH) + ' bytes'}))

  rawdata = xmlEncoding.decode(mediaType, charset, rawdata, loggedEvents, fallback='utf-8')

  validator = _validate(rawdata, firstOccurrenceOnly, loggedEvents, base)

  if mediaType and validator.feedType:
    mediaTypes.checkAgainstFeedType(mediaType, validator.feedType, validator.loggedEvents)

  return {"feedType":validator.feedType, "loggedEvents":validator.loggedEvents}

def validateString(aString, firstOccurrenceOnly=0, fallback=None, base=""):
  loggedEvents = []
  if type(aString) != unicode:
    aString = xmlEncoding.decode("", None, aString, loggedEvents, fallback)

  if aString is not None:
    validator = _validate(aString, firstOccurrenceOnly, loggedEvents, base)
    return {"feedType":validator.feedType, "loggedEvents":validator.loggedEvents}
  else:
    return {"loggedEvents": loggedEvents}

def validateURL(url, firstOccurrenceOnly=1, wantRawData=0):
  """validate RSS from URL, returns events list, or (events, rawdata) tuple"""
  loggedEvents = []
  request = urllib2.Request(url)
  request.add_header("Accept-encoding", "gzip, deflate")
  request.add_header("User-Agent", "FeedValidator/1.3")
  try:
    usock = urllib2.urlopen(request)
    rawdata = usock.read(MAXDATALENGTH)
    if usock.read(1):
      raise ValidationFailure(logging.ValidatorLimit({'limit': 'feed length > ' + str(MAXDATALENGTH) + ' bytes'}))

    # check for temporary redirects
    if usock.geturl()<>request.get_full_url():
      from httplib import HTTPConnection
      spliturl=url.split('/',3)
      if spliturl[0]=="http:":
        conn=HTTPConnection(spliturl[2])
        conn.request("GET",'/'+spliturl[3].split("#",1)[0])
        resp=conn.getresponse()
        if resp.status<>301:
          loggedEvents.append(TempRedirect({}))

  except urllib2.HTTPError, status:
    raise ValidationFailure(logging.HttpError({'status': status}))
  except urllib2.URLError, x:
    raise ValidationFailure(logging.HttpError({'status': x.reason}))
  except Timeout, x:
    raise ValidationFailure(logging.IOError({"message": 'Server timed out', "exception":x}))

  if usock.headers.get('content-encoding', None) == None:
    loggedEvents.append(Uncompressed({}))

  if usock.headers.get('content-encoding', None) == 'gzip':
    import gzip, StringIO
    try:
      rawdata = gzip.GzipFile(fileobj=StringIO.StringIO(rawdata)).read()
    except:
      import sys
      exctype, value = sys.exc_info()[:2]
      event=logging.IOError({"message": 'Server response declares Content-Encoding: gzip', "exception":value})
      raise ValidationFailure(event)

  if usock.headers.get('content-encoding', None) == 'deflate':
    import zlib
    try:
      rawdata = zlib.decompress(rawdata, -zlib.MAX_WBITS)
    except:
      import sys
      exctype, value = sys.exc_info()[:2]
      event=logging.IOError({"message": 'Server response declares Content-Encoding: deflate', "exception":value})
      raise ValidationFailure(event)

  mediaType = None
  charset = None

  # Is the Content-Type correct?
  contentType = usock.headers.get('content-type', None)
  if contentType:
    (mediaType, charset) = mediaTypes.checkValid(contentType, loggedEvents)

  # Check for malformed HTTP headers
  for (h, v) in usock.headers.items():
    if (h.find(' ') >= 0):
      loggedEvents.append(HttpProtocolError({'header': h}))

  usock.close()

  rawdata = xmlEncoding.decode(mediaType, charset, rawdata, loggedEvents, fallback='utf-8')

  if rawdata is None:
    return {'loggedEvents': loggedEvents}

  rawdata = rawdata.replace('\r\n', '\n').replace('\r', '\n') # normalize EOL
  validator = _validate(rawdata, firstOccurrenceOnly, loggedEvents, url)

  # Warn about mismatches between media type and feed version
  if mediaType and validator.feedType:
    mediaTypes.checkAgainstFeedType(mediaType, validator.feedType, validator.loggedEvents)

  params = {"feedType":validator.feedType, "loggedEvents":validator.loggedEvents}
  if wantRawData:
    params['rawdata'] = rawdata
  return params

__all__ = ['base',
           'channel',
           'compatibility',
           'image',
           'item',
           'logging',
           'rdf',
           'root',
           'rss',
           'skipHours',
           'textInput',
           'util',
           'validators',
           'validateURL',
           'validateString']

__history__ = """
$Log$
Revision 1.34  2005/08/20 03:58:58  rubys
white-space + xml:base

Revision 1.33  2005/08/18 17:22:59  rubys
Better exception handling when timeoutsocket is not necessary (Python 2.3+)

Revision 1.32  2005/08/16 01:14:52  rubys
fix to bug 1214019: https support

Revision 1.31  2005/08/01 14:23:44  rubys
Provide more helpful advice when people attempt to use XHTML named entity
references inside their feeds.

Addresses bugs: 1242762, 1243771, 1249420

Revision 1.30  2005/01/29 05:41:12  rubys
Fix for [ 1042359 ] invalid RSS 1.0 not flagged as invalid

Revision 1.29  2005/01/26 18:37:13  rubys
Add a 'real' RDF parser for RSS 1.x feeds

Revision 1.28  2005/01/07 18:02:57  josephw
Check for bad HTTP headers, specifically where the name includes a space.

Revision 1.27  2004/09/20 17:44:55  josephw
Show the error when downloading the feed times out.

Revision 1.26  2004/07/28 12:24:25  rubys
Partial support for verifing xml:lang

Revision 1.25  2004/07/28 04:41:55  rubys
Informational messages for text/xml with no charset and uncompressed responses

Revision 1.24  2004/07/28 04:07:55  rubys
Detect temporary redirects

Revision 1.23  2004/07/16 22:04:03  rubys
Deflate support

Revision 1.22  2004/07/09 02:43:23  rubys
Warn if non-ASCII characters are present in a feed served as text/xml
with no explicit charset defined in the HTTP headers.

Revision 1.21  2004/07/04 00:16:51  josephw
Fixed '?manual=1' mode and validation of POSTed feeds.

Revision 1.20  2004/07/03 23:39:21  josephw
Implemented validateStream.

Revision 1.19  2004/07/03 22:58:50  josephw
Refactor media type checks into their own module.

Revision 1.18  2004/06/21 22:28:50  rubys
Fix 976875: XML Validation
Validation is only performed if libxml2 is installed (libxml2 is installed
on both feeds.archive.org and feedvalidator.org) and a DOCTYPE is present.

Revision 1.17  2004/05/30 17:54:22  josephw
Warn when the content type, although valid, doesn't match the feed type.

Revision 1.16  2004/05/12 21:42:18  josephw
Report failure if a feed is larger than MAXDATALENGTH.

Revision 1.15  2004/04/30 09:05:14  josephw
Decode Unicode before parsing XML, to cover cases Expat doesn't deal with.
Present the report as UTF-8, to better deal with Unicode feeds.

Revision 1.14  2004/04/29 20:47:09  rubys
Try harder to handle obscure encodings

Revision 1.13  2004/04/24 01:50:32  rubys
Attempt to respect RFC 3023.

Revision 1.12  2004/04/10 16:34:37  rubys
Allow application/rdf+xml

Revision 1.11  2004/03/30 09:03:30  josephw
Check Content-Type against valid feed types, and against the actual XML
character encoding.

Revision 1.10  2004/03/30 08:26:28  josephw
Check XML character encoding before parsing.

Revision 1.9  2004/03/28 11:37:41  josephw
Replaced 'from logging import *', so validtest.py works again.

Revision 1.8  2004/03/28 10:58:07  josephw
Catch and show ValidationFailure in check.cgi. Changed text_html.py
to allow global events, with no specific document location. Moved DOCSURL
into config.py. Moved trivial HTML list-delimiter definitions into
text_html.py.

Revision 1.7  2004/03/28 09:49:58  josephw
Accept URLs relative to the current directory in demo.py. Added a top-level
exception to indicate validation failure; catch and print it in demo.py.

Revision 1.6  2004/03/23 02:03:00  rubys
Dummy up line, column and other info needed for cgi

Revision 1.5  2004/03/23 01:33:04  rubys
Apply patch from Joseph Walton to provide better error reporting when
servers are misconfigured for gzip encoding.

Revision 1.4  2004/02/07 14:23:19  rubys
Fix for bug 892178: must reject xml 1.1

Revision 1.3  2004/02/07 02:15:43  rubys
Implement feature 890049: gzip compression support
Fix for bug 890054: sends incorrect user-agent

Revision 1.2  2004/02/06 15:06:10  rubys
Handle 404 Not Found errors
Applied path 891556 provided by aegrumet

Revision 1.1.1.1  2004/02/03 17:33:14  rubys
Initial import.

Revision 1.24  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.23  2003/08/09 17:09:34  rubys
Remove misleading mapping of LookupError to UnicodeError

Revision 1.22  2003/08/06 05:40:00  f8dy
patch to send a real User-Agent on HTTP requests

Revision 1.21  2003/08/05 18:51:38  f8dy
added hack to work around bug in built-in SAX parser (doesn't recognize xml: namespace)

Revision 1.20  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.19  2002/12/22 19:01:17  rubys
Integrate in SOAP support

Revision 1.18  2002/11/04 01:06:43  rubys
Remove remaining call to preValidate

Revision 1.17  2002/11/04 00:28:55  rubys
Handle LookupError (e.g., unknown encoding)

Revision 1.16  2002/10/31 00:52:21  rubys
Convert from regular expressions to EntityResolver for detecting
system entity references

Revision 1.15  2002/10/30 23:03:01  f8dy
security fix: external (SYSTEM) entities

Revision 1.14  2002/10/22 19:41:07  f8dy
normalize line endings before parsing (SAX parser is not Mac-CR-friendly)

Revision 1.13  2002/10/22 16:35:11  f8dy
commented out fallback except (caller handles it gracefully anyway)

Revision 1.12  2002/10/22 16:24:04  f8dy
added UnicodeError support for feeds that declare utf-8 but use 8-bit characters anyway

Revision 1.11  2002/10/18 13:06:57  f8dy
added licensing information

"""
