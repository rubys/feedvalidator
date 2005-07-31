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
    return w3cdtf(), noduplicates()

  def do_dcterms_dateCopyrighted(self):
    return w3cdtf(), noduplicates()

  def do_dcterms_dateSubmitted(self):
    return w3cdtf(), noduplicates()

  def do_dcterms_extent(self):
    return positiveInteger(), noduplicates()

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

  def do_dcterms_accessRights(self):
    return text(), noduplicates()


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

  def do_foaf_primaryTopic(self):
    return eater()

  def do_slash_comments(self):
    return nonNegativeInteger()

  def do_slash_section(self):
    return text()

  def do_slash_department(self):
    return text()

  def do_slash_hit_parade(self):
    return text() # TODO: should be comma-separated integers

  def do_taxo_topics(self):
    return eater()

  def do_thr_children(self):
    return eater()

class extension_rss20_item(extension_item):
  def do_trackback_ping(self):
    return rfc2396_full(), noduplicates()

  def do_trackback_about(self):
    return rfc2396_full()

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
    return sy_updateFrequency(), noduplicates()

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

# revisit these once Atom 1.0 comes out (issue warning on duplicate semantics)
class extension_entry(extension_item):
  def do_dc_creator(self): # atom:creator
    return text() # duplicates allowed
  def do_dc_subject(self): # atom:category
    return text() # duplicates allowed
  def do_dc_date(self): # atom:published
    return w3cdtf(), noduplicates()

  def do_trackback_ping(self):
    return rfc2396_full(), noduplicates()

  # XXX This should have duplicate semantics with link[@rel='related']
  def do_trackback_about(self):
    return rfc2396_full()

class admin_generatorAgent(rdfResourceURI): pass
class admin_errorReportsTo(rdfResourceURI): pass

class sy_updateFrequency(positiveInteger): pass

class sy_updatePeriod(text):
  def validate(self):
    if self.value not in ('hourly', 'daily', 'weekly', 'monthly', 'yearly'):
      self.log(InvalidUpdatePeriod({"parent":self.parent.name, "element":self.name, "value":self.value}))
    else:
      self.log(ValidUpdatePeriod({"parent":self.parent.name, "element":self.name, "value":self.value}))

__history__ = """
$Log$
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
