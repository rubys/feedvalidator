"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from validators import *
from logging import UndecipherableSpecification

class itunes:
  def do_itunes_explicit(self):
    return yesno(), noduplicates()

  def do_itunes_block(self):
    self.log(UndecipherableSpecification({"parent":self.name, "element":"itunes:block"}))
    return eater()

  def do_itunes_subtitle(self):
    return lengthLimitedText(255)

  def do_itunes_summary(self):
    return lengthLimitedText(4000)

  def do_itunes_image(self):
    self.log(UndecipherableSpecification({"parent":self.name, "element":"itunes:image"}))
    return eater()

  def do_itunes_author(self):
    return text()

  def do_itunes_category(self):
    return category()

class itunes_channel(itunes):
  def do_itunes_owner(self):
    return owner()

class itunes_item(itunes):
  def do_itunes_duration(self):
    return duration(), noduplicates()

  def do_itunes_keywords(self):
    return lengthLimitedText(255), keywords(), noduplicates()

class owner(validatorBase):
  def validate(self):
    if not "itunes_email" in self.children:
      self.log(MissingElement({"parent":self.name.replace("_",":"), 
        "element":"itunes:email"}))

  def do_itunes_email(self):
    return email(), noduplicates()

  def do_itunes_name(self):
    return text(), noduplicates()

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

class category(subcategory):
  def __init__(self):
    subcategory.__init__(self, valid_itunes_categories.keys())

  def do_itunes_category(self):
    if not self.text: return eater()
    return subcategory(valid_itunes_categories[self.text])
    
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
    "K-12",
    "Higher Education"],
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
  "Travel": []
}

__history__ = """
$Log$
Revision 1.3  2005/07/06 19:49:18  rubys
Remove unnecessary import

Revision 1.2  2005/07/06 19:35:28  rubys
Validate iTunes keywords

Revision 1.1  2005/07/01 23:55:30  rubys
Initial support for itunes

"""
