"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

import feedvalidator
import sys
import os
import urllib
import urllib2
import urlparse

if __name__ == '__main__':
  # arg 1 is URL to validate
  link = sys.argv[1:] and sys.argv[1] or 'http://www.intertwingly.net/blog/index.rss2'
  link = urlparse.urljoin('file:' + urllib.pathname2url(os.getcwd()) + '/', link)
  print 'Validating %s' % link

  try:
    events = feedvalidator.validateURL(link, firstOccurrenceOnly=1)['loggedEvents']
  except feedvalidator.logging.ValidationFailure, vf:
    events = [vf.event]

  # (optional) arg 2 is compatibility level
  # "A" is most basic level
  # "AA" mimics online validator
  # "AAA" is experimental; these rules WILL change or disappear in future versions
  from feedvalidator import compatibility
  filter = sys.argv[2:] and sys.argv[2] or "AA"
  filterFunc = getattr(compatibility, filter)
  events = filterFunc(events)

  from feedvalidator.formatter.text_plain import Formatter
  output = Formatter(events)
  if output:
      print "\n".join(output)
      sys.exit(1)
  else:
      print "No errors or warnings"

__history__ = """
$Log$
Revision 1.5  2004/03/28 09:49:58  josephw
Accept URLs relative to the current directory in demo.py. Added a top-level
exception to indicate validation failure; catch and print it in demo.py.

Revision 1.4  2004/02/21 16:30:21  rubys
Apply patch 901736: Make demo.py return meaningful exit status on erro

Revision 1.3  2004/02/07 02:15:43  rubys
Implement feature 890049: gzip compression support
Fix for bug 890054: sends incorrect user-agent

Revision 1.2  2004/02/06 15:06:09  rubys
Handle 404 Not Found errors
Applied path 891556 provided by aegrumet

Revision 1.1.1.1  2004/02/03 17:33:14  rubys
Initial import.

Revision 1.3  2003/12/12 15:53:42  f8dy
renamed source directories

Revision 1.2  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.1  2003/08/06 16:56:14  f8dy
combined pievalidtest and rssvalidtest, renamed rssdemo to demo

Revision 1.13  2003/07/16 19:47:15  rubys
Remove debug statement

Revision 1.12  2003/07/10 21:16:33  rubys
Get rssdemo back on its feet...

Revision 1.11  2002/10/20 04:47:21  f8dy
*** empty log message ***

Revision 1.10  2002/10/20 04:41:21  f8dy
*** empty log message ***

Revision 1.9  2002/10/20 04:36:09  f8dy
cleaned up for public distribution

Revision 1.8  2002/10/18 13:06:57  f8dy
added licensing information

"""
