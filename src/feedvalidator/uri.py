"""$Id$"""

# This is working code, with tests, but not yet integrated into validation.
# (Change unique in validators.py to use Uri(self.value), rather than the
#  plain value.)
# Ideally, this would be part of the core Python classes.
# It's probably not ready for deployment, but having it here helps establish
#  the test case as a repository for any pathological cases that people
#  suggest.

import urlparse
from urllib import quote, quote_plus, unquote, unquote_plus

from unicodedata import normalize
from codecs import lookup

(enc, dec) = lookup('UTF-8')[:2]

def _n(s):
  return enc(normalize('NFC', dec(s)[0]))[0]

def _qnu(s,plus=False):
  if plus:
    return quote_plus(_n(unquote_plus(s)))
  else:
    return quote(_n(unquote(s)))

def _normPort(netloc,port):
  a = netloc.rfind('@')
  if a >= 0:
    ui = netloc[:a]
    nl = netloc[a + 1:]
  else:
    ui = ''
  nl = netloc.lower()
  p = port
  i = nl.find(':')
  if i >= 0:
    ps = nl[i + 1:]
    if ps:
      if not(ps.isdigit()):
        return netloc
      p = int(ps)
    nl = nl[:i]
  if p != port:
    nl = nl + ':' + str(p)
  return ui + nl

def _norm(s):
  (scheme, netloc, path, query, fragment) = urlparse.urlsplit(s)

  scheme = scheme.lower()

#  netloc = netloc.lower()

  if scheme == 'http':
    netloc = _normPort(netloc, 80)
    if path == '':
      path = '/'
    path = _qnu(path)
    query = _qnu(query, True)
    fragment = _qnu(fragment)
  elif scheme == 'tag':
    # "Tags are simply strings of characters and are considered equal if and
    # only if they are completely indistinguishable in their machine
    # representations when using the same character encoding."
    pass
  elif scheme == 'ftp':
    netloc = _normPort(netloc, 21)
    if path == '':
      path = '/'
  elif scheme == 'mailto':
    # XXX From RFC 2368, mailto equivalence needs to be subtler than this
    i = path.find('@')
    if i > 0:
      j = path.find('?')
      if j < 0:
        j = len(path)

      path = _qnu(path[:i]) + '@' + _qnu(path[i + 1:].lower()) + _qnu(path[j:])
  else:
    pass

  return (scheme, netloc, path, query, fragment)

class Uri:
  """A Uri wraps a string and performs equality testing according to the
   rules for URI equivalence. """
  def __init__(self,s):
    self.s = s
    self.n = _norm(s)

  def __str__(self):
    return self.s

  def __repr__(self):
    return repr(self.s)

  def __eq__(self, a):
    return self.n == a.n

__history__ = """
$Log$
Revision 1.1  2004/11/28 17:34:16  josephw
Added URI class, with __eq__ method for equivalence testing.

"""
