"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

import feedvalidator
from feedvalidator.logging import *

line = "line %(line)s"
column = "column %(column)s"
occurances = " (%(msgcount)s occurrences)"

messages = {
  SAXError:                "XML Parsing error: %(exception)s",
  NotHtml:                 "Invalid HTML: %(message)s",
  UnicodeError:            "%(exception)s (maybe a high-bit character?)",
  UndefinedElement:        "Undefined %(parent)s element: %(element)s",
  MissingNamespace:        "Missing namespace for %(element)s",
  MissingElement:          "Missing %(parent)s element: %(element)s",
  MissingOptionalElement:  "%(parent)s should contain a %(element)s element",
  MissingRecommendedElement: "%(parent)s should contain a %(element)s element",
  MissingAttribute:        "Missing %(element)s attribute: %(attr)s",
  UnexpectedAttribute:     "Unexpected %(attribute)s attribute on %(element)s element",
  NoBlink:                 "There is no blink element in RSS; use blogChannel:blink instead",
  InvalidValue:            "Invalid value for %(element)s: \"%(value)s\"",
  InvalidWidth:            "%(element)s must be between 1 and 144",
  InvalidHeight:           "%(element)s must be between 1 and 400",
  InvalidHour:             "%(element)s must be between 1 and 24",
  InvalidDay:              "%(element)s must be Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday",
  InvalidInteger:          "%(element)s must be a positive integer",
  InvalidHttpGUID:         "guid must be a full URL, unless isPermaLink attribute is false",
  InvalidUpdatePeriod:     "%(element)s must be hourly, daily, weekly, monthly, or yearly",
  RecommendedWidth:        "%(element)s should be between 1 and 88",
  RecommendedHeight:       "%(element)s should be between 1 and 31",
  NotBlank:                "%(element)s can not be blank",
  AttrNotBlank:            "The %(attr)s attribute of %(element)s can not be blank",
  DuplicateElement:        "%(parent)s contains more than one %(element)s",
  DuplicateSemantics:      "A channel must not include both %(core)s and %(ext)s",
  DuplicateItemSemantics:  "An item must not include both %(core)s and %(ext)s",
  DuplicateValue:          "%(element)s values must not be duplicated within a feed",
  NonstdPrefix:            '"%(preferred)s" is the preferred prefix for the namespace "%(ns)s"',
  ReservedPrefix:          'The prefix "%(prefix)s" generally uses the namespace "%(ns)s"',
  UseModularEquivalent:    "%(ext)s should be used instead of %(core)s",
  InvalidContact:          "%(element)s must include an email address",
  InvalidLink:             "%(element)s must be a valid URL",
  InvalidFullLink:         "%(element)s must be a full and valid URL",
  InvalidW3DTFDate:        "%(element)s must be an ISO-8601 date",
  InvalidRFC2822Date:      "%(element)s must be an RFC-822 date",
  InvalidLanguage:         "%(element)s must be an ISO-639 language code",
  InvalidURLAttribute:     "%(attr)s attribute of %(element)s must be a full URL",
  InvalidIntegerAttribute: "%(attr)s attribute of %(element)s must be a positive integer",
  InvalidBooleanAttribute: "%(attr)s attribute of %(element)s must be 'true' or 'false'",
  InvalidMIMEAttribute:    "%(attr)s attribute of %(element)s must be a valid MIME type",
  ItemMustContainTitleOrDescription: "item must contain either title or description",
  ContainsHTML:            "%(element)s should not contain HTML",
  ContainsUndeclaredHTML:  "%(element)s must not contain HTML unless declared in the type attribute",
  NotEnoughHoursInTheDay:  "skipHours can not contain more than 24 hour elements",
  EightDaysAWeek:          "skipDAys can not contain more than 7 day elements",
  SecurityRisk:            "%(element)s should not contain %(tag)s tag",
  ContainsRelRef:          "%(element)s should not contain relative URL references",
  ContainsSystemEntity:    "Feeds must not contain SYSTEM entities",
  InvalidContentMode:      "mode must be 'xml', 'escaped', or 'base64'",
  InvalidMIMEType:         "Not a valid MIME type",
  NoMIMEType:              "%(element)s does not specify a MIME type",
  W3DTFDateNoTimezone:     "Date should include a timezone",
  W3DTFDateNonUTC:         "Date should be a UTC date",
  W3DTFDateNonLocal:       "Date should not be a UTC date",
  NotEscaped:              "%(element)s claims to be escaped, but isn't",
  NotInline:               "%(element)s claims to be inline, but isn't",
  NotBase64:               "%(element)s claims to be base64-encoded, but isn't",
  InvalidURN:              "%(element)s is not a valid URN",
  InvalidTAG:              "%(element)s is not a valid TAG",
  InvalidURI:              "%(element)s is not a valid URI",
  ObsoleteVersion:         "This feed is an obsolete version",
  ObsoleteNamespace:       "This feed uses an obsolete namespace",
  InvalidNamespace:        "%(element)s is in an invalid namespace: %(namespace)s",
  InvalidDoctype:          "This feed contains conflicting DOCTYPE and version information",
  MultipartInvalid:        "Multipart/alternative content can only contain other content elements",
  MultipartMissing:        "Multipart/alternative content must contain at least one content element",
  MultipartRecursion:      "Multipart/alternative content can not contain other multipart/alternative content elements",
  MultipartDuplicate:      "Multipart/alternative content can not contain multiple content elements of the same type",
  DuplicateAtomLink:       "Duplicate link with the same type and rel",
  MissingHref:             "%(element)s must have an href attribute",
  AtomLinkNotEmpty:        "%(element)s should not have text (all data is in attributes)",
  AtomLinkMissingRel:      "%(element)s must have a rel attribute",
  MissingAlternateLink:    '''%(parent)s must contain a link element with rel="alternate"''',
  BadCharacters:           '%(element)s contains bad characters',
  BadXmlVersion:           "Incorrect XML Version: %(version)s",
  InvalidAtomLinkRel:      "%(value)s is not a valid link relationship",
  HttpError:               "Server returned %(status)s"
}
 

__history__ = """
$Log$
Revision 1.9  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.8  2004/02/16 20:31:13  rubys
Message string requires a substitution type for %(value) variable

Revision 1.7  2004/02/16 20:24:00  rubys
Fix for bug 892843: FeedValidator allows arbitrary Atom link rel values

Revision 1.6  2004/02/16 16:25:26  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.5  2004/02/07 14:23:19  rubys
Fix for bug 892178: must reject xml 1.1

Revision 1.4  2004/02/07 02:15:44  rubys
Implement feature 890049: gzip compression support
Fix for bug 890054: sends incorrect user-agent

Revision 1.3  2004/02/06 18:43:18  rubys
Apply patch 886675 from Joseph Walton:
"Warn about windows-1252 presented as ISO-8859-1"

Revision 1.2  2004/02/06 15:06:10  rubys
Handle 404 Not Found errors
Applied path 891556 provided by aegrumet

Revision 1.1.1.1  2004/02/03 17:33:17  rubys
Initial import.

Revision 1.54  2003/12/12 20:37:06  f8dy
oops, URNs can contain letters after all

Revision 1.53  2003/12/12 15:53:42  f8dy
renamed source directories

Revision 1.52  2003/12/12 15:00:22  f8dy
changed blank link attribute tests to new error AttrNotBlank to distinguish them from elements that can not be blank

Revision 1.51  2003/12/12 05:57:39  f8dy
added missing messages

Revision 1.50  2003/12/12 05:42:05  rubys
Rough in some support for the new link syntax

Revision 1.49  2003/12/12 01:24:36  rubys
Multipart/alternative tests

Revision 1.48  2003/12/11 20:13:58  f8dy
feed title, copyright, and tagline may be blank

Revision 1.47  2003/12/11 18:20:46  f8dy
passed all content-related testcases

Revision 1.46  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.45  2003/12/11 06:00:51  f8dy
added tag: testcases, passed

Revision 1.44  2003/08/23 00:28:04  rubys
Validate escaped text/HTML content

Revision 1.43  2003/08/06 16:16:59  f8dy
added testcase for Netscape DOCTYPE

Revision 1.42  2003/08/05 22:09:03  f8dy
added automated message test to test output messages

Revision 1.41  2003/08/05 20:54:42  f8dy
Added message for InvalidNamespace error

Revision 1.40  2003/08/05 18:04:12  f8dy
added Atom 0.2-specific messages

Revision 1.39  2003/08/04 01:59:33  rubys
Full http and ftp URIs require two slashes

Revision 1.38  2003/08/04 00:54:35  rubys
Log every valid element (for better self validation in test cases)

Revision 1.37  2003/07/29 16:14:21  rubys
Validate urns

Revision 1.36  2003/07/29 15:15:33  f8dy
added tests for invalid URNs (may be used in entry/id of Atom feeds)

Revision 1.35  2003/07/19 21:15:08  f8dy
added tests and logging classes for duplicate guid/id values within a feed (thanks AaronSw for this idea)

Revision 1.34  2003/07/09 19:28:39  f8dy
added test cases looking at actual content vs. mode (note: not passed)

Revision 1.33  2003/07/09 03:54:39  f8dy
yet more changes to the date messages

Revision 1.32  2003/07/09 03:48:04  f8dy
more changes to pie-specific messages

Revision 1.31  2003/07/09 03:31:36  f8dy
Updated pie-specific log messages

Revision 1.30  2003/06/26 18:03:04  f8dy
add workaround for case where SAX throws UnicodeError but locator.getLineNumber() is screwy

Revision 1.29  2002/10/31 00:52:21  rubys
Convert from regular expressions to EntityResolver for detecting
system entity references

Revision 1.28  2002/10/30 23:02:30  f8dy
*** empty log message ***

Revision 1.27  2002/10/30 15:44:48  rubys
Improve error messages for relative references: error message should
be gramatically correct.  Remove "hidden" fields prevented duplicate
errors from being flagged as such.

Revision 1.26  2002/10/27 18:54:30  rubys
Issue warnings for relative references in descriptions

Revision 1.25  2002/10/22 22:37:21  f8dy
tweaked ReservedPrefix message one last time

Revision 1.24  2002/10/22 19:32:19  f8dy
made friendlier messages for NonStdPrefix and ReservedPrefix

Revision 1.23  2002/10/22 16:24:04  f8dy
added UnicodeError support for feeds that declare utf-8 but use 8-bit characters anyway

Revision 1.22  2002/10/19 21:08:02  f8dy
added "special case" functionality for the web front end

Revision 1.21  2002/10/18 19:28:43  f8dy
added testcases for mod_syndication and passed them

Revision 1.20  2002/10/18 14:17:30  f8dy
added tests for language/dc:language (must be valid ISO-639 language code
plus optional country code) and passed them

Revision 1.19  2002/10/18 13:06:57  f8dy
added licensing information

"""
