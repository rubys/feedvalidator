"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

# feed types
TYPE_UNKNOWN = 0
TYPE_RSS1 = 1
TYPE_RSS2 = 2
TYPE_ATOM = 3
TYPE_PIE  = 4
TYPE_OPML = 9

FEEDTYPEDISPLAY = {0:"(unknown type)", 1:"RSS", 2:"RSS", 3:"Atom 1.0", 4:"Atom 0.3", 9:"OPML"}

VALIDFEEDGRAPHIC = {0:"", 1:"valid-rss.png", 2:"valid-rss.png", 3:"valid-atom.png", 4:"valid-atom.png", 9:"valid-opml.gif"}

#
# logging support
#

class LoggedEvent:
  def __init__(self, params):
    self.params = params
class Info(LoggedEvent): pass
class Warning(LoggedEvent): pass
class Error(LoggedEvent): pass

class ValidationFailure(Exception):
  def __init__(self, event):
    self.event = event

###################### error ######################

class SAXError(Error): pass
class UnicodeError(Error): pass
class MissingNamespace(SAXError): pass
class UndefinedNamedEntity(SAXError): pass

class UndefinedElement(Error): pass
class NoBlink(UndefinedElement): pass
class MissingAttribute(Error): pass
class UnexpectedAttribute(Error): pass
class DuplicateElement(Error): pass
class NotEnoughHoursInTheDay(Error): pass
class EightDaysAWeek(Error): pass

class InvalidValue(Error): pass
class InvalidContact(InvalidValue): pass
class InvalidAddrSpec(InvalidContact): pass
class InvalidLink(InvalidValue): pass
class InvalidFullLink(InvalidLink): pass
class InvalidISO8601Date(InvalidValue): pass
class InvalidW3CDTFDate(InvalidISO8601Date): pass
class InvalidRFC2822Date(InvalidValue): pass
class InvalidRFC3339Date(InvalidValue): pass
class InvalidURIAttribute(InvalidLink): pass
class InvalidURLAttribute(InvalidURIAttribute): pass
class InvalidIntegerAttribute(InvalidValue): pass
class InvalidBooleanAttribute(InvalidValue): pass
class InvalidMIMEAttribute(InvalidValue): pass
class InvalidInteger(InvalidValue): pass
class InvalidPositiveInteger(InvalidInteger): pass
class InvalidWidth(InvalidValue): pass
class InvalidHeight(InvalidValue): pass
class InvalidHour(InvalidValue): pass
class InvalidDay(InvalidValue): pass
class InvalidHttpGUID(InvalidValue): pass
class InvalidLanguage(InvalidValue): pass
class InvalidUpdatePeriod(InvalidValue): pass
class InvalidItunesCategory(InvalidValue): pass
class InvalidYesNo(InvalidValue): pass
class InvalidDuration(InvalidValue): pass
class TooLong(InvalidValue): pass
class InvalidKeywords(InvalidValue): pass
class InvalidTextType(InvalidValue): pass

class UndecipherableSpecification(Error): pass

class MissingElement(Error): pass
class MissingChannel(MissingElement): pass
class MissingDescription(MissingElement): pass
class MissingLink(MissingElement): pass
class MissingTitle(MissingElement): pass
class ItemMustContainTitleOrDescription(MissingElement): pass
class MissingXhtmlDiv(MissingElement): pass
class MissingContentOrAlternate(MissingElement): pass

class FatalSecurityRisk(Error): pass
class ContainsSystemEntity(Info): pass

class DuplicateValue(InvalidValue): pass

class InvalidDoctype(Error): pass
class BadXmlVersion(Error): pass

class MultipartInvalid(Error): pass
class MultipartMissing(Error): pass
class MultipartRecursion(Error): pass
class MultipartDuplicate(Error): pass

class DuplicateAtomLink(Error): pass
class MissingHref(MissingAttribute): pass
class AtomLinkNotEmpty(Warning): pass
class AtomLinkMissingRel(Error): pass
class InvalidAtomLinkRel(Error): pass
class MissingAlternateLink(Error): pass

class HttpError(Error): pass
class IOError(Error): pass
class UnknownEncoding(Error): pass

class UnexpectedText(Error): pass
class UnexpectedWhitespace(Error): pass

class ValidatorLimit(Error): pass

class HttpProtocolError(Error): pass

class InvalidRDF(Error): pass

class InvalidLatitude(Error): pass
class InvalidLongitude(Error): pass

class MisplacedMetadata(Error): pass

###################### warning ######################

class DuplicateSemantics(Warning): pass
class DuplicateItemSemantics(DuplicateSemantics): pass

class ContainsRelRef(Warning): pass

class ReservedPrefix(Warning): pass

class NotSufficientlyUnique(Warning): pass
class ImplausibleDate(Warning): pass

class SecurityRisk(Warning): pass
class ContainsScript(SecurityRisk): pass
class ContainsMeta(SecurityRisk): pass
class ContainsEmbed(SecurityRisk): pass
class ContainsObject(SecurityRisk): pass

class BadCharacters(Warning): pass
class ObscureEncoding(Warning): pass
class UnexpectedContentType(Warning): pass
class EncodingMismatch(Warning): pass

class NonCanonicalURI(Warning): pass
class SameDocumentReference(Warning): pass

class ContainsEmail(Warning): pass

class ContainsHTML(Warning): pass
class ContainsUndeclaredHTML(ContainsHTML): pass

class MissingSelf(Warning): pass 
class SelfDoesntMatchLocation(Warning): pass 

class MissingSourceElement(Warning): pass 
class MissingTypeAttr(Warning): pass 

class DuplicateEntries(Warning): pass
class DuplicateUpdated(Warning): pass

class NotBlank(Warning): pass
class AttrNotBlank(Warning): pass
class MissingTextualContent(Warning): pass

###################### info ######################

class MissingOptionalElement(Info): pass
class MissingItemLink(MissingOptionalElement): pass
class MissingItemTitle(MissingOptionalElement): pass

class BestPractices(Info): pass

class MissingRecommendedElement(BestPractices): pass
class MissingDCLanguage(MissingRecommendedElement): pass

class NonstdPrefix(BestPractices): pass

class NonstdEncoding(BestPractices): pass
class MissingEncoding(BestPractices): pass

class TempRedirect(Info): pass
class TextXml(Info): pass
class Uncompressed(Info): pass

## Atom-specific errors
class ObsoleteVersion(Warning): pass
class ObsoleteNamespace(Error): pass

class InvalidURI(InvalidValue) : pass
class InvalidURN(InvalidValue): pass
class InvalidTAG(InvalidValue): pass
class InvalidContentMode(InvalidValue) : pass
class InvalidMIMEType(InvalidValue) : pass
class InvalidNamespace(Error): pass
class NoMIMEType(MissingAttribute) : pass
class NotEscaped(InvalidValue): pass
class NotBase64(InvalidValue): pass
class NotInline(Warning): pass # this one can never be sure...
class NotHtml(Warning): pass
class HtmlFragment(Warning): pass

class W3CDTFDateNoTimezone(Warning) : pass
class W3CDTFDateNonUTC(Info) : pass
class W3CDTFDateNonLocal(Warning) : pass

############## non-errors (logging successes) ###################

class Success(LoggedEvent): pass

class ValidValue(Success): pass
class ValidCloud(Success): pass

class ValidURI(ValidValue): pass
class ValidHttpGUID(ValidURI): pass
class ValidURLAttribute(ValidURI): pass
class ValidURN(ValidValue): pass
class ValidTAG(ValidValue): pass
class ValidTitle(ValidValue): pass

class ValidDate(ValidValue): pass
class ValidW3CDTFDate(ValidDate): pass
class ValidRFC2822Date(ValidDate): pass

class ValidAttributeValue(ValidValue): pass
class ValidBooleanAttribute(ValidAttributeValue): pass

class ValidLanguage(ValidValue): pass
class ValidHeight(ValidValue): pass
class ValidWidth(ValidValue): pass
class ValidTitle(ValidValue): pass
class ValidContact(ValidValue): pass
class ValidIntegerAttribute(ValidValue): pass
class ValidMIMEAttribute(ValidValue): pass
class ValidDay(ValidValue): pass
class ValidHour(ValidValue): pass
class ValidInteger(ValidValue): pass
class ValidUpdatePeriod(ValidValue): pass
class ValidContentMode(ValidValue): pass
class ValidElement(ValidValue): pass
class ValidCopyright(ValidValue): pass
class ValidGeneratorName(ValidValue): pass
class OptionalValueMissing(ValidValue): pass
class ValidDoctype(ValidValue): pass
class ValidHtml(ValidValue): pass
class ValidAtomLinkRel(ValidValue): pass
class ValidLatitude(ValidValue): pass
class ValidLongitude(ValidValue): pass

###################### opml ######################

class InvalidOPMLVersion(Error): pass
class MissingXmlURL(Warning): pass
class InvalidOutlineVersion(Warning): pass
class InvalidOutlineType(Warning): pass
class InvalidExpansionState(Error): pass
class InvalidTrueFalse(InvalidValue): pass

__history__ = """
$Log$
Revision 1.56  2005/10/31 00:35:06  rubys
OPML attribute verification

Revision 1.55  2005/10/30 21:34:50  rubys
Preliminary OMPL support

Revision 1.54  2005/10/12 08:57:44  rubys
Issue warnings on names containing email addresses.

Revision 1.53  2005/09/15 04:43:45  rubys
Issue deprecation warnings on Atom 0.3 feeds.  No other code changes
were made.

Revision 1.52  2005/08/20 17:04:43  rubys
check rel="self": fix bug 1255184

Revision 1.51  2005/08/20 06:42:46  rubys
Doc for same-document reference warning

Revision 1.50  2005/08/20 03:58:58  rubys
white-space + xml:base

Revision 1.49  2005/08/08 01:24:12  rubys
Better error reporting on invalid email addr-spec

Revision 1.48  2005/08/07 12:20:52  rubys
RFC 3339 date checking, NotHTML is now a warning, atom testcase index

Revision 1.47  2005/08/07 01:08:14  rubys
I had a report of an uncaught Y2K error.  At the same time, catch
future dates and update the documentation to reflect RFC 3339 as
opposed to various related standards.

Revision 1.46  2005/08/01 14:23:44  rubys
Provide more helpful advice when people attempt to use XHTML named entity
references inside their feeds.

Addresses bugs: 1242762, 1243771, 1249420

Revision 1.45  2005/07/28 23:56:04  rubys
Duplicate Updated warning

Revision 1.44  2005/07/28 15:25:12  rubys
Warn on use of html mime types containing fragments

Revision 1.43  2005/07/25 00:40:54  rubys
Convert errors to warnings

Revision 1.42  2005/07/19 13:12:43  rubys
Complete basic coverage for Atom 1.0

Revision 1.41  2005/07/18 18:53:29  rubys
Atom 1.0 section 4.1.3

Revision 1.40  2005/07/18 12:20:46  rubys
Atom 1.0 section 4.1.2

Revision 1.39  2005/07/18 10:14:48  rubys
Warn on same document references

Revision 1.38  2005/07/17 23:22:44  rubys
Atom 1.0 section 4.1.1.1

Revision 1.37  2005/07/17 18:49:18  rubys
Atom 1.0 section 4.1

Revision 1.36  2005/07/16 22:01:14  rubys
Atom 1.0 text constructs and relative URIs

Revision 1.35  2005/07/16 14:40:09  rubys
More Atom 1.0 support

Revision 1.34  2005/07/15 11:17:24  rubys
Baby steps towards Atom 1.0 support

Revision 1.33  2005/07/08 14:56:13  rubys
Allow slash:comments to be zero.

Revision 1.32  2005/07/06 19:35:29  rubys
Validate iTunes keywords

Revision 1.31  2005/07/04 22:54:31  philor
Support rest of dc, dcterms, geo, geourl, icbm, and refactor out common extension elements

Revision 1.30  2005/07/02 19:26:44  rubys
Issue warnings for itunes tags which appear to contain HTML.

Note: this will also cause warnings to appear for titles and a
few other select tags (not descriptions!).  Previously, only
informational messages (which, by default, are not displayed)
were generated.

If this is a problem, we can change some individual tags, or
split this into two messages (one a warning, one informational).

Revision 1.29  2005/07/01 23:55:30  rubys
Initial support for itunes

Revision 1.28  2005/06/29 18:03:42  rubys
AtomLinkNotEmpty changed to a warning per
https://sourceforge.net/tracker/?func=detail&atid=626803&aid=1229805&group_id=99943

Revision 1.27  2005/01/22 23:45:36  rubys
pass last rss11 test case (neg-ext-notrdf.xml)

Revision 1.26  2005/01/21 23:18:42  josephw
Add logging, documentation and tests for canonical URIs.

Revision 1.25  2005/01/07 18:02:57  josephw
Check for bad HTTP headers, specifically where the name includes a space.

Revision 1.24  2004/07/28 04:41:55  rubys
Informational messages for text/xml with no charset and uncompressed responses

Revision 1.23  2004/07/28 04:07:55  rubys
Detect temporary redirects

Revision 1.22  2004/07/28 02:23:41  rubys
Remove some experimental rules

Revision 1.21  2004/07/16 22:09:20  rubys
Make MissingEncoding a Best Practice

Revision 1.20  2004/07/12 04:15:11  rubys
s/W3DTF/W3CDTF/g

Revision 1.19  2004/05/12 21:42:18  josephw
Report failure if a feed is larger than MAXDATALENGTH.

Revision 1.18  2004/05/03 19:59:11  josephw
Made MissingEncoding a warning and added documentation.

Revision 1.17  2004/04/30 11:50:02  rubys
Detect stray text outside of elements

Revision 1.16  2004/04/30 07:48:48  josephw
Added MissingEncoding, for when there's no apparent declaration of
encoding.

Revision 1.15  2004/03/30 02:42:40  rubys
Flag instances of small positive integers as guids as being "not sufficiently
unique".

Revision 1.14  2004/03/28 11:39:44  josephw
Added logging events and documentation for encoding and media type checks.

Revision 1.13  2004/03/28 09:49:58  josephw
Accept URLs relative to the current directory in demo.py. Added a top-level
exception to indicate validation failure; catch and print it in demo.py.

Revision 1.12  2004/03/23 01:33:04  rubys
Apply patch from Joseph Walton to provide better error reporting when
servers are misconfigured for gzip encoding.

Revision 1.11  2004/02/18 19:06:40  rubys
Downgrade system entities to info, particularly as the RSS 1.0 spec
explicitly endorses them.

Revision 1.10  2004/02/18 16:12:14  rubys
Make the distiction between W3CDTF and ISO8601 clearer in the docs.

Revision 1.9  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.8  2004/02/16 20:24:00  rubys
Fix for bug 892843: FeedValidator allows arbitrary Atom link rel values

Revision 1.7  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.6  2004/02/07 14:23:19  rubys
Fix for bug 892178: must reject xml 1.1

Revision 1.5  2004/02/07 02:27:14  rubys
SAXError on some installations, MissingNamespace on others...

Revision 1.4  2004/02/07 02:15:43  rubys
Implement feature 890049: gzip compression support
Fix for bug 890054: sends incorrect user-agent

Revision 1.3  2004/02/06 18:43:18  rubys
Apply patch 886675 from Joseph Walton:
"Warn about windows-1252 presented as ISO-8859-1"

Revision 1.2  2004/02/06 15:06:10  rubys
Handle 404 Not Found errors
Applied path 891556 provided by aegrumet

Revision 1.1.1.1  2004/02/03 17:33:16  rubys
Initial import.

Revision 1.63  2003/12/12 15:00:22  f8dy
changed blank link attribute tests to new error AttrNotBlank to distinguish them from elements that can not be blank

Revision 1.62  2003/12/12 14:23:19  f8dy
ValidAtomLinkRel should inherit from ValidValue

Revision 1.61  2003/12/12 05:42:05  rubys
Rough in some support for the new link syntax

Revision 1.60  2003/12/12 01:24:36  rubys
Multipart/alternative tests

Revision 1.59  2003/12/11 18:20:46  f8dy
passed all content-related testcases

Revision 1.58  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.57  2003/12/11 06:00:51  f8dy
added tag: testcases, passed

Revision 1.56  2003/08/24 00:05:34  f8dy
removed iframe tests, after further discussion this is not enough of a security risk to keep feeds from validating

Revision 1.55  2003/08/23 01:45:22  f8dy
added ContainsIframe

Revision 1.54  2003/08/23 00:28:04  rubys
Validate escaped text/HTML content

Revision 1.53  2003/08/06 16:16:59  f8dy
added testcase for Netscape DOCTYPE

Revision 1.52  2003/08/06 16:10:04  f8dy
added testcase for Netscape DOCTYPE

Revision 1.51  2003/08/05 18:01:37  f8dy
*** empty log message ***

Revision 1.50  2003/08/05 07:59:04  rubys
Add feed(id,tagline,contributor)
Drop feed(subtitle), entry(subtitle)
Check for obsolete version, namespace
Check for incorrect namespace on feed element

Revision 1.49  2003/08/05 05:37:42  f8dy
0.2 snapshot - add test for obsolete 0.1 version

Revision 1.48  2003/08/04 01:05:33  rubys
Check for HTML in titles

Revision 1.47  2003/08/04 00:54:35  rubys
Log every valid element (for better self validation in test cases)

Revision 1.46  2003/08/03 18:46:04  rubys
support author(url,email) and feed(author,copyright,generator)

Revision 1.45  2003/07/29 21:48:10  f8dy
tightened up test cases, added parent element check, changed negative test cases to positive

Revision 1.44  2003/07/29 20:57:39  f8dy
tightened up test cases, check for parent element, explicitly test for success

Revision 1.43  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.42  2003/07/29 17:13:17  f8dy
more urn tests

Revision 1.41  2003/07/29 16:44:56  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.40  2003/07/29 15:46:31  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.39  2003/07/29 15:15:33  f8dy
added tests for invalid URNs (may be used in entry/id of Atom feeds)

Revision 1.38  2003/07/20 17:44:27  rubys
Detect duplicate ids and guids

Revision 1.37  2003/07/19 21:15:08  f8dy
added tests and logging classes for duplicate guid/id values within a feed (thanks AaronSw for this idea)

Revision 1.36  2003/07/11 17:47:04  rubys
not-inline can only be a warning as one can never be totally sure...

Revision 1.35  2003/07/09 19:28:39  f8dy
added test cases looking at actual content vs. mode (note: not passed)

Revision 1.34  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.33  2003/07/09 03:31:36  f8dy
Updated pie-specific log messages

Revision 1.32  2003/07/07 10:35:50  rubys
Complete first pass of echo/pie tests

Revision 1.31  2003/07/07 00:54:00  rubys
Rough in some pie/echo support

Revision 1.30  2003/07/06 21:20:02  rubys
Refactor so test cases are organized by protocol

Revision 1.29  2002/10/30 23:03:01  f8dy
security fix: external (SYSTEM) entities

Revision 1.28  2002/10/27 18:54:30  rubys
Issue warnings for relative references in descriptions

Revision 1.27  2002/10/22 16:24:04  f8dy
added UnicodeError support for feeds that declare utf-8 but use 8-bit characters anyway

Revision 1.26  2002/10/18 19:28:43  f8dy
added testcases for mod_syndication and passed them

Revision 1.25  2002/10/18 14:17:30  f8dy
added tests for language/dc:language (must be valid ISO-639 language code
plus optional country code) and passed them

Revision 1.24  2002/10/18 13:06:57  f8dy
added licensing information

"""
