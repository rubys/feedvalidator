"""
$Id$
This module deals with valid internet media types for feeds.
"""

__author__ = "Joseph Walton <http://www.kafsemo.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2004 Joseph Walton"
__license__ = "Python"

from cgi import parse_header
from logging import UnexpectedContentType, TYPE_RSS1, TYPE_RSS2, TYPE_ATOM, TYPE_OPML

FEED_TYPES = [
  'text/xml', 'application/xml', 'application/rss+xml', 'application/rdf+xml',
  'application/atom+xml', 'text/x-opml'
]

# Is the Content-Type correct?
def checkValid(contentType, loggedEvents):
  (mediaType, params) = parse_header(contentType)
  if mediaType.lower() not in FEED_TYPES:
    loggedEvents.append(UnexpectedContentType({"type": "Feeds", "contentType": contentType}))
  if 'charset' in params:
    charset = params['charset']
  elif mediaType.lower().startswith('text/'):
#    charset = 'US-ASCII'
    charset = None
  else:
    charset = None

  return (mediaType, charset)

# Warn about mismatches between media type and feed version
def checkAgainstFeedType(mediaType, feedType, loggedEvents):
  mtl = mediaType.lower()

  if mtl in ['application/x.atom+xml', 'application/atom+xml']:
    if feedType != TYPE_ATOM:
      loggedEvents.append(UnexpectedContentType({"type": 'Non-Atom 1.0 feeds', "contentType": mediaType}))
  elif mtl == 'application/rdf+xml':
    if feedType != TYPE_RSS1:
      loggedEvents.append(UnexpectedContentType({"type": 'Non-RSS 1.0 feeds', "contentType": mediaType}))
  elif mtl == 'application/rss+xml':
    if feedType not in [TYPE_RSS1, TYPE_RSS2]:
      loggedEvents.append(UnexpectedContentType({"type": 'Non-RSS feeds', "contentType": mediaType}))
  elif mtl == 'text/x-opml':
    if feedType not in [TYPE_OPML]:
      loggedEvents.append(UnexpectedContentType({"type": 'Non-OPML feeds', "contentType": mediaType}))

# warn if a non-specific media type is used without a 'marker'
def contentSniffing(mediaType, rawdata, loggedEvents):
  if mediaType not in FEED_TYPES: return
  if mediaType == 'application/atom+xml': return
  if mediaType == 'application/rss+xml': return

  block = rawdata[:512]

  if block.find('<rss') >= 0: return
  if block.find('<feed') >= 0: return
  if (block.find('<rdf:RDF') >=0 and 
      block.find('http://www.w3.org/1999/02/22-rdf-syntax-ns#') >= 0 and
      block.find( 'http://purl.org/rss/1.0/')): return

  from logging import NonSpecificMediaType
  loggedEvents.append(NonSpecificMediaType({"contentType": mediaType}))
