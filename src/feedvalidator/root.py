"""$Id$"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase

rss11_namespace='http://purl.org/net/rss1.1#'
purl1_namespace='http://purl.org/rss/1.0/'
soap_namespace='http://feeds.archive.org/validator/'
pie_namespace='http://purl.org/atom/ns#'
atom_namespace='http://www.w3.org/2005/Atom'
opensearch_namespace='http://a9.com/-/spec/opensearch/1.1/'

#
# Main document.  
# Supports rss, rdf, pie, and ffkar
#
class root(validatorBase):

  def __init__(self, parent, base):
    validatorBase.__init__(self)
    self.parent = parent
    self.dispatcher = parent
    self.name = "root"
    self.xmlBase = base
    self.xmlLang = None

  def startElementNS(self, name, qname, attrs):
    if name=='rss':
      if qname:
        from logging import InvalidNamespace
        self.log(InvalidNamespace({"parent":"root", "element":name, "namespace":qname}))
        validatorBase.defaultNamespaces.append(qname)

    if name=='feed' or name=='entry':
      if qname==pie_namespace:
        from logging import ObsoleteNamespace
        self.log(ObsoleteNamespace({"element":"feed"}))
        validatorBase.defaultNamespaces.append(pie_namespace)
        from logging import TYPE_ATOM
        self.setFeedType(TYPE_ATOM)
      elif not qname:
        from logging import MissingNamespace
        self.log(MissingNamespace({"parent":"root", "element":name}))
      else:
        if name=='feed':
          from logging import TYPE_ATOM
          self.setFeedType(TYPE_ATOM)
        else:
          from logging import TYPE_ATOM_ENTRY
          self.setFeedType(TYPE_ATOM_ENTRY)
        validatorBase.defaultNamespaces.append(atom_namespace)
        if qname<>atom_namespace:
          from logging import InvalidNamespace
          self.log(InvalidNamespace({"parent":"root", "element":name, "namespace":qname}))
          validatorBase.defaultNamespaces.append(qname)

    if name=='Channel':
      if not qname:
        from logging import MissingNamespace
        self.log(MissingNamespace({"parent":"root", "element":name}))
      elif qname != rss11_namespace :
        from logging import InvalidNamespace
        self.log(InvalidNamespace({"parent":"root", "element":name, "namespace":qname}))
      else:
        validatorBase.defaultNamespaces.append(qname)
        from logging import TYPE_RSS1
        self.setFeedType(TYPE_RSS1)

    if name=='OpenSearchDescription':
      if not qname:
        from logging import MissingNamespace
        self.log(MissingNamespace({"parent":"root", "element":name}))
        qname = opensearch_namespace
      elif qname != opensearch_namespace:
        from logging import InvalidNamespace
        self.log(InvalidNamespace({"element":name, "namespace":qname}))
        validatorBase.defaultNamespaces.append(qname)
        qname = opensearch_namespace

    validatorBase.startElementNS(self, name, qname, attrs)

  def unknown_starttag(self, name, qname, attrs):
    from logging import ObsoleteNamespace,InvalidNamespace,UndefinedElement
    if qname in ['http://example.com/newformat#','http://purl.org/atom/ns#']:
      self.log(ObsoleteNamespace({"element":name, "namespace":qname}))
    elif name=='feed':
      self.log(InvalidNamespace({"element":name, "namespace":qname}))
    else:
      self.log(UndefinedElement({"parent":"root", "element":name}))

    from validators import any
    return any(self, name, qname, attrs)

  def do_rss(self):
    from rss import rss
    return rss()

  def do_feed(self):
    from feed import feed
    if pie_namespace in validatorBase.defaultNamespaces:
      from validators import eater
      return eater()
    return feed()

  def do_entry(self):
    from entry import entry
    return entry()

  def do_opml(self):
    from opml import opml
    return opml()

  def do_outlineDocument(self):
    from logging import ObsoleteVersion
    self.log(ObsoleteVersion({"element":"outlineDocument"}))

    from opml import opml
    return opml()

  def do_opensearch_OpenSearchDescription(self):
    import opensearch
    validatorBase.defaultNamespaces.append(opensearch_namespace)
    return opensearch.OpenSearchDescription()

  def do_rdf_RDF(self):
    from rdf import rdf
    validatorBase.defaultNamespaces.append(purl1_namespace)
    return rdf()

  def do_Channel(self):
    from channel import rss10Channel
    return rss10Channel()

  def do_soap_Envelope(self):
    return root(self, self.xmlBase)

  def do_soap_Body(self):
    validatorBase.defaultNamespaces.append(soap_namespace)
    return root(self, self.xmlBase)

  def do_request(self):
    return root(self, self.xmlBase)

  def do_xhtml_html(self):
    from logging import UndefinedElement
    self.log(UndefinedElement({"parent":"root", "element":"xhtml:html"}))
    from validators import eater
    return eater()
