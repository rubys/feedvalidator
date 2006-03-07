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
class NotInANamespace(MissingNamespace): pass
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
class UriNotIri(InvalidLink): pass
class InvalidIRI(InvalidLink): pass
class InvalidFullLink(InvalidLink): pass
class InvalidISO8601Date(InvalidValue): pass
class InvalidISO8601DateTime(InvalidValue): pass
class InvalidW3CDTFDate(InvalidISO8601Date): pass
class InvalidRFC2822Date(InvalidValue): pass
class InvalidRFC3339Date(InvalidValue): pass
class InvalidURIAttribute(InvalidLink): pass
class InvalidURLAttribute(InvalidURIAttribute): pass
class InvalidIntegerAttribute(InvalidValue): pass
class InvalidBooleanAttribute(InvalidValue): pass
class InvalidMIMEAttribute(InvalidValue): pass
class InvalidInteger(InvalidValue): pass
class InvalidPercentage(InvalidValue): pass
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
class InvalidKeywords(Warning): pass
class InvalidTextType(InvalidValue): pass
class InvalidCommaSeparatedIntegers(InvalidValue): pass
class UndeterminableVocabulary(Warning): pass
class InvalidFormComponentName(InvalidValue): pass

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

###################### warning ######################

class DuplicateSemantics(Warning): pass
class DuplicateItemSemantics(DuplicateSemantics): pass

class ImageLinkDoesntMatch(Warning): pass
class ImageUrlFormat(Warning): pass

class ContainsRelRef(Warning): pass

class ReservedPrefix(Warning): pass

class NotSufficientlyUnique(Warning): pass
class ImplausibleDate(Warning): pass
class DeprecatedRFC822Date(Warning): pass

class SecurityRisk(Warning): pass

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

class NotUTF8(Warning): pass
class MissingItunesElement(Warning): pass
class MissingItunesEmail(Warning): pass
class UnsupportedItunesFormat(Warning): pass

class SelfNotAtom(Warning): pass
class DuplicateEnclosure(Warning): pass

class MissingGuid(Warning): pass

class ObsoleteWikiNamespace(Warning): pass

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
class NotEscaped(InvalidValue): pass
class NotBase64(InvalidValue): pass
class NotInline(Warning): pass # this one can never be sure...
class NotHtml(Warning): pass
class HtmlFragment(Warning): pass

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
