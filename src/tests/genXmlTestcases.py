#!/usr/bin/python
"""$Id$
Generate XML example files, valid and not, with a range of encodings."""

__author__ = "Joseph Walton <http://www.kafsemo.org/>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2004 Joseph Walton"
__license__ = "Python"

import os, sys

curdir = os.path.abspath(os.path.dirname(sys.argv[0]))
srcdir = os.path.split(curdir)[0]
if srcdir not in sys.path:
  sys.path.insert(0, srcdir)
basedir = os.path.split(srcdir)[0]

import codecs
import re

bom8='\xEF\xBB\xBF'
bom16BE='\xFE\xFF'
bom16LE='\xFF\xFE'
bom32BE='\x00\x00\xFE\xFF'
bom32LE='\xFF\xFE\x00\x00'

DIR=os.path.join(basedir, 'tmp')

written={}

def wtf(e, t, x, v=True):
  t.sort()
  if v: pfx = '/valid_'
  else: pfx  = '/invalid_'
  name = DIR + pfx + '_'.join([e] + t) + '.xml'
  assert not(name in written),"The file '" + name + "' has already been generated"
  open(name, 'w').write(x)
  written[name]=True

# Some fairly typical Unicode text. It should survive XML roundtripping.
docText=u'<x>\u201c"This\uFEFF" is\na\r\u00A3t\u20Acst\u201D</x>'

validDecl = re.compile('[A-Za-z][-A-Za-z0-9._]*')

def makeDecl(enc=None):
  if enc:
    assert validDecl.match(enc), "'" + enc + "' is not a valid encoding name"
    return "<?xml version='1.0' encoding='" + enc + "'?>"
  else:
    return "<?xml version='1.0'?>"

def encoded(enc, txt=docText):
  return codecs.getencoder(enc)(txt, 'xmlcharrefreplace')[0]

if __name__ == '__main__':
  if not(os.path.isdir(DIR)):
    os.mkdir(DIR)

  someFailed = False

  # Required

  wtf('UTF-8', ['BOM', 'declaration'],
    bom8 + makeDecl('UTF-8') + encoded('UTF-8'))

  wtf('UTF-8', [],
    encoded('UTF-8'))

  wtf('UTF-8', ['noenc'],
    makeDecl() + encoded('UTF-8'))

  wtf('UTF-8', ['declaration'],
    makeDecl('UTF-8') + encoded('UTF-8'))

  wtf('UTF-8', ['BOM'],
    bom8 + encoded('UTF-8'))

  wtf('UTF-8', ['BOM', 'noenc'],
    bom8 + makeDecl('UTF-8') + encoded('UTF-8'))

  wtf('UTF-16', ['BOM', 'declaration', 'BE'],
    bom16BE + encoded('UTF-16BE', makeDecl('UTF-16') + docText))

  wtf('UTF-16', ['BOM', 'declaration', 'LE'],
    bom16LE + encoded('UTF-16LE', makeDecl('UTF-16') + docText))

  wtf('UTF-16', ['BOM', 'BE'],
    bom16BE + encoded('UTF-16BE'))

  wtf('UTF-16', ['BOM', 'BE', 'noenc'],
    bom16BE + encoded('UTF-16BE', makeDecl() + docText))

  wtf('UTF-16', ['BOM', 'LE'],
    bom16LE + encoded('UTF-16LE'))

  wtf('UTF-16', ['BOM', 'LE', 'noenc'],
    bom16LE + encoded('UTF-16LE', makeDecl() + docText))

  wtf('UTF-16', ['declaration', 'BE'],
    encoded('UTF-16BE', makeDecl('UTF-16') + docText))

  wtf('UTF-16', ['declaration', 'LE'],
    encoded('UTF-16LE', makeDecl('UTF-16') + docText))


  # Standard wide encodings

  try:
    wtf('ISO-10646-UCS-2', ['BOM', 'declaration', 'BE'],
      bom16BE + encoded('UCS-2BE', makeDecl('ISO-10646-UCS-2') + docText))

    wtf('ISO-10646-UCS-2', ['BOM', 'declaration', 'LE'],
      bom16LE + encoded('UCS-2LE', makeDecl('ISO-10646-UCS-2') + docText))

    wtf('UTF-32', ['BOM', 'declaration', 'BE'],
      bom32BE + encoded('UTF-32BE', makeDecl('UTF-32') + docText))

    wtf('UTF-32', ['BOM', 'declaration', 'LE'],
      bom32LE + encoded('UTF-32LE', makeDecl('UTF-32') + docText))

    wtf('UTF-32', ['declaration', 'BE'],
      encoded('UTF-32BE', makeDecl('UTF-32') + docText))

    wtf('UTF-32', ['declaration', 'LE'],
      encoded('UTF-32LE', makeDecl('UTF-32') + docText))

    wtf('ISO-10646-UCS-4', ['BOM', 'declaration', 'BE'],
      bom32BE + encoded('UCS-4BE', makeDecl('ISO-10646-UCS-4') + docText))

    wtf('ISO-10646-UCS-4', ['BOM', 'declaration', 'LE'],
      bom32LE + encoded('UCS-4LE', makeDecl('ISO-10646-UCS-4') + docText))
  except LookupError, e:
    print e
    someFailed = True


  # Encodings that don't have BOMs, and require declarations
  withDeclarations = [
    # Common ASCII-compatible encodings
    'US-ASCII', 'ISO-8859-1', 'ISO-8859-15', 'WINDOWS-1252',

    # EBCDIC
    'IBM037', 'IBM038',

    # Encodings with explicit endianness
    'UTF-16BE', 'UTF-16LE',
    'UTF-32BE', 'UTF-32LE',
    # (UCS doesn't seem to define endian'd encodings)
  ]

  for enc in withDeclarations:
    try:
      wtf(enc, ['declaration'], encoded(enc, makeDecl(enc) + docText))
    except LookupError, e:
      print e
      someFailed = True


  # 10646-UCS encodings, with no BOM but with a declaration

  try:
    wtf('ISO-10646-UCS-2', ['declaration', 'BE'],
      encoded('UCS-2BE', makeDecl('ISO-10646-UCS-2') + docText))

    wtf('ISO-10646-UCS-2', ['declaration', 'LE'],
      encoded('UCS-2LE', makeDecl('ISO-10646-UCS-2') + docText))

    wtf('ISO-10646-UCS-4', ['declaration', 'BE'],
      encoded('UCS-4BE', makeDecl('ISO-10646-UCS-4') + docText))

    wtf('ISO-10646-UCS-4', ['declaration', 'LE'],
      bom32LE + encoded('UCS-4LE', makeDecl('ISO-10646-UCS-4') + docText))
  except LookupError, e:
    print e
    someFailed = True


  # Files with aliases for declarations. The declared alias should be
  #  reported back, rather than the canonical form.

  try:
    wtf('csUnicode', ['alias', 'BOM', 'BE'],
      bom16BE + encoded('UCS-2BE', makeDecl('csUnicode') + docText))

    wtf('csUnicode', ['alias', 'LE'],
      encoded('UCS-2LE', makeDecl('csUnicode') + docText))

    wtf('csucs4', ['alias', 'BE'],
      encoded('csucs4', makeDecl('csucs4') + docText))
  except LookupError, e:
    print e
    someFailed = True


  # Invalid files

  # UTF-32 with a non-four-byte declaration
  try:
    wtf('UTF-32', ['BOM', 'BE', 'declaration'],
      encoded('UTF-32', makeDecl('US-ASCII') + docText), False)
  except LookupError, e:
    print e
    someFailed = True

  # UTF-16 with a non-two-byte declaration
  wtf('UTF-16', ['BOM', 'BE', 'declaration'],
    encoded('UTF-16', makeDecl('UTF-8') + docText), False)

  # UTF-16BE, with a BOM
  wtf('UTF-16BE', ['BOM', 'declaration'],
    bom16BE + encoded('UTF-16BE', makeDecl('UTF-16BE') + docText), False)

  # UTF-8, with a BOM, declaring US-ASCII
  wtf('UTF-8', ['BOM', 'declaration'],
    bom8 + encoded('UTF-8', makeDecl('US-ASCII') + docText), False)

  try:
    # UTF-32, with a BOM, beginning without a declaration
    wtf('UTF-32', ['BOM', 'BE'],
      bom32BE + encoded('UTF-32BE'), False)

    # UTF-32, with a BOM, and a declaration with no encoding
    wtf('UTF-32', ['BOM', 'BE', 'noenc'],
      bom32BE + encoded('UTF-32BE', makeDecl() + docText), False)
  except LookupError, e:
    print e
    someFailed = True

  # UTF-16, no BOM, no declaration
  # wtf('UTF-16', ['BE'],
  #   encoded('UTF-16BE'), False)
  # This case falls through, and is identified as UTF-8; leave it out
  #  until we're doing decoding as well as detection.

  if someFailed:
    print "Unable to generate some tests; see README for details"

__history__ = """
$Log$
Revision 1.2  2004/03/30 16:44:30  josephw
If the 32-bit codecs are missing, only fail in detect() if there's an
attempt to use them. Make the test cases adapt to their absence, and point
the user to an explanatory README.

Revision 1.1  2004/03/30 08:11:45  josephw
Added a test for xmlEncoding. Made detect() log any problems.

"""
