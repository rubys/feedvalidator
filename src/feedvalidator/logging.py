"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"

# feed types
TYPE_UNKNOWN = 0
TYPE_RSS1 = 1
TYPE_RSS2 = 2
TYPE_ATOM = 3
TYPE_ATOM_ENTRY = 4
TYPE_APP_CATEGORIES = 5
TYPE_APP_SERVICE = 6
TYPE_XRD = 7
TYPE_OPENSEARCH = 8
TYPE_OPML = 9
TYPE_KML20 = 10
TYPE_KML21 = 11
TYPE_KML22 = 12

FEEDTYPEDISPLAY = {0:"(unknown type)", 1:"RSS", 2:"RSS", 3:"Atom 1.0", 4:"Atom 1.0", 5:"Atom Publishing Protocol Category", 6:"Atom Publishing Protocol Service", 7:"XRD", 8:"OpenSearch", 9:"OPML", 10:"KML 2.0", 11:"KML 2.1", 12:"KML 2.2"}

VALIDFEEDGRAPHIC = {0:"", 1:"valid-rss.png", 2:"valid-rss-rogers.png", 3:"valid-atom.png", 4:"valid-atom.png", 5:"valid-atom.png",  6:"valid-atom.png", 7:"valid-xrd.png", 8:"valid-opensearch.png", 9:"valid-opml.gif", 10:"valid-kml.png", 11:"valid-kml.png", 12:"valid-kml.png"}

#
# logging support
#

class LoggedEvent:
  def __init__(self, params):
    self.params = params
class Info(LoggedEvent): pass

class Message(LoggedEvent): pass
class Warning(Message): pass
class Error(Message): pass

class ValidationFailure(Error):
  def __init__(self, event):
    LoggedEvent.__init__(self, {})
    self.event = event

###################### error ######################

class SAXError(Error): pass
class WPBlankLine(SAXError): pass
class UnicodeError(Error): pass
class MissingNamespace(SAXError): pass
class NotInANamespace(MissingNamespace): pass
class UseOfExtensionAttr(Warning): pass
class UndefinedNamedEntity(SAXError): pass

class InvalidRSSVersion(Error): pass
class UndefinedElement(Error): pass
class NoBlink(UndefinedElement): pass
class NoThrWhen(UndefinedElement): pass
class MissingAttribute(Error): pass
class UnexpectedAttribute(Error): pass
class DuplicateElement(Error): pass
class NotEnoughHoursInTheDay(Error): pass
class EightDaysAWeek(Error): pass

class InvalidValue(Error): pass
class InvalidContact(InvalidValue): pass
class UnknownHost(Warning): pass
class InvalidAddrSpec(InvalidContact): pass
class InvalidLink(InvalidValue): pass
class UriNotIri(InvalidLink): pass
class InvalidIRI(InvalidLink): pass
class InvalidFullLink(InvalidLink): pass
class InvalidUriChar(InvalidLink): pass
class InvalidISO8601Date(InvalidValue): pass
class InvalidISO8601DateTime(InvalidValue): pass
class InvalidW3CDTFDate(InvalidISO8601Date): pass
class InvalidRFC2822Date(InvalidValue): pass
class IncorrectDOW(InvalidRFC2822Date): pass
class InvalidRFC3339Date(InvalidValue): pass
class InvalidURIAttribute(InvalidLink): pass
class InvalidURLAttribute(InvalidURIAttribute): pass
class InvalidIntegerAttribute(InvalidValue): pass
class InvalidBooleanAttribute(InvalidValue): pass
class InvalidMIMEAttribute(InvalidValue): pass
class InvalidInteger(InvalidValue): pass
class InvalidPercentage(InvalidValue): pass
class InvalidNonNegativeInteger(InvalidInteger): pass
class InvalidPositiveInteger(InvalidInteger): pass
class InvalidAlphanum(Error): pass
class InvalidWidth(InvalidValue): pass
class InvalidHeight(InvalidValue): pass
class InvalidHour(InvalidValue): pass
class InvalidDay(InvalidValue): pass
class InvalidHttpGUID(InvalidValue): pass
class InvalidLanguage(InvalidValue): pass
class InvalidUpdatePeriod(InvalidValue): pass
class InvalidItunesCategory(InvalidValue): pass
class ObsoleteItunesCategory(Warning): pass
class InvalidYesNo(InvalidValue): pass
class InvalidYesNoClean(InvalidValue): pass
class InvalidDuration(InvalidValue): pass
class TooLong(InvalidValue): pass
class InvalidKeywords(Warning): pass
class InvalidTextType(InvalidValue): pass
class InvalidCommaSeparatedIntegers(InvalidValue): pass
class UndeterminableVocabulary(Warning): pass
class InvalidFormComponentName(InvalidValue): pass
class InvalidAccessRestrictionRel(InvalidValue): pass
class NotURLEncoded(InvalidValue): pass
class InvalidLocalRole(InvalidValue): pass
class InvalidEncoding(InvalidValue): pass
class InvalidSyndicationRight(InvalidValue): pass
class InvalidLocalParameter(InvalidValue): pass

class MissingElement(Error): pass
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

class DuplicateAtomLink(Error): pass
class MissingHref(MissingAttribute): pass
class AtomLinkNotEmpty(Warning): pass
class UnregisteredAtomLinkRel(Warning): pass

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

class InvalidPermalink(Error): pass

class InvalidCreditRole(Error): pass

class InvalidMediaTextType(Error): pass
class InvalidMediaHash(Error): pass
class InvalidMediaRating(Error): pass
class InvalidNPTTime(Error): pass
class InvalidMediaRestriction(Error): pass
class InvalidMediaRestrictionRel(Error): pass
class InvalidMediaRestrictionType(Error): pass
class InvalidMediaMedium(Error): pass
class InvalidMediaExpression(Error): pass
class DeprecatedMediaAdult(Warning): pass
class MediaGroupWithoutAlternatives(Error): pass

class InvalidSseType(Error): pass
class InvalidNSS(Error): pass
class IntegerOverflow(Error): pass
class SinceAfterUntil(Error): pass
class MissingByAndWhenAttrs(Error): pass

class HttpErrorWithPossibleFeed(Error): pass

###################### warning ######################

class DuplicateSemantics(Warning): pass
class DuplicateItemSemantics(DuplicateSemantics): pass
class DuplicateDescriptionSemantics(DuplicateSemantics): pass

class ImageLinkDoesntMatch(Warning): pass
class ImageUrlFormat(Warning): pass

class ContainsRelRef(Warning): pass

class ReservedPrefix(Warning): pass
class MediaRssNamespace(Error): pass

class NotSufficientlyUnique(Warning): pass
class ImplausibleDate(Warning): pass
class ProblematicalRFC822Date(Warning): pass

class SecurityRisk(Warning): pass
class SecurityRiskAttr(SecurityRisk): pass
class DangerousStyleAttr(SecurityRiskAttr): pass

class BadCharacters(Warning): pass
class ObscureEncoding(Warning): pass
class UnexpectedContentType(Warning): pass
class EncodingMismatch(Warning): pass
class NonSpecificMediaType(Warning): pass

class NonCanonicalURI(Warning): pass
class SameDocumentReference(Warning): pass

class ContainsEmail(Warning): pass

class ContainsHTML(Warning): pass
class ContainsUndeclaredHTML(ContainsHTML): pass

class MissingSelf(Warning): pass 
class SelfDoesntMatchLocation(Warning): pass 
class RelativeSelf(Warning): pass 

class MissingSourceElement(Warning): pass 
class MissingTypeAttr(Warning): pass 

class DuplicateIds(Error): pass
class DuplicateEntries(Warning): pass
class DuplicateUpdated(Warning): pass

class NotBlank(Warning): pass
class AttrNotBlank(Warning): pass
class MissingSummary(Error): pass
class MissingTextualContent(Warning): pass

class NotUTF8(Warning): pass
class MissingItunesElement(Warning): pass
class MissingItunesEmail(Warning): pass
class UnsupportedItunesFormat(Warning): pass

class SelfNotAtom(Warning): pass
class DuplicateEnclosure(Warning): pass

class MissingGuid(Warning): pass

class ObsoleteWikiNamespace(Warning): pass
class CommentRSS(Warning): pass

class ShouldIncludeExample(Warning): pass
class InvalidAdultContent(Warning): pass
class InvalidSyndicationRight(InvalidValue): pass
class UndeclaredPrefix(InvalidValue): pass

class MisplacedXHTMLContent(Warning): pass
class SchemeNotIANARegistered(Warning): pass
class AvoidNamespacePrefix(Warning): pass
class UnknownNamespace(Warning): pass

class MissingRecommendedAttribute(Warning): pass

class QuestionableUsage(Warning): pass

###################### info ######################

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

class ConflictingCatAttr(Error): pass 
class ConflictingCatChildren(Error): pass 
class InvalidMediaRange(Error): pass 
class UndefinedParam(Warning): pass 

class InvalidURI(InvalidValue) : pass
class InvalidURN(InvalidValue): pass
class InvalidUUID(InvalidValue): pass
class InvalidTAG(InvalidValue): pass
class InvalidContentMode(InvalidValue) : pass
class InvalidMIMEType(InvalidMediaRange) : pass
class InvalidNamespace(Error): pass
class NotEscaped(InvalidValue): pass
class NotBase64(InvalidValue): pass
class NotInline(Warning): pass # this one can never be sure...
class NotHtml(Warning): pass
class HtmlFragment(Warning): pass

class FeedHistoryRelInEntry(Warning): pass
class FeedRelInCompleteFeed(Error): pass
class CurrentNotSelfInCompleteFeed(Error): pass
class LinkPastEnd(Error): pass
class MissingCurrentInArchive(Warning): pass
class ArchiveIncomplete(Warning): pass

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
class ValidPercentage(ValidValue): pass
class ValidUpdatePeriod(ValidValue): pass
class ValidContentMode(ValidValue): pass
class ValidElement(ValidValue): pass
class ValidCopyright(ValidValue): pass
class ValidGeneratorName(ValidValue): pass
class OptionalValueMissing(ValidValue): pass
class ValidDoctype(ValidValue): pass
class DeprecatedDTD(Error): pass
class ValidHtml(ValidValue): pass
class ValidAtomLinkRel(ValidValue): pass
class ValidLatitude(ValidValue): pass
class ValidLongitude(ValidValue): pass
class ValidNPTTime(ValidValue): pass

###################### opml ######################

class InvalidOPMLVersion(Error): pass
class MissingXmlURL(Warning): pass
class InvalidOutlineVersion(Warning): pass
class InvalidOutlineType(Warning): pass
class InvalidExpansionState(Error): pass
class InvalidTrueFalse(InvalidValue): pass
class MissingOutlineType(Warning): pass
class MissingTitleAttr(Warning): pass
class MissingUrlAttr(Warning): pass

###################### gbase ######################

class InvalidCountryCode(InvalidValue): pass
class InvalidCurrencyUnit(InvalidValue): pass
class InvalidFloat(InvalidValue): pass
class InvalidFloatUnit(InvalidValue): pass
class InvalidFullLocation(InvalidValue): pass
class InvalidGender(InvalidValue): pass
class InvalidIntUnit(InvalidValue): pass
class InvalidLabel(InvalidValue): pass
class InvalidLocation(InvalidValue): pass
class InvalidMaritalStatus(InvalidValue): pass
class InvalidPaymentMethod(InvalidValue): pass
class InvalidPriceType(InvalidValue): pass
class InvalidRatingType(InvalidValue): pass
class InvalidReviewerType(InvalidValue): pass
class InvalidSalaryType(InvalidValue): pass
class InvalidServiceType(InvalidValue): pass
class InvalidYear(InvalidValue): pass
class TooMany(DuplicateElement): pass

###################### georss ######################

class InvalidCoord(InvalidValue): pass
class InvalidCoordList(InvalidValue): pass
class CoordComma(Warning): pass

###################### meta ######################

class InvalidMetaName(InvalidValue): pass
class InvalidMetaContent(InvalidValue): pass

###################### kml ######################

class Deprecated(Warning): pass
class DeprecatedRootHref(Warning): pass
class InvalidAltitudeMode(InvalidValue): pass
class InvalidAngle(InvalidValue): pass
class InvalidColor(InvalidValue): pass
class InvalidColorMode(InvalidValue): pass
class InvalidItemIconState(InvalidValue): pass
class InvalidListItemType(InvalidValue): pass
class InvalidKmlCoordList(InvalidValue): pass
class InvalidKmlLatitude(InvalidValue): pass
class InvalidKmlLongitude(InvalidValue): pass
class InvalidKmlMediaType(Warning): pass
class InvalidKmlUnits(InvalidValue): pass
class InvalidRefreshMode(InvalidValue): pass
class InvalidSchemaFieldType(InvalidValue): pass
class InvalidStyleState(InvalidValue): pass
class InvalidViewRefreshMode(InvalidValue): pass
class InvalidZeroOne(InvalidValue): pass
class MissingId(Warning): pass
class ValidAngle(ValidValue): pass

###################### RSS 2.0 Profile ######################

class RSS20Profile(Warning): pass
class CharacterData(ContainsHTML): pass
class EmailFormat(RSS20Profile): pass
class MissingRealName(EmailFormat): pass
class MisplacedItem(RSS20Profile): pass
class ImageTitleDoesntMatch(RSS20Profile): pass
class AvoidTextInput(RSS20Profile): pass
class NeedDescriptionBeforeContent(RSS20Profile): pass
class SlashDate(RSS20Profile): pass
class UseZeroForMidnight(RSS20Profile): pass
class MissingAtomSelfLink(MissingSelf): pass
class UseZeroForUnknown(InvalidNonNegativeInteger): pass
