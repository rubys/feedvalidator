"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net>, Mark Pilgrim <http://diveintomark.org/> and Phil Ringnalda <http://philringnalda.com>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby, Mark Pilgrim and Phil Ringnalda"
__license__ = "Python"
            
from validators import *
from logging import *

class extension:
  def do_dc_title(self):
    return text(), noduplicates()

  def do_dc_description(self):
    return text(), noduplicates()

  def do_dc_publisher(self):
    if "webMaster" in self.children:
      self.log(DuplicateSemantics({"core":"webMaster", "ext":"dc:publisher"}))
    return text() # duplicates allowed

  def do_dc_contributor(self):
    return text() # duplicates allowed

  def do_dc_type(self):
    return text(), noduplicates()
  
  def do_dc_format(self):
    return text(), noduplicates()

  def do_dc_identifier(self):
    return text()

  def do_dc_source(self):
    if "source" in self.children:
      self.log(DuplicateItemSemantics({"core":"source", "ext":"dc:source"}))
    return text(), noduplicates()

  def do_dc_language(self):
    if "language" in self.children:
      self.log(DuplicateSemantics({"core":"language", "ext":"dc:language"}))
    return iso639(), noduplicates()

  def do_dc_relation(self):
    return text(), # duplicates allowed

  def do_dc_coverage(self):
    return text(), # duplicates allowed

  def do_dc_rights(self):
    if "copyright" in self.children:
      self.log(DuplicateSemantics({"core":"copyright", "ext":"dc:rights"}))
    return text(), noduplicates()

  def do_dcterms_alternative(self):
    return text() #duplicates allowed

  def do_dcterms_abstract(self):
    return text(), noduplicates()

  def do_dcterms_tableOfContents(self):
    return rdfResourceURI(), noduplicates()

  def do_dcterms_created(self):
    return w3cdtf(), noduplicates()
  
  def do_dcterms_valid(self):
    return eater()
  
  def do_dcterms_available(self):
    return eater()

  def do_dcterms_issued(self):
    return w3cdtf(), noduplicates()

  def do_dcterms_modified(self):
    if "lastBuildDate" in self.children:
      self.log(DuplicateSemantics({"core":"lastBuildDate", "ext":"dcterms:modified"}))
    return w3cdtf(), noduplicates()

  def do_dcterms_dateAccepted(self):
    return text(), noduplicates()

  def do_dcterms_dateCopyrighted(self):
    return text(), noduplicates()

  def do_dcterms_dateSubmitted(self):
    return text(), noduplicates()

  def do_dcterms_extent(self):
    return positiveInteger(), nonblank(), noduplicates()

#  def do_dcterms_medium(self):
#    spec defines it as something that should never be used
#    undefined element'll do for now 

  def do_dcterms_isVersionOf(self):
    return rdfResourceURI() # duplicates allowed
  
  def do_dcterms_hasVersion(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_isReplacedBy(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_replaces(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_isRequiredBy(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_requires(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_isPartOf(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_hasPart(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_isReferencedBy(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_references(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_isFormatOf(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_hasFormat(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_conformsTo(self):
    return rdfResourceURI() # duplicates allowed

  def do_dcterms_spatial(self):
    return eater()  

  def do_dcterms_temporal(self):
    return eater()

  def do_dcterms_audience(self):
    return text()

  def do_dcterms_mediator(self):
    return text(), noduplicates()

  # added to DMCI, but no XML mapping has been defined
  def do_dcterms_accessRights(self):
    return eater()

  def do_dcterms_accrualMethod(self):
    return eater()

  def do_dcterms_accrualPeriodicity(self):
    return eater()

  def do_dcterms_accrualPolicy(self):
    return eater()

  def do_dcterms_bibliographicCitation(self):
    return eater()

  def do_dcterms_educationLevel(self):
    return eater()

  def do_dcterms_instructionalMethod(self):
    return eater()

  def do_dcterms_license(self):
    return eater()

  def do_dcterms_provenance(self):
    return eater()

  def do_dcterms_rightsHolder(self):
    return eater()

  def do_g_actor(self):
    return nonhtml(), noduplicates()

  def do_g_age(self):
    return nonNegativeInteger(), noduplicates()

  def do_g_agent(self):
    return nonhtml(), noduplicates()

  def do_g_area(self):
    return nonhtml(), noduplicates() # intUnit

  def do_g_apparel_type(self):
    return nonhtml(), noduplicates()

  def do_g_artist(self):
    return nonhtml(), noduplicates()

  def do_g_author(self):
    return nonhtml(), noduplicates()

  def do_g_bathrooms(self):
    return nonNegativeInteger(), noduplicates()

  def do_g_bedrooms(self):
    return nonNegativeInteger(), noduplicates()

  def do_g_brand(self):
    return nonhtml(), noduplicates()

  def do_g_color(self):
    return nonhtml(), noduplicates()

  def do_g_condition(self):
    return nonhtml(), noduplicates()

  def do_g_course_date_range(self):
    return g_dateTimeRange(), noduplicates()

  def do_g_course_number(self):
    return nonhtml(), noduplicates()

  def do_g_course_times(self):
    return nonhtml(), noduplicates()

  def do_g_currency(self):
    return iso4217(), noduplicates()

  def do_g_delivery_notes(self):
    return nonhtml(), noduplicates()

  def do_g_delivery_radius(self):
    return floatUnit(), noduplicates()

  def do_g_education(self):
    return nonhtml(), noduplicates()

  def do_g_employer(self):
    return nonhtml(), noduplicates()

  def do_g_ethnicity(self):
    return nonhtml(), noduplicates()

  def do_g_event_date_range(self):
    return g_dateTimeRange(), noduplicates()

  def do_g_expiration_date(self):
    return iso8601_date(), noduplicates()

  def do_g_expiration_date_time(self):
    return iso8601(), noduplicates()

  def do_g_from_location(self):
    return g_locationType(), noduplicates()

  def do_g_gender(self):
    return g_genderEnumeration(), noduplicates()

  def do_g_hoa_dues(self):
    return g_float(), noduplicates()

  def do_g_format(self):
    return nonhtml(), noduplicates()

  def do_g_id(self):
    return nonhtml(), noduplicates()

  def do_g_image_link(self):
    return rfc2396_full() # TODO: max 10

  def do_g_immigration_status(self):
    return nonhtml(), noduplicates()

  def do_g_interested_in(self):
    return nonhtml(), noduplicates()

  def do_g_isbn(self):
    return nonhtml(), noduplicates()

  def do_g_job_function(self):
    return nonhtml(), noduplicates()

  def do_g_job_industry(self):
    return nonhtml(), noduplicates()

  def do_g_job_type(self):
    return nonhtml(), noduplicates()

  def do_g_label(self):
    return g_labelType() # TODO: max 10

  def do_g_listing_type(self):
    return truefalse(), noduplicates()

  def do_g_location(self):
    return g_full_locationType(), noduplicates()

  def do_g_make(self):
    return nonhtml(), noduplicates()

  def do_g_manufacturer(self):
    return nonhtml(), noduplicates()

  def do_g_manufacturer_id(self):
    return nonhtml(), noduplicates()

  def do_g_marital_status(self):
    return g_maritalStatusEnumeration(), noduplicates()

  def do_g_megapixels(self):
    return floatUnit(), noduplicates()

  def do_g_memory(self):
    return floatUnit(), noduplicates()

  def do_g_mileage(self):
    return g_intUnit(), noduplicates()

  def do_g_model(self):
    return nonhtml(), noduplicates()

  def do_g_model_number(self):
    return nonhtml(), noduplicates()

  def do_g_name_of_item_being_reviewed(self):
    return nonhtml(), noduplicates()

  def do_g_news_source(self):
    return nonhtml(), noduplicates()

  def do_g_occupation(self):
    return nonhtml(), noduplicates()

  def do_g_payment_notes(self):
    return nonhtml(), noduplicates()

  def do_g_pages(self):
    return positiveInteger(), nonblank(), noduplicates()

  def do_g_payment_accepted(self):
    return g_paymentMethodEnumeration()

  def do_g_pickup(self):
    return truefalse(), noduplicates()

  def do_g_price(self):
    return floatUnit(), noduplicates()

  def do_g_price_type(self):
    return g_priceTypeEnumeration(), noduplicates()

  def do_g_processor_speed(self):
    return floatUnit(), noduplicates()

  def do_g_product_type(self):
    return nonhtml(), noduplicates()

  def do_g_property_type(self):
    return nonhtml(), noduplicates()

  def do_g_publication_name(self):
    return nonhtml(), noduplicates()

  def do_g_publication_volume(self):
    return nonhtml(), noduplicates()

  def do_g_publish_date(self):
    return iso8601_date(), noduplicates()

  def do_g_quantity(self):
    return nonNegativeInteger(), nonblank(), noduplicates()

  def do_g_rating(self):
    return g_ratingTypeEnumeration(), noduplicates()

  def do_g_review_type(self):
    return nonhtml(), noduplicates()

  def do_g_reviewer_type(self):
    return g_reviewerTypeEnumeration(), noduplicates()

  def do_g_salary(self):
    return g_float(), noduplicates()

  def do_g_salary_type(self):
    return g_salaryTypeEnumeration(), noduplicates()

  def do_g_school_district(self):
    return nonhtml(), noduplicates()

  def do_g_service_type(self):
    return nonhtml(), noduplicates()

  def do_g_sexual_orientation(self):
    return nonhtml(), noduplicates()

  def do_g_size(self):
    return nonhtml(), noduplicates() # TODO: expressed in either two or three dimensions.

  def do_g_shipping(self):
    return g_shipping(), noduplicates()

  def do_g_subject(self):
    return nonhtml(), noduplicates()

  def do_g_subject_area(self):
    return nonhtml(), noduplicates()

  def do_g_tax_percent(self):
    return percentType(), noduplicates()

  def do_g_tax_region(self):
    return nonhtml(), noduplicates()

  def do_g_to_location(self):
    return g_locationType(), noduplicates()

  def do_g_travel_date_range(self):
    return g_dateTimeRange(), noduplicates()

  def do_g_university(self):
    return nonhtml(), noduplicates()

  def do_g_upc(self):
    return nonhtml(), noduplicates()

  def do_g_url_of_item_being_reviewed(self):
    return rfc2396_full(), noduplicates()

  def do_g_vehicle_type(self):
    return nonhtml(), noduplicates()

  def do_g_vin(self):
    return nonhtml(), noduplicates()

  def do_g_weight(self):
    return floatUnit(), noduplicates()

  def do_g_year(self):
    return g_year(), noduplicates()

class extension_channel_item(extension):
  def do_geo_lat(self):
    return latitude()

  def do_geo_long(self):
    return longitude()

  def do_geourl_latitude(self):
    return latitude()

  def do_geourl_longitude(self):
    return longitude()

  def do_icbm_latitude(self):
    return latitude()

  def do_icbm_longitude(self):
    return longitude()

class extension_item(extension_channel_item):
  def do_annotate_reference(self):
    return rdfResourceURI(), noduplicates()
    
  def do_ag_source(self):
    return text(), noduplicates()

  def do_ag_sourceURL(self):
    return rfc2396_full(), noduplicates()

  def do_ag_timestamp(self):
    return iso8601(), noduplicates()

  def do_ev_startdate(self):
    return iso8601(), noduplicates()

  def do_ev_enddate(self):
    return iso8601(), noduplicates()

  def do_ev_location(self):
    return eater()

  def do_ev_organizer(self):
    return eater()

  def do_ev_type(self):
    return text(), noduplicates()

  def do_foaf_maker(self):
    return eater()

  def do_foaf_primaryTopic(self):
    return eater()

  def do_slash_comments(self):
    return nonNegativeInteger()

  def do_slash_section(self):
    return text()

  def do_slash_department(self):
    return text()

  def do_slash_hit_parade(self):
    return commaSeparatedIntegers(), noduplicates()

  def do_taxo_topics(self):
    return eater()

  def do_thr_children(self):
    return eater()

class extension_rss20_item(extension_item):
  def do_trackback_ping(self):
    return rfc2396_full(), noduplicates()

  def do_trackback_about(self):
    return rfc2396_full()

  def do_dcterms_accessRights(self):
    return eater()

  def do_dcterms_accrualMethod(self):
    return eater()

  def do_dcterms_accrualPeriodicity(self):
    return eater()

  def do_dcterms_accrualPolicy(self):
    return eater()

  def do_dcterms_bibliographicCitation(self):
    return eater()

  def do_dcterms_educationLevel(self):
    return eater()

  def do_dcterms_instructionalMethod(self):
    return eater()

  def do_dcterms_license(self):
    return eater()

  def do_dcterms_provenance(self):
    return eater()

  def do_dcterms_rightsHolder(self):
    return eater()

class extension_rss10_item(extension_item):
  def do_trackback_ping(self):
    return rdfResourceURI(), noduplicates()

  def do_trackback_about(self):
    return rdfResourceURI()

class extension_channel(extension_channel_item):
  def do_admin_generatorAgent(self):
    if "generator" in self.children:
      self.log(DuplicateSemantics({"core":"generator", "ext":"admin:generatorAgent"}))
    return admin_generatorAgent(), noduplicates()

  def do_admin_errorReportsTo(self):
    return admin_errorReportsTo(), noduplicates()

  def do_blogChannel_blogRoll(self):
    return rfc2396_full(), noduplicates()

  def do_blogChannel_mySubscriptions(self):
    return rfc2396_full(), noduplicates()

  def do_blogChannel_blink(self):
    return rfc2396_full(), noduplicates()

  def do_blogChannel_changes(self):
    return rfc2396_full(), noduplicates()

  def do_sy_updatePeriod(self):
    return sy_updatePeriod(), noduplicates()

  def do_sy_updateFrequency(self):
    return positiveInteger(), nonblank(), noduplicates()

  def do_sy_updateBase(self):
    return w3cdtf(), noduplicates()

  def do_foaf_maker(self):
    return eater()

  def do_cp_server(self):
    return rdfResourceURI()

# revisit these once Atom 1.0 comes out (issue warning on duplicate semantics)
class extension_feed(extension_channel):
  def do_dc_creator(self): # atom:creator
    return text() # duplicates allowed
  def do_dc_subject(self): # atom:category
    return text() # duplicates allowed
  def do_dc_date(self): # atom:updated
    return w3cdtf(), noduplicates()
  def do_creativeCommons_license(self):
    return rfc2396_full()


# revisit these once Atom 1.0 comes out (issue warning on duplicate semantics)
class extension_entry(extension_item):
  def do_dc_creator(self): # atom:creator
    return text() # duplicates allowed
  def do_dc_subject(self): # atom:category
    return text() # duplicates allowed
  def do_dc_date(self): # atom:published
    return w3cdtf(), noduplicates()
  def do_creativeCommons_license(self):
    return rfc2396_full()

  def do_trackback_ping(self):
    return rfc2396_full(), noduplicates()

  # XXX This should have duplicate semantics with link[@rel='related']
  def do_trackback_about(self):
    return rfc2396_full()

class admin_generatorAgent(rdfResourceURI): pass
class admin_errorReportsTo(rdfResourceURI): pass

class sy_updatePeriod(text):
  def validate(self):
    if self.value not in ('hourly', 'daily', 'weekly', 'monthly', 'yearly'):
      self.log(InvalidUpdatePeriod({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      self.log(ValidUpdatePeriod({"parent":self.parent.name, "element":self.name, "value":self.value}))

class g_shipping(validatorBase):
  def do_g_service(self):
    return g_serviceTypeEnumeration(), noduplicates()
  def do_g_country(self):
    return iso3166(), noduplicates()
  def do_g_price(self):
    return floatUnit(), noduplicates()

class g_dateTimeRange(validatorBase):
  def do_g_start(self):
    return iso8601(), noduplicates()
  def do_g_end(self):
    return iso8601(), noduplicates()

class enumeration(text):
  def validate(self):
    if self.value not in self.valuelist:
      self.log(self.error({"parent":self.parent.name, "element":self.name,
        "attr": ':'.join(self.name.split('_',1)), "value":self.value}))

class g_labelType(text):
  def validate(self):
    if self.value.find(',')>=0:
      self.log(InvalidLabel({"parent":self.parent.name, "element":self.name,
        "attr": ':'.join(self.name.split('_',1)), "value":self.value}))

class g_locationType(text):
  def validate(self):
    if len(self.value.split(',')) not in [2,3]: 
      self.log(InvalidLocation({"parent":self.parent.name, "element":self.name,
        "attr": ':'.join(self.name.split('_',1)), "value":self.value}))

class g_full_locationType(text):
  def validate(self):
    fields = self.value.split(',')
    if len(fields) != 5 or 0 in [len(f.strip()) for f in fields]: 
      self.log(InvalidFullLocation({"parent":self.parent.name, "element":self.name,
        "attr": ':'.join(self.name.split('_',1)), "value":self.value}))

class g_genderEnumeration(enumeration):
  error = InvalidGender
  valuelist =  ["Male", "M", "Female", "F"]

class g_maritalStatusEnumeration(enumeration):
  error = InvalidMaritalStatus
  valuelist =  ["single", "divorced", "separated", "widowed", "married", "in relationship"]

class g_paymentMethodEnumeration(enumeration):
  error = InvalidPaymentMethod
  valuelist =  ["Cash", "Check", "Traveler's Check", "Visa", "MasterCard",
   "American Express", "Discover", "Wire transfer"]

class g_priceTypeEnumeration(enumeration):
  error = InvalidPriceType
  valuelist =  ["negotiable", "starting"]

class g_ratingTypeEnumeration(enumeration):
  error = InvalidRatingType
  valuelist =  ["1", "2", "3", "4", "5"]

class g_reviewerTypeEnumeration(enumeration):
  error = InvalidReviewerType
  valuelist =  ["editorial", "user"]

class g_salaryTypeEnumeration(enumeration):
  error = InvalidSalaryType
  valuelist =  ["starting", "negotiable"]

class g_serviceTypeEnumeration(enumeration):
  error = InvalidServiceType
  valuelist =  ['FedEx', 'UPS', 'DHL', 'Mail', 'Other', 'Overnight', 'Standard']

class g_float(text):
  def validate(self):
    import re
    if not re.match('\d+\.?\d*\s*\w*', self.value):
      self.log(InvalidFloat({"parent":self.parent.name, "element":self.name,
        "attr": ':'.join(self.name.split('_',1)), "value":self.value}))

class floatUnit(text):
  def validate(self):
    import re
    if not re.match('\d+\.?\d*\s*\w*$', self.value):
      self.log(InvalidFloatUnit({"parent":self.parent.name, "element":self.name,
        "attr": ':'.join(self.name.split('_',1)), "value":self.value}))

class g_year(text):
  def validate(self):
    import time
    try:
      year = int(self.value)
      if year < 1900 or year > time.localtime()[0]+4: raise InvalidYear
    except:
      self.log(InvalidYear({"parent":self.parent.name, "element":self.name,
        "attr": ':'.join(self.name.split('_',1)), "value":self.value}))

class g_intUnit(text):
  def validate(self):
    try:
      if int(self.value.split(' ')[0].replace(',','')) < 0: raise InvalidIntUnit
    except:
      self.log(InvalidIntUnit({"parent":self.parent.name, "element":self.name,
        "attr": ':'.join(self.name.split('_',1)), "value":self.value}))

class iso3166(nonhtml):
  error = InvalidCountryCode
  valuelist = [
    "AD", "AE", "AF", "AG", "AI", "AM", "AN", "AO", "AQ", "AR", "AS", "AT",
    "AU", "AW", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ",
    "BM", "BN", "BO", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC",
    "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN", "CO", "CR", "CU",
    "CV", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE",
    "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA",
    "GB", "GD", "GE", "GF", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR",
    "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID",
    "IE", "IL", "IN", "IO", "IQ", "IR", "IS", "IT", "JM", "JO", "JP", "KE",
    "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB",
    "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD",
    "MG", "MH", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT",
    "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI",
    "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH",
    "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO",
    "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK",
    "SL", "SM", "SN", "SO", "SR", "ST", "SV", "SY", "SZ", "TC", "TD", "TF",
    "TG", "TH", "TJ", "TK", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ",
    "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN",
    "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW"]

class iso4217(enumeration):
  error = InvalidCurrencyUnit
  valuelist = [
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZM",
    "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV",
    "BRL", "BSD", "BTN", "BWP", "BYR", "BZD", "CAD", "CDF", "CHE", "CHF",
    "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CSD", "CUP", "CVE",
    "CYP", "CZK", "DJF", "DKK", "DOP", "DZD", "EEK", "EGP", "ERN", "ETB",
    "EUR", "FJD", "FKP", "GBP", "GEL", "GHC", "GIP", "GMD", "GNF", "GTQ",
    "GWP", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "INR",
    "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF",
    "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL",
    "LTL", "LVL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP",
    "MRO", "MTL", "MUR", "MWK", "MXN", "MXV", "MYR", "MZM", "NAD", "NGN",
    "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR",
    "PLN", "PYG", "QAR", "ROL", "RON", "RUB", "RWF", "SAR", "SBD", "SCR",
    "SDD", "SEK", "SGD", "SHP", "SIT", "SKK", "SLL", "SOS", "SRD", "STD",
    "SVC", "SYP", "SZL", "THB", "TJS", "TMM", "TND", "TOP", "TRL", "TRY",
    "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "USS", "UYU", "UZS",
    "VEB", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC",
    "XBD", "XCD", "XDR", "XFO", "XFU", "XOF", "XPD", "XPF", "XPT", "XTS",
    "XXX", "YER", "ZAR", "ZMK", "ZWD"]

__history__ = """
$Log$
Revision 1.16  2005/11/21 01:55:24  rubys
Commit some (minimal) documentation

Revision 1.15  2005/11/20 20:07:22  rubys
gbase attribute tests

Revision 1.14  2005/11/20 06:52:48  philor
Better slash:hit_parade validation

Revision 1.13  2005/11/20 01:39:50  rubys
Add in country codes

Revision 1.12  2005/11/20 00:36:00  rubys
Initial support for gbase namespace

Revision 1.11  2005/08/30 09:41:52  rubys
foaf:maker at the item level, and dc:title as an attribute on rdf:resources

Revision 1.10  2005/08/22 22:21:34  rubys
creativeCommons support in Atom

Revision 1.9  2005/08/13 22:04:41  rubys
Make Dublin Core less useful, per request of Houghton,Andrew.
Make RFC 3339 message more helpful.

Revision 1.8  2005/08/01 18:26:50  rubys
http://sourceforge.net/mailarchive/forum.php?thread_id=7867731&forum_id=37467

Revision 1.7  2005/07/31 18:50:03  rubys
DcTerms for RSS 2.0, and new link for iTunes doc

Revision 1.6  2005/07/28 09:54:14  rubys
RDF extensions

Revision 1.5  2005/07/17 20:04:05  josephw
Allow trackback extensions in Atom entries.

Revision 1.4  2005/07/08 14:56:13  rubys
Allow slash:comments to be zero.

Revision 1.3  2005/07/06 00:14:23  rubys
Allow dublin core (and more!) on atom feeds

Revision 1.2  2005/07/05 16:06:55  philor
Minimal mod_taxonomy support

Revision 1.1  2005/07/04 22:54:31  philor
Support rest of dc, dcterms, geo, geourl, icbm, and refactor out common extension elements


"""
