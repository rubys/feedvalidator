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
  SAXError:                "XML parsing error: %(exception)s",
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
  InvalidValue:            "Invalid value for %(attr)s: \"%(value)s\"",
  InvalidWidth:            "%(element)s must be between 1 and 144",
  InvalidHeight:           "%(element)s must be between 1 and 400",
  InvalidHour:             "%(element)s must be between 1 and 24",
  InvalidDay:              "%(element)s must be Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday",
  InvalidInteger:          "%(element)s must be an integer",
  InvalidPositiveInteger:  "%(element)s must be a positive integer",
  InvalidLatitude:         "%(element)s must be between -90 and 90",
  InvalidLongitude:        "%(element)s must be between -180 and 180",
  InvalidHttpGUID:         "guid must be a full URL, unless isPermaLink attribute is false",
  InvalidUpdatePeriod:     "%(element)s must be hourly, daily, weekly, monthly, or yearly",
  NotBlank:                "%(element)s should not be blank",
  AttrNotBlank:            "The %(attr)s attribute of %(element)s should not be blank",
  DuplicateElement:        "%(parent)s contains more than one %(element)s",
  DuplicateSemantics:      "A channel must not include both %(core)s and %(ext)s",
  DuplicateItemSemantics:  "An item must not include both %(core)s and %(ext)s",
  DuplicateValue:          "%(element)s values must not be duplicated within a feed",
  NonstdPrefix:            '"%(preferred)s" is the preferred prefix for the namespace "%(ns)s"',
  ReservedPrefix:          'The prefix "%(prefix)s" generally uses the namespace "%(ns)s"',
  InvalidContact:          "%(element)s must include an email address",
  InvalidAddrSpec:         "%(element)s must be an email address",
  InvalidLink:             "%(element)s must be a valid URI",
  InvalidFullLink:         "%(element)s must be a full and valid URL",
  InvalidISO8601Date:      "%(element)s must be an ISO8601 date",
  InvalidW3CDTFDate:        "%(element)s must be an W3CDTF date",
  InvalidRFC2822Date:      "%(element)s must be an RFC-822 date-time",
  InvalidRFC3339Date:      "%(element)s must be an RFC-3339 date-time",
  InvalidLanguage:         "%(element)s must be an ISO-639 language code",
  InvalidURIAttribute:     "%(attr)s attribute of %(element)s must be a valid URI",
  InvalidURLAttribute:     "%(attr)s attribute of %(element)s must be a full URL",
  InvalidIntegerAttribute: "%(attr)s attribute of %(element)s must be a positive integer",
  InvalidBooleanAttribute: "%(attr)s attribute of %(element)s must be 'true' or 'false'",
  InvalidMIMEAttribute:    "%(attr)s attribute of %(element)s must be a valid MIME type",
  ItemMustContainTitleOrDescription: "item must contain either title or description",
  ContainsHTML:            "%(element)s should not contain HTML",
  ContainsUndeclaredHTML:  "%(element)s should not contain HTML unless declared in the type attribute",
  NotEnoughHoursInTheDay:  "skipHours can not contain more than 24 hour elements",
  EightDaysAWeek:          "skipDays can not contain more than 7 day elements",
  SecurityRisk:            "%(element)s should not contain %(tag)s tag",
  ContainsRelRef:          "%(element)s should not contain relative URL references",
  ContainsSystemEntity:    "Feeds must not contain SYSTEM entities",
  InvalidContentMode:      "mode must be 'xml', 'escaped', or 'base64'",
  InvalidMIMEType:         "Not a valid MIME type",
  NoMIMEType:              "%(element)s does not specify a MIME type",
  W3CDTFDateNoTimezone:     "Date should include a timezone",
  W3CDTFDateNonUTC:         "Date should be a UTC date",
  W3CDTFDateNonLocal:       "Date should not be a UTC date",
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
  DuplicateAtomLink:       "Duplicate alternate links with the same type and hreflang",
  MissingHref:             "%(element)s must have an href attribute",
  AtomLinkNotEmpty:        "%(element)s should not have text (all data is in attributes)",
  AtomLinkMissingRel:      "%(element)s must have a rel attribute",
  MissingAlternateLink:    '''%(parent)s must contain a link element with rel="alternate"''',
  BadCharacters:           '%(element)s contains bad characters',
  BadXmlVersion:           "Incorrect XML Version: %(version)s",
  InvalidAtomLinkRel:      "%(value)s is not a valid link relationship",
  HttpError:               "Server returned %(status)s",
  IOError:                 "%(exception)s (%(message)s; misconfigured server?)",
  ObscureEncoding:         "Obscure XML character encoding: %(encoding)s",
  NonstdEncoding:          "This encoding is not mandated by the XML specification: %(encoding)s",
  UnexpectedContentType:   '%(type)s should not be served with the "%(contentType)s" media type',
  EncodingMismatch:        'Your feed appears to be encoded as "%(encoding)s", but your server is reporting "%(charset)s"',
  UnknownEncoding:         "Unknown XML character encoding: %(encoding)s",
  NotSufficientlyUnique:   "The specified guid is not sufficiently unique",
  MissingEncoding:         "No character encoding was specified",
  UnexpectedText:          "Unexpected Text",
  ValidatorLimit:          "Unable to validate, due to hardcoded resource limits (%(limit)s)",
  TempRedirect:            "Temporary redirect",
  TextXml:                 "Content type of text/xml with no charset",
  Uncompressed:            "Response is not compressed",
  HttpProtocolError:       'Response includes bad HTTP header name: "%(header)s"',
  NonCanonicalURI:         'Identifier "%(uri)s" is not in canonical form (should be "%(curi)s")',
  InvalidRDF:              'RDF parsing error: %(message)s',
  UndecipherableSpecification: 'The specification of the %(element)s element is unclear',
  InvalidDuration:         'Invalid duration: "%(value)s"',
  InvalidYesNo:            '%(element)s must be "Yes" or "No"',
  TooLong:                 'length of %(len)d exceeds the maximum allowable for %(element)s of %(max)d',
  InvalidItunesCategory:   '%(text)s is not one of the predefined iTunes categories or sub-categories',
  InvalidKeywords:         'Keywords must be words separated by spaces',
  InvalidTextType:         'type attribute must be "text", "html", or "xhtml"',
  MissingXhtmlDiv:         'Missing xhtml:div element',
  MissingSelf:             'Missing atom:link with rel="self"',
  DuplicateEntries:        'Two entries with the same id',
  MisplacedMetadata:       '%(element)s must appear before all entries',
  MissingTextualContent:   'Missing textual content',
  MissingContentOrAlternate: 'Missing content or alternate link',
  MissingSourceElement:    "Missing %(parent)s element: %(element)s",
  MissingTypeAttr:         "Missing %(element)s attribute: %(attr)s",
  HtmlFragment:            "%(type)s type used for a document fragment",
  DuplicateUpdated:        "Two entries with the same value for atom:updated",
  UndefinedNamedEntity:    "Undefined named entity: %(value)s",
  ImplausibleDate:         "Implausible date: %(value)s",
  UnexpectedWhitespace:    "Whitespace not permitted here",
}
 

__history__ = """
$Log$
Revision 1.50  2005/08/20 03:58:58  rubys
white-space + xml:base

Revision 1.49  2005/08/08 01:24:13  rubys
Better error reporting on invalid email addr-spec

Revision 1.48  2005/08/07 01:08:14  rubys
I had a report of an uncaught Y2K error.  At the same time, catch
future dates and update the documentation to reflect RFC 3339 as
opposed to various related standards.

Revision 1.47  2005/08/01 14:23:45  rubys
Provide more helpful advice when people attempt to use XHTML named entity
references inside their feeds.

Addresses bugs: 1242762, 1243771, 1249420

Revision 1.46  2005/07/28 23:56:04  rubys
Duplicate Updated warning

Revision 1.45  2005/07/28 15:25:12  rubys
Warn on use of html mime types containing fragments

Revision 1.44  2005/07/25 01:37:55  rubys
Nested invalid iTunes categories and cleanup

Revision 1.43  2005/07/25 00:40:55  rubys
Convert errors to warnings

Revision 1.42  2005/07/23 16:08:42  rubys
Align the documention with Atom 1.0

Revision 1.41  2005/07/19 19:57:46  rubys
Few things I spotted...

Revision 1.40  2005/07/18 23:22:12  rubys
Atom 4.2.2.1, 4.2.4, 4.2.5

Revision 1.39  2005/07/18 12:20:46  rubys
Atom 1.0 section 4.1.2

Revision 1.38  2005/07/18 10:14:48  rubys
Warn on same document references

Revision 1.37  2005/07/17 23:22:44  rubys
Atom 1.0 section 4.1.1.1

Revision 1.36  2005/07/17 18:49:18  rubys
Atom 1.0 section 4.1

Revision 1.35  2005/07/16 22:01:14  rubys
Atom 1.0 text constructs and relative URIs

Revision 1.34  2005/07/16 14:40:09  rubys
More Atom 1.0 support

Revision 1.33  2005/07/08 14:56:13  rubys
Allow slash:comments to be zero.

Revision 1.32  2005/07/06 19:35:29  rubys
Validate iTunes keywords

Revision 1.31  2005/07/04 22:54:31  philor
Support rest of dc, dcterms, geo, geourl, icbm, and refactor out common extension elements

Revision 1.30  2005/07/03 01:31:17  rubys
Improve documentation and test coverage on itunes categories.

Revision 1.29  2005/07/01 23:55:30  rubys
Initial support for itunes

Revision 1.28  2005/06/24 22:21:24  rubys
s/RFC 822 date/RFC 822 date-time/g

Revision 1.27  2005/01/26 18:37:13  rubys
Add a 'real' RDF parser for RSS 1.x feeds

Revision 1.26  2005/01/22 23:45:36  rubys
pass last rss11 test case (neg-ext-notrdf.xml)

Revision 1.25  2005/01/21 23:18:44  josephw
Add logging, documentation and tests for canonical URIs.

Revision 1.24  2005/01/07 18:02:58  josephw
Check for bad HTTP headers, specifically where the name includes a space.

Revision 1.23  2004/08/06 10:37:54  rubys
Make it more clear that http only accepts double quotes

Revision 1.22  2004/07/28 04:41:55  rubys
Informational messages for text/xml with no charset and uncompressed responses

Revision 1.21  2004/07/28 04:07:55  rubys
Detect temporary redirects

Revision 1.20  2004/07/28 02:23:42  rubys
Remove some experimental rules

Revision 1.19  2004/07/12 04:15:12  rubys
s/W3DTF/W3CDTF/g

Revision 1.18  2004/05/30 17:54:22  josephw
Warn when the content type, although valid, doesn't match the feed type.

Revision 1.17  2004/05/12 21:42:19  josephw
Report failure if a feed is larger than MAXDATALENGTH.

Revision 1.16  2004/04/30 11:50:02  rubys
Detect stray text outside of elements

Revision 1.15  2004/04/30 07:48:48  josephw
Added MissingEncoding, for when there's no apparent declaration of
encoding.

Revision 1.14  2004/04/05 23:54:42  rubys
Fix bug 929794: verify version attribute

Revision 1.13  2004/03/30 02:42:40  rubys
Flag instances of small positive integers as guids as being "not sufficiently
unique".

Revision 1.12  2004/03/28 11:39:45  josephw
Added logging events and documentation for encoding and media type checks.

Revision 1.11  2004/03/23 01:33:05  rubys
Apply patch from Joseph Walton to provide better error reporting when
servers are misconfigured for gzip encoding.

Revision 1.10  2004/02/18 16:12:14  rubys
Make the distiction between W3CDTF and ISO8601 clearer in the docs.

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
