"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *

#
# Atom generator element
#
class generator(nonhtml,rfc2396):
  def getExpectedAttrNames(self):
    return [(None, u'uri'), (None, u'version')]

  def prevalidate(self):
    if self.attrs.has_key((None, "url")):
      self.value = self.attrs.getValue((None, "url"))
      rfc2396.validate(self, extraParams={"attr": "url"})
    if self.attrs.has_key((None, "uri")):
      self.value = self.attrs.getValue((None, "uri"))
      rfc2396.validate(self, errorClass=InvalidURIAttribute, extraParams={"attr": "uri"})
    self.value=''
