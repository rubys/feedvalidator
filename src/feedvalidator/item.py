"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *
from logging import *
from sets import ImmutableSet

#
# item element.
#
class item(validatorBase):

  def validate(self):
    if not "link" in self.children:
      self.log(MissingItemLink({"parent":self.name, "element":"link"}))
    if not "title" in self.children:
      self.log(MissingItemTitle({"parent":self.name, "element":"title"}))
    if (not "title" in self.children) and (not "description" in self.children):
      self.log(ItemMustContainTitleOrDescription({}))

  def do_link(self):
    return rfc2396_full(), noduplicates()
  
  def do_comments(self):
    return rfc2396_full(), noduplicates()

  def do_annotate_reference(self):
    return annotate_reference(), noduplicates()
  
  def do_title(self):
    return nonhtml(), noduplicates()

  def do_description(self):
    return nonhtml(), noduplicates()

  def do_enclosure(self):
    return enclosure()
  
  def do_pubDate(self):
    if "dc_date" in self.children:
      self.log(DuplicateItemSemantics({"core":"pubDate", "ext":"dc:date"}))
    self.log(UseDCDate({"core":"pubDate", "ext":"dc:date"}))
    return rfc822(), noduplicates()

  def do_author(self):
    if "dc_creator" in self.children:
      self.log(DuplicateItemSemantics({"core":"author", "ext":"dc:creator"}))
    self.log(UseDCCreator({"core":"author", "ext":"dc:creator"}))
    return email(), noduplicates()

  def do_category(self):
    if "dc_subject" in self.children:
      self.log(DuplicateItemSemantics({"core":"category", "ext":"dc:subject"}))
    self.log(UseDCSubject({"core":"category", "ext":"dc:subject"}))
    return category()

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
    return iso8601(), noduplicates()

  def do_source(self):
    if "dc_source" in self.children:
      self.log(DuplicateItemSemantics({"core":"source", "ext":"dc:source"}))
    self.log(UseDCSource({"core":"source", "ext":"dc:source"}))
    return source(), noduplicates()

  def do_dc_source(self):
    if "source" in self.children:
      self.log(DuplicateItemSemantics({"core":"source", "ext":"dc:source"}))
    return text(), noduplicates()

  def do_guid(self):
    return guid(), noduplicates(), unique('guid',self.parent)

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

  def do_xhtml_body(self):
    return htmlEater(self,'xhtml:body')

class category(text):
  def getExpectedAttrNames(self):
    return ImmutableSet([(None, u'domain')])

class source(text, httpURLMixin):
  def getExpectedAttrNames(self):
    return ImmutableSet([(None, u'url')])
  def prevalidate(self):
    try:
      self.validateHttpURL(None, 'url')
    except KeyError:
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":'url'}))
    return text.prevalidate(self)

class enclosure(validatorBase, httpURLMixin):
  from validators import mime_re
  def getExpectedAttrNames(self):
    return ImmutableSet([(None, u'url'), (None, u'length'), (None, u'type')])
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
    return ImmutableSet([(None, u'isPermaLink')])

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
    else:
      self.log(ValidHttpGUID({"parent":self.parent.name, "element":self.name}))
      return noduplicates.validate(self)

class annotate_reference(rdfResourceURI): pass

__history__ = """
$Log$
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
