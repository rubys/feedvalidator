from base import validatorBase
from category import category

class categories(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,u'scheme'),(None,u'fixed'),(None,u'href')]

  def prevalidate(self):
    pass

  def do_atom_category(self):
    return category()
