from base import validatorBase
from validators import *
from logging import InvalidSseType, InvalidNSS, MissingElement, MissingByAndWhenAttrs
import re

class Sharing(validatorBase):
  def getExpectedAttrNames(self):
    return [ (None, u'expires'), (None, u'since'), (None, u'until') ] 

  def prevalidate(self):
    if self.attrs.has_key((None,'until')):
      self.validate_required_attribute((None,'since'), rfc3339)
    else:
      self.validate_optional_attribute((None,'since'), rfc3339)

    if self.attrs.has_key((None,'since')):
      self.validate_required_attribute((None,'until'), rfc3339)
    else:
      self.validate_optional_attribute((None,'until'), rfc3339)

    self.validate_optional_attribute((None,'expires'), rfc3339)

    if self.attrs.has_key((None,'since')):
      if self.attrs.has_key((None,'until')):
        if self.attrs[(None,'since')]>self.attrs[(None,'until')]:
          self.log(SinceAfterUntil({}))

  def do_sx_related(self):
    return Related()

class Sync(validatorBase):
  def getExpectedAttrNames(self):
    return [ (None, u'deleted'), (None, u'noconflicts'),
             (None, u'id'), (None, u'updates') ]

  def prevalidate(self):
    self.validate_optional_attribute((None,'deleted'), truefalsestrict)
    self.validate_optional_attribute((None,'noconflicts'), truefalsestrict)
    self.validate_required_attribute((None,'id'), unique('id',self.parent.parent))
    self.validate_optional_attribute((None,'id'), rfc2141_nss)
    self.validate_required_attribute((None,'updates'), UINT31)

  def validate(self):
    if not 'sx_history' in self.children:
      self.log(MissingElement({'parent':self.name, 'element':'sx:history'}))

  def do_sx_history(self):
    return History()

  def do_sx_conflicts(self):
    return Conflicts()

class Related(validatorBase):
  def getExpectedAttrNames(self):
    return [ (None, u'link'), (None, u'title'), (None, u'type') ]

  def prevalidate(self):
    self.validate_required_attribute((None,'link'), rfc2396_full)
    self.validate_optional_attribute((None,'title'), nonhtml)
    self.validate_optional_attribute((None,'title'), nonblank)
    self.validate_required_attribute((None,'type'), FeedType)

class History(validatorBase):
  def getExpectedAttrNames(self):
    return [ (None, u'by'), (None, u'sequence'), (None, u'when') ]

  def prevalidate(self):
    self.validate_optional_attribute((None,'by'), nonhtml)
    self.validate_optional_attribute((None,'by'), nonblank)
    self.validate_optional_attribute((None,'by'), rfc2141_nss)
    self.validate_required_attribute((None,'sequence'), UINT31)
    self.validate_optional_attribute((None,'when'), rfc3339)

    if self.attrs.has_key((None,'when')):
      if not self.attrs.has_key((None,'by')):
        self.log(MissingRecommendedAttribute({"attr":"by"}))
    elif self.attrs.has_key((None,'by')):
      self.log(MissingRecommendedAttribute({"attr":"when"}))
    else:
      self.log(MissingByAndWhenAttrs({}))

class FeedType(enumeration):
  error = InvalidSseType
  valuelist = ['complete', 'aggregated']

class rfc2141_nss(text):
  def validate(self):
    if not re.match("^([0-9a-zA-Z()+,\\-\\.:=@;$_!*'/?#]|%[0-9a-fA-F][0-9a-fA-F])+$", self.value):
     self.log(InvalidNSS({"element":self.name,"parent":self.parent.name}))

class Conflicts(validatorBase):
  def do_entry(self): 
    from entry import entry
    return entry()
  def do_item(self): 
    from item import item
    return item()
