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
from logging import UnexpectedContentType, TYPE_RSS1, TYPE_RSS2, TYPE_ATOM

# Is the Content-Type correct?
def checkValid(contentType, loggedEvents):
  (mediaType, params) = parse_header(contentType)
  if not(mediaType.lower() in ['text/xml', 'application/xml', 'application/rss+xml', 'application/rdf+xml', 'application/x.atom+xml', 'application/atom+xml']):
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
    

__history__ = """
$Log$
Revision 1.3  2005/07/17 18:53:02  josephw
Clarify that only Atom 1.0 may use the Atom media type.

Revision 1.2  2004/07/06 14:23:17  josephw
Revert to previous behaviour, where text/* does not force charset=US-ASCII.

Revision 1.1  2004/07/03 22:58:50  josephw
Refactor media type checks into their own module.

"""
