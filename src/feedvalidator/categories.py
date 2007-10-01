from base import validatorBase
from category import category
from validators import yesno
from logging import ConflictingCatAttr, ConflictingCatChildren

class categories(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,u'scheme'),(None,u'fixed'),(None,u'href')]

  def prevalidate(self):
    self.validate_optional_attribute((None,'fixed'), yesno)

    if self.attrs.has_key((None,'href')):
      if self.attrs.has_key((None,'fixed')):
        self.log(ConflictingCatAttr({'attr':'fixed'}))
      if self.attrs.has_key((None,'scheme')):
        self.log(ConflictingCatAttr({'attr':'scheme'}))

  def validate(self):
    if self.attrs.has_key((None,'href')) and self.children:
      self.log(ConflictingCatChildren({}))

  def do_atom_category(self):
    return category()
