"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *

#
# image element.
#
class image(validatorBase):
  def validate(self):
    if self.attrs.has_key((rdfNS,"resource")):
      return # looks like an RSS 1.0 feed
    if not "link" in self.children:
      self.log(MissingLink({"parent":self.name, "element":"link"}))
    if not "title" in self.children:
      self.log(MissingTitle({"parent":self.name, "element":"title"}))
    if not "url" in self.children:
      self.log(MissingElement({"parent":self.name, "element":"url"}))

  def do_title(self):
    return title(), noduplicates()

  def do_link(self):
    return rfc2396(), noduplicates()

  def do_url(self):
    return rfc2396(), noduplicates()

  def do_width(self):
    return width(), noduplicates()

  def do_height(self):
    return height(), noduplicates()

  def do_description(self):
    return nonhtml(), noduplicates()
  
class title(text, noduplicates):
  def validate(self):
    if not self.value.strip():
      self.log(NotBlank({"parent":self.parent.name, "element":self.name}))
    else:
      self.log(ValidTitle({"parent":self.parent.name, "element":self.name}))
    return nonhtml()

class width(text, noduplicates):
  def validate(self):
    try:
      w = int(self.value)
      if (w <= 0) or (w > 144):
        self.log(InvalidWidth({"parent":self.parent.name, "element":self.name, "value":self.value}))
      else:
        self.log(ValidWidth({"parent":self.parent.name, "element":self.name}))
        if w > 88:
          self.log(RecommendedWidth({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidWidth({"parent":self.parent.name, "element":self.name, "value":self.value}))

class height(text, noduplicates):
  def validate(self):
    try:
      h = int(self.value)
      if (h <= 0) or (h > 400):
        self.log(InvalidHeight({"parent":self.parent.name, "element":self.name, "value":self.value}))
      else:
        self.log(ValidHeight({"parent":self.parent.name, "element":self.name}))
        if h > 31:
          self.log(RecommendedHeight({"parent":self.parent.name, "element":self.name, "value":self.value}))
    except ValueError:
      self.log(InvalidHeight({"parent":self.parent.name, "element":self.name, "value":self.value}))

__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:15  rubys
Initial revision

Revision 1.11  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.10  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.9  2002/10/24 14:47:33  f8dy
decoupled "no duplicates" check from individual validator classes,
allow handlers to return multiple validator classes

Revision 1.8  2002/10/22 17:29:52  f8dy
loosened restrictions on link/docs/url protocols; RSS now allows any
IANA protocol, not just http:// and ftp://

Revision 1.7  2002/10/22 16:43:55  rubys
textInput vs textinput: don't reject valid 1.0 feeds, but don't allow
invalid textinput fields in RSS 2.0 either...

Revision 1.6  2002/10/18 15:41:33  f8dy
added (and passed) testcases for unallowed duplicates of the same element

Revision 1.5  2002/10/18 13:06:57  f8dy
added licensing information

"""
