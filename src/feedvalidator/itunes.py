"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from validators import *

class itunes:
  def do_itunes_author(self):
    return lengthLimitedText(255), noduplicates()

  def do_itunes_block(self):
    return yesno(), noduplicates()

  def do_itunes_explicit(self):
    return yesno(), noduplicates()

  def do_itunes_keywords(self):
    return lengthLimitedText(255), keywords(), noduplicates()

  def do_itunes_subtitle(self):
    return lengthLimitedText(255), noduplicates()

  def do_itunes_summary(self):
    return lengthLimitedText(4000), noduplicates()

  def do_itunes_image(self):
    return image(), noduplicates()

class itunes_channel(itunes):
  from logging import MissingItunesElement

  def validate(self):
    if not 'language' in self.children and not self.xmlLang:
      self.log(MissingItunesElement({"parent":self.name, "element":'language'}))
    if not 'itunes_category' in self.children:
      self.log(MissingItunesElement({"parent":self.name, "element":'itunes:category'}))
    if not 'itunes_explicit' in self.children:
      self.log(MissingItunesElement({"parent":self.name, "element":'itunes:explicit'}))
    if not 'itunes_owner' in self.children:
      self.log(MissingItunesEmail({"parent":self.name, "element":'itunes:email'}))

  def setItunes(self, value):
    if value and not self.itunes:
      if self.dispatcher.encoding.lower() not in ['utf-8','utf8']:
        from logging import NotUTF8
        self.log(NotUTF8({"parent":self.parent.name, "element":self.name}))
      if self.getFeedType() == TYPE_ATOM and 'entry' in self.children:
        self.validate()
        
    self.itunes |= value

  def do_itunes_owner(self):
    return owner(), noduplicates()

  def do_itunes_category(self):
    return category()

  def do_itunes_pubDate(self):
    return rfc822(), noduplicates()

  def do_itunes_new_feed_url(self):
    if self.child != 'itunes_new-feed-url':
      self.log(UndefinedElement({"parent":self.name.replace("_",":"), "element":self.child}))
    return rfc2396_full(), noduplicates()

class itunes_item(itunes):
  supported_formats = ['m4a', 'mp3', 'mov', 'mp4', 'm4v', 'pdf']

  def validate(self):
    pass

  def setItunes(self, value):
    if value and not self.itunes: 
      self.parent.setItunes(True)
      self.itunes = value
      if hasattr(self, 'enclosures'):
        save, self.enclosures = self.enclosures, []
        for enclosure in save:
          self.setEnclosure(enclosure)

  def setEnclosure(self, url):
    if self.itunes:
      if url.split('.')[-1] not in itunes_item.supported_formats:
        from logging import UnsupportedItunesFormat
        self.log(UnsupportedItunesFormat({"parent":self.parent.name, "element":self.name, "extension":url.split('.')[-1]}))
      
    if not hasattr(self, 'enclosures'): self.enclosures = []
    self.enclosures.append(url)

  def do_itunes_duration(self):
    return duration(), noduplicates()

class owner(validatorBase):
  def validate(self):
    if not "itunes_email" in self.children:
      self.log(MissingElement({"parent":self.name.replace("_",":"), 
        "element":"itunes:email"}))

  def do_itunes_email(self):
    return email(), noduplicates()

  def do_itunes_name(self):
    return lengthLimitedText(255), noduplicates()

class subcategory(validatorBase):
  def __init__(self, list):
    validatorBase.__init__(self)
    self.list = list
    self.text = None

  def getExpectedAttrNames(self):
      return [(None, u'text')]

  def prevalidate(self):
    try:
      self.text=self.attrs.getValue((None, "text"))
      if not self.text in self.list:
        self.log(InvalidItunesCategory({"parent":self.parent.name.replace("_",":"), 
          "element":self.name.replace("_",":"), 
          "text":self.text}))
    except KeyError:
      self.log(MissingAttribute({"parent":self.parent.name.replace("_",":"), 
        "element":self.name.replace("_",":"), 
        "attr":"text"}))

class image(validatorBase, httpURLMixin):
  def getExpectedAttrNames(self):
    return [(None, u'href')]

  def prevalidate(self):
    try:
      self.validateHttpURL(None, 'href')
    except KeyError:
      self.log(MissingAttribute({"parent":self.parent.name, "element":self.name, "attr":'href'}))

    return validatorBase.prevalidate(self)

class category(subcategory):
  def __init__(self):
    subcategory.__init__(self, valid_itunes_categories.keys())

  def do_itunes_category(self):
    if not self.text: return eater()
    return subcategory(valid_itunes_categories.get(self.text,[]))
    
valid_itunes_categories = {
  "Arts & Entertainment": [
    "Architecture",
    "Books",
    "Design",
    "Entertainment",
    "Games",
    "Performing Arts",
    "Photography",
    "Poetry",
    "Science Fiction"],
  "Audio Blogs": [],
  "Business": [
    "Careers",
    "Finance",
    "Investing",
    "Management",
    "Marketing"],
  "Comedy": [],
  "Education": [
    "Higher Education",
    "K-12"],
  "Family": [],
  "Food": [],
  "Health": [
    "Diet & Nutrition",
    "Fitness",
    "Relationships",
    "Self-Help",
    "Sexuality"],
  "International": [
    "Australian",
    "Belgian",
    "Brazilian",
    "Canadian",
    "Chinese",
    "Dutch",
    "French",
    "German",
    "Hebrew",
    "Italian",
    "Japanese",
    "Norwegian",
    "Polish",
    "Portuguese",
    "Spanish",
    "Swedish"],
  "Movies & Television": [],
  "Music": [],
  "News": [],
  "Politics": [],
  "Public Radio": [],
  "Religion & Spirituality": [
    "Buddhism",
    "Christianity",
    "Islam",
    "Judaism",
    "New Age",
    "Philosophy",
    "Spirituality"],
  "Science": [],
  "Sports": [],
  "Talk Radio": [],
  "Technology": [
    "Computers",
    "Developers",
    "Gadgets",
    "Information Technology",
    "News",
    "Operating Systems",
    "Podcasting",
    "Smart Phones",
    "Text/Speech"],
  "Transportation": [
    "Automotive",
    "Aviation",
    "Bicycles",
    "Commuting"],
  "Travel": []
}

__history__ = """
$Log$
Revision 1.15  2006/02/28 21:39:56  rubys
Issue a warning on missing itunes email elements

Revision 1.14  2005/11/09 03:32:44  rubys
Verify enclosure against itunes formats

Revision 1.13  2005/11/08 18:27:42  rubys
Warn on missing language, itunes:explicit, or itunes:category if any itunes
elements are present.

Revision 1.12  2005/11/07 03:55:40  rubys
Add support for new-feed-url

Revision 1.11  2005/11/07 03:12:34  rubys
Itunes update:
http://lists.apple.com/archives/syndication-dev/2005/Nov/msg00002.html

Revision 1.10  2005/11/07 01:40:30  rubys
Updated categories

Revision 1.9  2005/07/29 14:51:36  philor
Update itunes:category values

Revision 1.8  2005/07/27 16:20:16  rubys
Support iTunes block as a Yes or No value.

Revision 1.7  2005/07/25 01:37:54  rubys
Nested invalid iTunes categories and cleanup

Revision 1.6  2005/07/19 17:32:07  rubys
Keywords is now legal at the channel level

Revision 1.5  2005/07/19 16:37:42  rubys
itunes:image/@url => itunes:image/href

Revision 1.4  2005/07/18 21:23:31  rubys
Itunes improvements

Revision 1.3  2005/07/06 19:49:18  rubys
Remove unnecessary import

Revision 1.2  2005/07/06 19:35:28  rubys
Validate iTunes keywords

Revision 1.1  2005/07/01 23:55:30  rubys
Initial support for itunes

"""
