"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from logging import *
from validators import rdfAbout, noduplicates

#
# rdf:RDF element.  The valid children include "channel", "item", "textinput", "image"
#
class rdf(validatorBase):
  def do_channel(self):
    from channel import channel
    return rdfAbout(), channel(), noduplicates()

  def do_item(self):
    from item import item
    return rdfAbout(), item()

  def do_textinput(self):
    from textInput import textInput
    return textInput()

  def do_image(self):
    from image import image
    return image()
  
  def prevalidate(self):
    self.setFeedType(TYPE_RSS1)
    
  def validate(self):
    if not "channel" in self.children:
      self.log(MissingChannel({"parent":self.name, "element":"channel"}))

__history__ = """
$Log$
Revision 1.1  2004/02/03 17:33:16  rubys
Initial revision

Revision 1.10  2003/12/11 16:32:08  f8dy
fixed id tags in header

Revision 1.9  2003/10/16 15:54:41  rubys
Detect duplicate channels

Revision 1.8  2003/08/12 00:26:30  rubys
Misleading error message if a channel is missing in an RSS 1.0 feed

Revision 1.7  2003/08/10 13:49:14  rubys
Add support for chanel and item level rdf:about.  Ensure that http and
ftp URLs have exactly two slashes after the scheme.

Revision 1.6  2003/07/29 19:38:07  f8dy
changed test cases to explicitly test for success (rather than the absence of failure)

Revision 1.5  2003/07/09 16:24:30  f8dy
added global feed type support

Revision 1.4  2002/10/22 14:11:36  f8dy
initial attempts to handle RSS 1.0 vs. 2.0 images and textinputs; test
cases still fail

Revision 1.3  2002/10/22 13:16:03  f8dy
passed lowercase textinput test

Revision 1.2  2002/10/18 13:06:57  f8dy
added licensing information

"""
