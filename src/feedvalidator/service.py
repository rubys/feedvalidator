from base import validatorBase
from validators import *

class service(validatorBase):
  def getExpectedAttrNames(self):
    return [] # (None,u'scheme'),(None,u'fixed')]

  def prevalidate(self):
    pass

  def do_app_workspace(self):
    return workspace()

class workspace(validatorBase):
  def do_app_collection(self):
    return collection()

  def do_atom_title(self):
    from content import textConstruct
    return textConstruct(), noduplicates()

class collection(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,u'href')]

  def do_atom_title(self):
    from content import textConstruct
    return textConstruct(), noduplicates()

  def do_app_categories(self):
    from categories import categories
    return categories()

  def do_app_accept(self):
    from categories import categories
    return MimeType()
