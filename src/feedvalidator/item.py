"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *
from logging import *
from itunes import itunes_item

#
# item element.
#
class item(validatorBase, itunes_item):
  def validate(self):
    if not "link" in self.children:
      self.log(MissingItemLink({"parent":self.name, "element":"link"}))
    if not "title" in self.children:
      self.log(MissingItemTitle({"parent":self.name, "element":"title"}))
    if (not "title" in self.children) and (not "description" in self.children):
      self.log(ItemMustContainTitleOrDescription({}))
        
  def do_link(self):
    return rfc2396_full(), noduplicates()
  
  def do_annotate_reference(self):
    return annotate_reference(), noduplicates()
  
  def do_title(self):
    return nonhtml(), noduplicates()

  def do_description(self):
    return safeHtml(), noduplicates()

  def do_dc_subject(self):
    if "category" in self.children:
      self.log(DuplicateItemSemantics({"core":"category", "ext":"dc:subject"}))
    return text()

  def do_dc_creator(self):
    if "author" in self.children:
      self.log(DuplicateItemSemantics({"core":"author", "ext":"dc:creator"}))
    return text()

  def do_dc_date(self):
    if "pubDate" in self.children:
      self.log(DuplicateItemSemantics({"core":"pubDate", "ext":"dc:date"}))
    return w3cdtf(), noduplicates()

  def do_dcterms_created(self):
    return w3cdtf(), noduplicates()

  def do_dcterms_issued(self):
    return w3cdtf(), noduplicates()

  def do_dcterms_modified(self):
    return w3cdtf(), noduplicates()

  def do_dc_source(self):
    if "source" in self.children:
      self.log(DuplicateItemSemantics({"core":"source", "ext":"dc:source"}))
    return text(), noduplicates()

  def do_dc_language(self):
    return iso639(), noduplicates()

  def do_content_encoded(self):
    return safeHtml(), noduplicates()

  def do_cc_license(self):
    if "creativeCommons_license" in self.children:
      self.log(DuplicateSemantics({"core":"creativeCommons:license", "ext":"cc:license"}))
    return eater()

  def do_creativeCommons_license(self):
    if "cc_license" in self.children:
      self.log(DuplicateSemantics({"core":"creativeCommons:license", "ext":"cc:license"}))
    return rfc2396_full()

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

  def do_slash_comments(self):
    return positiveInteger()

  def do_slash_section(self):
    return text()

  def do_slash_department(self):
    return text()

  def do_slash_hit_parade(self):
    return text() # TODO: should be comma-separated integers

  def do_xhtml_body(self):
    return htmlEater(self,'xhtml:body')

  def do_atom_id(self):
    return rfc2396_full(), noduplicates(), unique('id',self.parent)

  def do_atom_link(self):
    from link import link
    self.links += [link()]
    return self.links[-1]

  def do_atom_title(self):
    from content import content
    return content(), noduplicates()

  def do_atom_summary(self):
    from content import content
    return content(), noduplicates()

  def do_atom_author(self):
    from author import author
    return author(), noduplicates()

  def do_atom_contributor(self):
    from author import author
    return author()

  def do_atom_content(self):
    from content import content
    return content()

  def do_atom_created(self):
    return iso8601_z(), noduplicates()
  
  def do_atom_issued(self):
    return iso8601(), noduplicates()
  
  def do_atom_modified(self):
    return iso8601_z(), noduplicates()

class rss20Item(item):
  def do_comments(self):
    return rfc2396_full(), noduplicates()

  def do_enclosure(self):
    return enclosure(), noduplicates()
  
  def do_pubDate(self):
    if "dc_date" in self.children:
      self.log(DuplicateItemSemantics({"core":"pubDate", "ext":"dc:date"}))
    return rfc822(), noduplicates()

  def do_author(self):
    if "dc_creator" in self.children:
      self.log(DuplicateItemSemantics({"core":"author", "ext":"dc:creator"}))
    return email(), noduplicates()

  def do_category(self):
    if "dc_subject" in self.children:
      self.log(DuplicateItemSemantics({"core":"category", "ext":"dc:subject"}))
    return category()

  def do_guid(self):
    return guid(), noduplicates(), unique('guid',self.parent)

  def do_source(self):
    if "dc_source" in self.children:
      self.log(DuplicateItemSemantics({"core":"source", "ext":"dc:source"}))
    return source(), noduplicates()

class rss10Item(item):
  def validate(self):
    if not "link" in self.children:
      self.log(MissingItemLink({"parent":self.name, "element":"link"}))
    if not "title" in self.children:
      self.log(MissingItemTitle({"parent":self.name, "element":"title"}))

  def getExpectedAttrNames(self):
      return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'about')]

  def do_rdfs_label(self):
      return text()

  def do_rdfs_comment(self):
      return text()

  def do_rdfs_seeAlso(self):
      return eater()

  def prevalidate(self):
    if self.attrs.has_key((rdfNS,"about")):
      about = self.attrs[(rdfNS,"about")]
      if not "abouts" in self.dispatcher.__dict__:
        self.dispatcher.__dict__["abouts"] = []
      if about in self.dispatcher.__dict__["abouts"]:
        self.log(DuplicateValue({"parent":self.name, "element":"rdf:about", "value":about}))
      else:
        self.dispatcher.__dict__["abouts"].append(about)


#
# items element.
#
class items(validatorBase):
  from root import rss11_namespace as rss11_ns

  def getExpectedAttrNames(self):
    return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'parseType')]

  def do_item(self):
    if self.rss11_ns not in self.defaultNamespaces:
      self.log(UndefinedElement({"element":"item","parent":"items"}))
    return rss10Item()

  def do_rdf_Seq(self):
    if self.rss11_ns in self.defaultNamespaces:
      self.log(UndefinedElement({"element":"rdf:Seq","parent":"items"}))
    return rdfSeq()

class rdfSeq(validatorBase):
  def do_rdf_li(self):
    return rdfLi()

class rdfLi(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,u'resource'),
            (u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'resource')]

class category(text):
  def getExpectedAttrNames(self):
    return [(None, u'domain')]

class source(text, httpURLMixin):
  def getExpectedAttrNames(self):
    return [(None, u'url')]
  def prevalidate(self):
    try:
      self.validateHttpURL(None, 'url')
    except KeyError:
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":'url'}))
    return text.prevalidate(self)

class enclosure(validatorBase, httpURLMixin):
  from validators import mime_re
  def getExpectedAttrNames(self):
    return [(None, u'url'), (None, u'length'), (None, u'type')]
  def prevalidate(self):
    try:
      if int(self.attrs.getValue((None, 'length'))) <= 0:
        self.log(InvalidIntegerAttribute({"parent":self.parent.name, "element":self.name, "attr":'length'}))
      else:
        self.log(ValidIntegerAttribute({"parent":self.parent.name, "element":self.name, "attr":'length'}))
    except KeyError:
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":'length'}))
    except ValueError:
      self.log(InvalidIntegerAttribute({"parent":self.parent.name, "element":self.name, "attr":'length'}))

    try:
      if not self.mime_re.match(self.attrs.getValue((None, 'type'))):
        self.log(InvalidMIMEAttribute({"parent":self.parent.name, "element":self.name, "attr":'type'}))
      else:
        self.log(ValidMIMEAttribute({"parent":self.parent.name, "element":self.name, "attr":'type'}))
    except KeyError:
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":'type'}))

    try:
      self.validateHttpURL(None, 'url')
    except KeyError:
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":'url'}))

    return validatorBase.prevalidate(self)

class guid(rfc2396_full, noduplicates):
  def getExpectedAttrNames(self):
    return [(None, u'isPermaLink')]

  def validate(self):
    isPermalink = 1
    try:
      isPermalinkStr = self.attrs.getValue((None, 'isPermaLink'))
      if isPermalinkStr not in ('true', 'false'):
        self.log(InvalidBooleanAttribute({"parent":self.parent.name, "element":self.name, "attr":"isPermaLink"}))
      else:
        self.log(ValidBooleanAttribute({"parent":self.parent.name, "element":self.name, "attr":"isPermaLink"}))
      isPermalink = (isPermalinkStr == 'true')
    except KeyError:
      pass
    if isPermalink:
      return rfc2396.validate(self, InvalidHttpGUID, ValidHttpGUID)
    elif len(self.value)<9 and self.value.isdigit():
      self.log(NotSufficientlyUnique({"parent":self.parent.name, "element":self.name, "value":self.value}))
      return noduplicates.validate(self)
    else:
      self.log(ValidHttpGUID({"parent":self.parent.name, "element":self.name}))
      return noduplicates.validate(self)

class annotate_reference(rdfResourceURI): pass

__history__ = """
$Log$
Revision 1.24  2005/07/03 00:54:29  philor
Support mod_slash, slash_comments for all

Revision 1.23  2005/07/03 00:02:01  philor
Support mod_event

Revision 1.22  2005/07/01 23:55:30  rubys
Initial support for itunes

Revision 1.21  2005/06/30 18:31:00  rubys
Support slash_comments

Revision 1.20  2005/06/29 23:53:56  rubys
Fixes:
  channel level dc:subject and foaf:maker
  item level dc:language and rdfs:seeAlso
  rdf:RDF level cc:License

Revision 1.19  2005/06/28 22:15:15  rubys
Catch errors involving unknown elements in known namespaces

Revision 1.18  2005/01/29 05:41:12  rubys
Fix for [ 1042359 ] invalid RSS 1.0 not flagged as invalid

Revision 1.17  2005/01/29 05:17:41  rubys
Fix for [ 1103931 ] Validator does not detect typo in RSS 1.0

Revision 1.16  2005/01/28 00:06:25  josephw
Use separate 'item' and 'channel' classes to reject RSS 2.0 elements in
 RSS 1.0 feeds (closes 1037785).

Revision 1.15  2005/01/22 01:22:39  rubys
pass testcases/rss11/must/neg-ext-adupabout.xml

Revision 1.14  2005/01/19 01:28:13  rubys
Initial support for rss 1.1

Revision 1.13  2004/12/27 23:41:52  rubys
Tentatively commit test for multiple enclosures.  If it is determined
that multiple enclosures are allowed, the test will be inverted.

Revision 1.12  2004/07/28 11:27:02  rubys
Allow safeHtml without informational messages in description

Revision 1.11  2004/07/28 04:41:55  rubys
Informational messages for text/xml with no charset and uncompressed responses

Revision 1.10  2004/07/28 02:23:41  rubys
Remove some experimental rules

Revision 1.9  2004/03/30 02:42:40  rubys
Flag instances of small positive integers as guids as being "not sufficiently
unique".

Revision 1.8  2004/03/24 00:48:12  rubys
Allow rdf:About on item

Revision 1.7  2004/02/20 15:35:46  rubys
Feature 900555: RSS+Atom support

Revision 1.6  2004/02/18 20:40:54  rubys
Apply additional attributes-fix by josephw

Revision 1.5  2004/02/18 16:12:14  rubys
Make the distiction between W3CDTF and ISO8601 clearer in the docs.

Revision 1.4  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.3  2004/02/17 15:38:39  rubys
Remove email_lax which previously accepted an email address anyplace
within the element

Revision 1.2  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.1.1.1  2004/02/03 17:33:16  rubys
Initial import.

Revision 1.29  2003/12/12 11:25:56  rubys
Validate mime type in link tags

Revision 1.28  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.27  2003/08/23 21:01:00  rubys
Validate that content, content:encoded, and xhtml:body are safe

Revision 1.26  2003/08/04 00:03:14  rubys
Implement more strict email check for pie

Revision 1.25  2003/07/30 01:54:59  f8dy
tighten test cases, add explicit params

Revision 1.24  2003/07/29 20:57:39  f8dy
tightened up test cases, check for parent element, explicitly test for success

Revision 1.23  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.22  2003/07/20 17:44:27  rubys
Detect duplicate ids and guids

Revision 1.21  2003/01/11 03:59:26  rubys
dashes are legal in MIME types

Revision 1.20  2002/12/20 13:26:00  rubys
CreativeCommons support

Revision 1.19  2002/10/24 14:47:33  f8dy
decoupled "no duplicates" check from individual validator classes,
allow handlers to return multiple validator classes

Revision 1.18  2002/10/22 17:29:52  f8dy
loosened restrictions on link/docs/url protocols; RSS now allows any
IANA protocol, not just http:// and ftp://

Revision 1.17  2002/10/18 15:46:35  f8dy
added (and passed) rule for no multiple content:encoded

Revision 1.16  2002/10/18 14:17:30  f8dy
added tests for language/dc:language (must be valid ISO-639 language code
plus optional country code) and passed them

Revision 1.15  2002/10/18 13:06:57  f8dy
added licensing information

"""
