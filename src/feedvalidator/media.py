from validators import *

class media_elements:
  def do_media_adult(self):
    return media_truefalse(), noduplicates()
  def do_media_category(self):
    return media_category()
  def do_media_credit(self):
    return media_credit()
  def do_media_copyright(self):
    return media_copyright(), noduplicates()
  def do_media_description(self):
    return media_title(), noduplicates()
  def do_media_keywords(self):
    return text(), noduplicates()
  def do_media_hash(self):
    return media_hash()
  def do_media_player(self):
    return media_player(), noduplicates()
  def do_media_rating(self):
    return text(), noduplicates()
  def do_media_restriction(self):
    return media_restriction(), noduplicates()
  def do_media_text(self):
    return media_text(), noduplicates()
  def do_media_title(self):
    return media_title(), noduplicates()
  def do_media_thumbnail(self):
    return media_thumbnail(), noduplicates()

class media_category(text):
  def getExpectedAttrNames(self):
      return [(None,u'label'),(None, u'scheme')]

class media_copyright(text):
  def getExpectedAttrNames(self):
      return [(None,u'url')]

class media_credit(text):
  def getExpectedAttrNames(self):
      return [(None, u'role'),(None,u'scheme')]

class media_hash(text):
  def getExpectedAttrNames(self):
    return [(None,u'algo')]

class media_rating(text):
  def getExpectedAttrNames(self):
    return [(None, u'scheme')]

class media_restriction(text):
  def getExpectedAttrNames(self):
    return [(None, u'relationship'),(None,u'type')]

class media_player(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,u'height'),(None,u'url'),(None, u'width')]

class media_text(text):
  def getExpectedAttrNames(self):
    return [(None,u'end'),(None,u'lang'),(None,u'start'),(None, u'type')]

class media_title(text):
  def getExpectedAttrNames(self):
    return [(None, u'type')]

class media_thumbnail(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,u'height'),(None,u'url'),(None,u'time'),(None, u'width')]

from extension import extension_everywhere
class media_content(validatorBase, media_elements, extension_everywhere):
  def getExpectedAttrNames(self):
    return [
        (None,u'bitrate'),
        (None,u'channels'),
        (None,u'duration'),
        (None,u'expression'),
        (None,u'fileSize'),
        (None,u'framerate'),
        (None,u'height'),
        (None,u'isDefault'),
        (None,u'lang'),
        (None,u'medium'),
        (None,u'samplingrate'),
        (None,u'type'),
        (None,u'url'),
        (None,u'width')
      ]

class media_group(validatorBase, media_elements):
  def do_media_content(self):
    return media_content()
