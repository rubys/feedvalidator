from validators import *

class media_elements:
  def do_media_adult(self):
    return media_truefalse(), noduplicates()
  def do_media_category(self):
    return media_category()
  def do_media_copyright(self):
    return media_copyright(), noduplicates()
  def do_media_credit(self):
    return media_credit()
  def do_media_description(self):
    return media_title(), noduplicates()
  def do_media_keywords(self):
    return text()
  def do_media_hash(self):
    return media_hash()
  def do_media_player(self):
    return media_player()
  def do_media_rating(self):
    return text(), noduplicates()
  def do_media_restriction(self):
    return media_restriction()
  def do_media_text(self):
    return media_text()
  def do_media_title(self):
    return media_title(), noduplicates()
  def do_media_thumbnail(self):
    return media_thumbnail()

class media_category(text):
  def getExpectedAttrNames(self):
      return [(None,u'label'),(None, u'scheme')]

class media_copyright(text,rfc2396_full):
  def getExpectedAttrNames(self):
      return [(None,u'url')]
  def prevalidate(self):
    self.name = "url"
    self.value = self.attrs.get((None,u'url'))
    if self.value: rfc2396_full.validate(self)

    self.name = "media_copyright"
    self.value = ""

class media_credit(text,rfc2396_full):
  EBU = [
    "actor", "adaptor", "anchor person", "animal trainer", "animator",
    "announcer", "armourer", "art director", "artist", "assistant camera",
    "assistant chief lighting technician", "assistant director",
    "assistant producer", "assistant visual editor", "author",
    "broadcast assistant", "broadcast journalist", "camera operator",
    "carpenter", "casting", "causeur", "chief lighting technician", "choir",
    "choreographer", "clapper loader", "commentary or commentator",
    "commissioning broadcaster", "composer", "computer programmer",
    "conductor", "consultant", "continuity checker", "correspondent",
    "costume designer", "dancer", "dialogue coach", "director",
    "director of photography", "distribution company", "draughtsman",
    "dresser", "dubber", "editor", "editor", "editor", "ensemble",
    "executive producer", "expert", "fight director", "floor manager",
    "focus puller", "foley artist", "foley editor", "foley mixer",
    "graphic assistant", "graphic designer", "greensman", "grip",
    "hairdresser", "illustrator", "interviewed guest", "interviewer",
    "key character", "key grip", "key talents", "leadman", "librettist",
    "lighting director", "lighting technician", "location manager",
    "lyricist", "make up artist", "manufacturer", "matte artist",
    "music arranger", "music group", "musician", "news reader", "orchestra",
    "participant", "photographer", "post", "producer", "production assistant",
    "production company", "production department", "production manager",
    "production secretary", "programme production researcher",
    "property manager", "publishing company", "puppeteer", "pyrotechnician",
    "reporter", "rigger", "runner", "scenario", "scenic operative",
    "script supervisor", "second assistant camera",
    "second assistant director", "second unit director", "set designer",
    "set dresser", "sign language", "singer", "sound designer", "sound mixer",
    "sound recordist", "special effects", "stunts", "subtitles",
    "technical director", "term", "translation", "transportation manager",
    "treatment ", "vision mixer", "visual editor", "visual effects",
    "wardrobe", "witness"]
  def getExpectedAttrNames(self):
    return [(None, u'role'),(None,u'scheme')]
  def prevalidate(self):
    scheme = self.attrs.get((None, 'scheme')) or 'urn:ebu'
    role = self.attrs.get((None, 'role'))

    if role:
      if scheme=='urn:ebu' and role not in self.EBU:
        self.log(InvalidCreditRole({"parent":self.parent.name, "element":self.name, "attr":"role", "value":role}))
      elif role != role.lower():
        self.log(InvalidCreditRole({"parent":self.parent.name, "element":self.name, "attr":"role", "value":role}))

    self.value = scheme
    self.name = "scheme"
    if scheme != 'urn:ebu': rfc2396_full.validate(self)

    self.name = "media_credit"
    self.value = ""

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

class media_text(nonhtml):
  def getExpectedAttrNames(self):
    return [(None,u'end'),(None,u'lang'),(None,u'start'),(None, u'type')]
  def prevalidate(self):
    self.type = self.attrs.get((None, 'type'))
    if self.type and self.type not in ['plain', 'html']:
      self.log(InvalidMediaTextType({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))

    start = self.attrs.get((None, 'start'))
    if start and not media_thumbnail.npt_re.match(start):
      self.log(InvalidNPTTime({"parent":self.parent.name, "element":self.name, "attr":"start", "value":start}))

    end = self.attrs.get((None, 'end'))
    if end and not media_thumbnail.npt_re.match(end):
      self.log(InvalidNPTTime({"parent":self.parent.name, "element":self.name, "attr":"end", "value":end}))

    lang = self.attrs.get((None, 'lang'))
    if lang: iso639_validate(self.log,lang,'lang',self.parent)

  def validate(self):
    if self.type == 'html':
      self.validateSafe(self.value)
    else:
      nonhtml.validate(self, ContainsUndeclaredHTML)

class media_title(nonhtml):
  def getExpectedAttrNames(self):
    return [(None, u'type')]
  def prevalidate(self):
    self.type = self.attrs.get((None, 'type'))
    if self.type and self.type not in ['plain', 'html']:
      self.log(InvalidMediaTextType({"parent":self.parent.name, "element":self.name, "attr":"type", "value":self.type}))
  def validate(self):
    if self.type == 'html':
      self.validateSafe(self.value)
    else:
      nonhtml.validate(self, ContainsUndeclaredHTML)

class media_thumbnail(validatorBase):
  npt_re = re.compile("^(now)|(\d+(\.\d+)?)|(\d+:\d\d:\d\d(\.\d+)?)$")
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
