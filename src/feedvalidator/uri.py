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
  if s == None:
    return None
  if plus:
    return quote_plus(_n(unquote_plus(s)), safe='=')
  else:
    return quote(_n(unquote(s)), safe='/~')

def _normPort(netloc,defPort):
  nl = netloc.lower()
  p = defPort
  i = nl.find(':')
  if i >= 0:
    ps = nl[i + 1:]
    if ps:
      if not(ps.isdigit()):
        return netloc
      p = int(ps)
    nl = nl[:i]
  if p != defPort:
    nl = nl + ':' + str(p)
  return nl

def _normAuth(auth,port):
  i = auth.rfind('@')
  if i >= 0:
    c = auth[:i]
    if c == ':':
      c = ''
    h = auth[i + 1:]
  else:
    c = None
    h = auth

  if c:
    return c + '@' + _normPort(h,port)
  else:
    return _normPort(h,port)

def _normPath(p):
  l = p.split('/')
  i = 0
  while i < len(l):
    c = l[i]
    if (c == '.'):
      del l[i]
    elif (c == '..'):
      del l[i]
      if i > 1:
        i -= 1
        del l[i]
    else:
      i += 1
  return '/'.join(l)

import re

# From RFC 2396bis, with added end-of-string marker
uriRe = re.compile('^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?$')

def _canonical(s):
  m = uriRe.match(s)
  if not(m):
    return None
  
  # Check for a relative URI
  if m.group(2) is None:
    scheme = None
  else:
    scheme = m.group(2).lower()

  if m.group(4) is None:
    authority = None

    if scheme == 'mailto':
      # XXX From RFC 2368, mailto equivalence needs to be subtler than this
      p = m.group(5)
      i = p.find('@')
      if i > 0:
        j = p.find('?')
        if j < 0:
          j = len(p)
        p = _qnu(p[:i]) + '@' + _qnu(p[i + 1:].lower()) + _qnu(p[j:])
      path = p
    else:
      path = _qnu(m.group(5))
  else:
    a = m.group(4)
    p = m.group(5)
    if scheme in ['http', 'ftp']:
      if scheme == 'http':
        a = _normAuth(a, 80)
      elif scheme == 'ftp':
        a = _normAuth(a, 21)

      if p == '':
        p = '/'
      else:
        p = _normPath(p)

      authority = a
      path = _qnu(p)

  query = _qnu(m.group(7), True)
  fragment = _qnu(m.group(9))

  s = ''
  if scheme != None:
    s += scheme + ':'

  if authority != None:
    s += '//' + authority

  s += path
  if query != None:
    s += '?' + query
  if fragment != None:
    s += '#' + fragment
  return s

class Uri:
  """A Uri wraps a string and performs equality testing according to the
   rules for URI equivalence. """
  def __init__(self,s):
    self.s = s
    self.n = _canonical(s)

  def __str__(self):
    return self.s

  def __repr__(self):
    return repr(self.s)

  def __eq__(self, a):
    return self.n == a.n

def canonicalForm(u):
  """Give the canonical form for a URI, so char-by-char comparisons become valid tests for equivalence."""
  try:
    return _canonical(u)
  except UnicodeError:
    return None

__history__ = """
$Log$
Revision 1.2  2005/01/18 23:26:00  josephw
Rewrite normalisation to deal with examples from PaceCanonicalIds.

Revision 1.1  2004/11/28 17:34:16  josephw
Added URI class, with __eq__ method for equivalence testing.

"""
