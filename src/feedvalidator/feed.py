"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *
from logging import *
from extension import extension_feed

#
# Atom root element
#
class feed(validatorBase, extension_feed):
  def prevalidate(self):
    self.links = []
    
  def missingElement(self, params):
    self.log(MissingElement(params))

  def validate_metadata(self):
    if not 'title' in self.children:
      self.missingElement({"parent":self.name, "element":"title"})
    if not 'id' in self.children:
      self.missingElement({"parent":self.name, "element":"id"})
    if not 'updated' in self.children:
      self.missingElement({"parent":self.name, "element":"updated"})

    # ensure that there is a link rel="self"
    for link in self.links:
      if link.rel=='self': break
    else:
      self.log(MissingSelf({"parent":self.parent.name, "element":self.name}))

    # link/type pair must be unique
    types={}
    for link in self.links:
      if not link.type in types: types[link.type]={}
      if link.rel in types[link.type]:
        if link.hreflang in types[link.type][link.rel]:
          self.log(DuplicateAtomLink({"parent":self.name, "element":"link", "type":link.type, "hreflang":link.hreflang}))
        else:
          types[link.type][link.rel] += [link.hreflang]
      else:
        types[link.type][link.rel] = [link.hreflang]

  def metadata(self):
    if 'entry' in self.children:
      self.log(MisplacedMetadata({"parent":self.name, "element":self.child}))

  def validate(self):
    if not 'entry' in self.children:
      self.validate_metadata()
      if not 'author' in self.children:
        self.log(MissingElement({"parent":self.name, "element":"author"}))

  def do_author(self):
    self.metadata()
    from author import author
    return author()

  def do_category(self):
    self.metadata()
    from category import category
    return category()

  def do_contributor(self):
    self.metadata()
    from author import author
    return author()

  def do_generator(self):
    self.metadata()
    from generator import generator
    return generator(), nonblank(), noduplicates()

  def do_id(self):
    self.metadata()
    return canonicaluri(), noduplicates()

  def do_icon(self):
    self.metadata()
    return nonblank(), rfc2396(), noduplicates()

  def do_link(self):
    self.metadata()
    from link import link
    self.links += [link()]
    return self.links[-1]

  def do_logo(self):
    self.metadata()
    return nonblank(), rfc2396(), noduplicates()

  def do_title(self):
    self.metadata()
    from content import textConstruct
    return textConstruct(), noduplicates()
  
  def do_subtitle(self):
    self.metadata()
    from content import textConstruct
    return textConstruct(), noduplicates()
  
  def do_rights(self):
    self.metadata()
    from content import textConstruct
    return textConstruct(), noduplicates()

  def do_updated(self):
    self.metadata()
    return iso8601_z(), noduplicates()

  def do_entry(self):
    if not 'entry' in self.children:
      self.validate_metadata()
    from entry import entry
    return entry()

  def do_xhtml_div(self):
    return eater()

class pie_feed(feed):
  def getExpectedAttrNames(self):
      return [(None, u'version')]

  def do_link(self):
    self.metadata()
    from link import pie_link
    self.links += [pie_link()]
    return self.links[-1]

  def do_title(self):
    from content import pie_content
    return pie_content(), noduplicates()

  def do_info(self):
    from content import pie_content
    return pie_content(), noduplicates()
  
  def prevalidate(self):
    feed.prevalidate(self)
    
    try:
      version = self.attrs.getValue((None,'version'))
      if not version:
        self.log(MissingAttribute({"element":self.name, "attr":"version"}))
      elif version in ['0.1', '0.2', '0.2.1']:
        self.log(ObsoleteVersion({"element":self.name, "version":version}))
      else:
        try:
          float(version)
	except:
          self.log(InvalidValue({"element":self.name, "attr":"version", "value":version}))
    except:
      self.log(MissingAttribute({"element":self.name, "attr":"version"}))

  def validate(self):
    if not 'title' in self.children:
      self.log(MissingElement({"parent":self.name, "element":"title"}))
    if not 'modified' in self.children:
      self.log(MissingElement({"parent":self.name, "element":"modified"}))

    # link/type pair must be unique
    types={}
    for link in self.links:
      if not link.type in types: types[link.type]=[]
      if link.rel in types[link.type]:
        self.log(DuplicateAtomLink({"parent":self.name, "element":"link"}))
      else:
        types[link.type] += [link.rel]

    # must have an alternate
    if [link for link in self.links if link.rel == u'alternate']:
      self.log(ValidAtomLinkRel({"parent":self.name, "element":"link", "attr":"rel", "attrvalue":"alternate"}))
    else:
      self.log(MissingAlternateLink({"parent":self.name, "element":"link", "attr":"rel", "attrvalue":"alternate"}))

  def do_tagline(self):
    from content import pie_content
    return pie_content(), noduplicates()

  def do_copyright(self):
    from content import pie_content
    return pie_content(), noduplicates()

  def do_modified(self):
    return iso8601_z(), noduplicates()

  def do_entry(self):
    from entry import pie_entry
    return pie_entry()

__history__ = """
$Log$
Revision 1.22  2005/08/03 04:40:08  rubys
whitespace

Revision 1.21  2005/07/25 00:40:54  rubys
Convert errors to warnings

Revision 1.20  2005/07/21 14:19:53  rubys
unregistered Atom 1.0 link rel

Revision 1.19  2005/07/19 19:57:46  rubys
Few things I spotted...

Revision 1.18  2005/07/19 01:08:04  rubys
Atom 1.0 section 4.2.6

Revision 1.17  2005/07/18 23:22:12  rubys
Atom 4.2.2.1, 4.2.4, 4.2.5

Revision 1.16  2005/07/17 23:22:44  rubys
Atom 1.0 section 4.1.1.1

Revision 1.15  2005/07/17 19:07:14  rubys
Fix error in producing error message

Revision 1.14  2005/07/17 18:49:18  rubys
Atom 1.0 section 4.1

Revision 1.13  2005/07/16 22:01:14  rubys
Atom 1.0 text constructs and relative URIs

Revision 1.12  2005/07/16 14:40:09  rubys
More Atom 1.0 support

Revision 1.11  2005/07/16 00:24:34  rubys
Through section 2

Revision 1.10  2005/07/15 11:17:24  rubys
Baby steps towards Atom 1.0 support

Revision 1.9  2005/07/06 00:14:23  rubys
Allow dublin core (and more!) on atom feeds

Revision 1.8  2005/06/27 16:02:42  rubys
Allow duplicate contributors at the feed level

Revision 1.7  2004/04/05 23:54:42  rubys
Fix bug 929794: verify version attribute

Revision 1.6  2004/02/28 03:25:24  rubys
Report obsolete version on the start element instead of the end element

Revision 1.5  2004/02/18 19:14:55  rubys
Feed modified is required

Revision 1.4  2004/02/17 23:17:45  rubys
Commit fixes for bugs 889545 and 893741: requiring non-relative URLs in
places where a relative URL is OK (example: rdf).

Revision 1.3  2004/02/17 22:42:02  rubys
Remove dependence on Python 2.3

Revision 1.2  2004/02/16 16:25:25  rubys
Fix for bug 890053: detecting unknown attributes, based largely
on patch 895910 by Joseph Walton.

Revision 1.1.1.1  2004/02/03 17:33:15  rubys
Initial import.

Revision 1.15  2003/12/12 14:35:08  f8dy
fixed link rel=alternate logic to pass new "link not missing" tests

Revision 1.14  2003/12/12 11:30:39  rubys
Validate feed links

Revision 1.13  2003/12/12 05:42:05  rubys
Rough in some support for the new link syntax

Revision 1.12  2003/12/11 23:16:32  f8dy
passed new generator test cases

Revision 1.11  2003/12/11 20:13:58  f8dy
feed title, copyright, and tagline may be blank

Revision 1.10  2003/12/11 18:20:46  f8dy
passed all content-related testcases

Revision 1.9  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.8  2003/12/11 04:50:53  f8dy
added test cases for invalid letters in urn NSS, fixed RE to match

Revision 1.7  2003/08/05 15:03:19  rubys
Handle complex (nested) content.  Remove copy/paste error in handing
of copyright.

Revision 1.6  2003/08/05 14:03:23  rubys
Tagline is optional

Revision 1.5  2003/08/05 07:59:04  rubys
Add feed(id,tagline,contributor)
Drop feed(subtitle), entry(subtitle)
Check for obsolete version, namespace
Check for incorrect namespace on feed element

Revision 1.4  2003/08/03 18:46:04  rubys
support author(url,email) and feed(author,copyright,generator)

Revision 1.3  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.2  2003/07/07 10:35:50  rubys
Complete first pass of echo/pie tests

Revision 1.1  2003/07/07 00:54:00  rubys
Rough in some pie/echo support

"""
