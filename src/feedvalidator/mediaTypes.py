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

# Is the Content-Type correct?
def checkValid(contentType, loggedEvents):
  (mediaType, params) = parse_header(contentType)
  if not(mediaType.lower() in ['text/xml', 'application/xml', 'application/rss+xml', 'application/rdf+xml', 'application/x.atom+xml', 'application/atom+xml', 'text/x-opml']):
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
