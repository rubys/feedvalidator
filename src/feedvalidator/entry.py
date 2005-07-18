"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *
from logging import *
from extension import extension_entry

#
# pie/echo entry element.
#
class entry(validatorBase, extension_entry):

  def prevalidate(self):
    self.links=[]
    self.content=None

  def validate(self):
    if not 'title' in self.children:
      self.log(MissingElement({"parent":self.name, "element":"title"}))
    if not 'author' in self.children and not 'author' in self.parent.children:
      self.log(MissingElement({"parent":self.name, "element":"author"}))
    if not 'id' in self.children:
      self.log(MissingElement({"parent":self.name, "element":"id"}))
    if not 'updated' in self.children:
      self.log(MissingElement({"parent":self.name, "element":"updated"}))

    if self.content:
      if not 'summary' in self.children:
        if self.content.attrs.has_key((None,"src")):
          self.log(MissingTextualContent({"parent":self.parent.name, "element":self.name}))
      ctype = self.content.type
      if ctype.find('/') > -1 and not (
         ctype.endswith('+xml') or ctype.endswith('/xml') or
         ctype.startswith('text/')):
        self.log(MissingTextualContent({"parent":self.parent.name, "element":self.name}))
    else:
      if not 'summary' in self.children:
        self.log(MissingTextualContent({"parent":self.parent.name, "element":self.name}))
      for link in self.links:
        if link.rel == 'alternate': break
      else:
        self.log(MissingContentOrAlternate({"parent":self.parent.name, "element":self.name}))

    # can only have one alternate per type
    types={}
    for link in self.links:
      if not link.rel=='alternate': continue
      if not link.type in types: types[link.type]=[]
      if link.hreflang in types[link.type]:
        self.log(DuplicateAtomLink({"parent":self.name, "element":"link", "type":link.type, "hreflang":link.hreflang}))
      else:
        types[link.type] += [link.hreflang]

  def do_author(self):
    from author import author
    return author()

  def do_category(self):
    from category import category
    return category()

  def do_content(self):
    from content import content
    self.content=content()
    return self.content, noduplicates()

  def do_contributor(self):
    from author import author
    return author()

  def do_id(self):
    return rfc2396_full(), noduplicates(), unique('id',self.parent,DuplicateEntries), canonicaluri()

  def do_link(self):
    from link import link
    self.links += [link()]
    return self.links[-1]

  def do_published(self):
    return iso8601(), noduplicates()

  def do_source(self):
    return source(), noduplicates()

  def do_rights(self):
    from content import textConstruct
    return textConstruct(), noduplicates()

  def do_summary(self):
    from content import textConstruct
    return textConstruct(), noduplicates()

  def do_title(self):
    from content import textConstruct
    return textConstruct(), noduplicates()
  
  def do_updated(self):
    return iso8601_z(), noduplicates()
  
class pie_entry(entry):

  def validate(self):
    if not 'summary' in self.children:
      self.children.append('summary')
    if not 'updated' in self.children:
      self.children.append('updated')
    entry.validate(self)
    if not 'modified' in self.children:
      self.log(MissingElement({"parent":self.name, "element":"modified"}))
    if not 'issued' in self.children:
      self.log(MissingElement({"parent":self.name, "element":"issued"}))

    # must have an alternate
    if [link for link in self.links if link.rel == u'alternate']:
      self.log(ValidAtomLinkRel({"parent":self.name, "element":"link", "attr":"rel", "attrvalue":"alternate"}))
    else:
      self.log(MissingAlternateLink({"parent":self.name, "element":"link", "attr":"rel", "attrvalue":"alternate"}))

  def do_created(self):
    return iso8601_z(), noduplicates()
  
  def do_content(self):
    from content import pie_content
    self.content=pie_content()
    return self.content

  def do_title(self):
    from content import pie_content
    return pie_content(), noduplicates()

  def do_summary(self):
    from content import pie_content
    return pie_content(), noduplicates()

  def do_issued(self):
    return iso8601(), noduplicates()
  
  def do_modified(self):
    return iso8601_z(), noduplicates()

from feed import feed
class source(feed):
  def do_author(self):
    if not 'author' in self.parent.children:
      self.parent.children.append('author')
    return feed.do_author(self)

  def do_entry(self):
    self.log(UndefinedElement({"parent":self.parent.name, "element":self.name}))
    return eater()

__history__ = """
$Log$
Revision 1.10  2005/07/18 12:20:46  rubys
Atom 1.0 section 4.1.2

Revision 1.9  2005/07/17 23:22:44  rubys
Atom 1.0 section 4.1.1.1

Revision 1.8  2005/07/17 18:49:18  rubys
Atom 1.0 section 4.1

Revision 1.7  2005/07/16 14:40:09  rubys
More Atom 1.0 support

Revision 1.6  2005/07/15 11:17:24  rubys
Baby steps towards Atom 1.0 support

Revision 1.5  2005/07/06 00:14:23  rubys
Allow dublin core (and more!) on atom feeds

Revision 1.4  2005/01/25 11:16:44  josephw
Warn about non-canonical URIs used as Atom identifiers.

Revision 1.3  2004/05/26 18:36:48  f8dy
added test cases for link rel="related", rel="via", and rel="parent"

Revision 1.2  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.1.1.1  2004/02/03 17:33:15  rubys
Initial import.

Revision 1.13  2003/12/12 14:35:08  f8dy
fixed link rel=alternate logic to pass new "link not missing" tests

Revision 1.12  2003/12/12 06:10:58  rubys
link rel/type checking

Revision 1.11  2003/12/12 05:42:05  rubys
Rough in some support for the new link syntax

Revision 1.10  2003/12/11 18:20:46  f8dy
passed all content-related testcases

Revision 1.9  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.8  2003/08/05 14:28:26  rubys
Allow author to be omitted from entries when present on the feed

Revision 1.7  2003/08/05 07:59:04  rubys
Add feed(id,tagline,contributor)
Drop feed(subtitle), entry(subtitle)
Check for obsolete version, namespace
Check for incorrect namespace on feed element

Revision 1.6  2003/07/20 17:48:50  rubys
Validate that titles are present

Revision 1.5  2003/07/20 17:44:27  rubys
Detect duplicate ids and guids

Revision 1.4  2003/07/20 16:35:57  rubys
Ensure that issued and modified are present exactly once

Revision 1.3  2003/07/07 10:35:50  rubys
Complete first pass of echo/pie tests

Revision 1.2  2003/07/07 02:44:13  rubys
Further progress towards pie

Revision 1.1  2003/07/07 00:54:00  rubys
Rough in some pie/echo support

"""
