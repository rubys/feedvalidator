"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from validators import *

#
# textInput element.
#
class textInput(validatorBase):
  def validate(self):
    if not "title" in self.children:
      self.log(MissingTitle({"parent":self.name, "element":"title"}))
    if not "link" in self.children:
      self.log(MissingLink({"parent":self.name, "element":"link"}))
    if not "description" in self.children:
      self.log(MissingDescription({"parent":self.name,"element":"description"}))
    if not "name" in self.children:
      self.log(MissingElement({"parent":self.name, "element":"name"}))

  def do_title(self):
    return nonhtml(), noduplicates()

  def do_description(self):
    return nonhtml(), noduplicates()

  def do_name(self):
    return nonhtml(), noduplicates()

  def do_link(self):
    return rfc2396(), noduplicates()

__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:16  rubys
Initial revision

Revision 1.6  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.5  2002/10/24 14:47:33  f8dy
decoupled "no duplicates" check from individual validator classes,
allow handlers to return multiple validator classes

Revision 1.4  2002/10/22 17:29:52  f8dy
loosened restrictions on link/docs/url protocols; RSS now allows any
IANA protocol, not just http:// and ftp://

Revision 1.3  2002/10/18 13:06:57  f8dy
added licensing information

"""
