from validators import *
from logging import *

class Query(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,attr) for attr in ['role', 'title', 'totalResults',
      'searchTerms', 'count', 'startIndex', 'startPage', 'language',
      'inputEncoding', 'xutputEncoding', 'parameter']]

  def validate(self):
    self.validate_required_attribute((None,'role'), QueryRole)
    self.validate_optional_attribute((None,'title'), lengthLimitedText(256))
    self.validate_optional_attribute((None,'title'), nonhtml)
    self.validate_optional_attribute((None,'totalResults'), nonNegativeInteger)
    self.validate_optional_attribute((None,'searchTerms'), UrlEncoded)
    self.validate_optional_attribute((None,'count'), nonNegativeInteger)
    self.validate_optional_attribute((None,'startIndex'), Integer)
    self.validate_optional_attribute((None,'startPage'), Integer)
    self.validate_optional_attribute((None,'language'), iso639)
    self.validate_optional_attribute((None,'inputEncoding'), Charset)
    self.validate_optional_attribute((None,'outputEncoding'), Charset)

class QueryRole(enumeration):
  error = InvalidLocalRole
  valuelist = ['request', 'example', 'related', 'correction', 'subset',
    'superset']
  def validate(self):
    if self.value.find(':')<0:
      enumeration.validate(self)
    else:
      pass # TBD: check for role extension

class UrlEncoded(validatorBase):
  def validate(self):
    from urllib import quote, unquote
    import re
    for value in self.value.split():
      value = re.sub('%\w\w', lambda x: x.group(0).lower(), value)
      if value != quote(unquote(value)):
        self.log(NotURLEncoded({}))
        break
