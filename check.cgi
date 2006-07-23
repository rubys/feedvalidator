#!/usr/bin/env python
from config import *

import cgi, sys, os, urlparse, sys, re, urllib
import cgitb
cgitb.enable()

import codecs
ENCODING='UTF-8'
sys.stdout = codecs.getwriter(ENCODING)(sys.stdout)

# Used for CGI parameters
decUTF8 = codecs.getdecoder('utf-8')
decW1252 = codecs.getdecoder('windows-1252')

if PYDIR not in sys.path:
    sys.path.insert(0, PYDIR)

if WEBDIR not in sys.path:
    sys.path.insert(0, WEBDIR)

if SRCDIR not in sys.path:
    sys.path.insert(0, SRCDIR)
import feedvalidator
from feedvalidator.logging import FEEDTYPEDISPLAY, VALIDFEEDGRAPHIC

from feedvalidator.logging import Info, Warning, Error, ValidationFailure
from feedvalidator.logging import TYPE_ATOM_ENTRY

def applyTemplate(templateFile, params={}):
    params['CSSURL'] = CSSURL
    fsock = open(os.path.join(WEBDIR, 'templates', templateFile))
    data = fsock.read() % params
    fsock.close()
    return data

def sanitizeURL(url):
    # Allow feed: URIs, as described by draft-obasanjo-feed-URI-scheme-02
    if url.lower().startswith('feed:'):
      url = url[5:]
      if url.startswith('//'):
        url = 'http:' + url

    if not url.split(':')[0].lower() in ['http','https']:
        url = 'http://%s' % url
    url = url.strip()

    # strip user and password
    url = re.sub(r'^(\w*://)[-+.\w]*(:[-+.\w]+)?@', r'\1' ,url)

    return url

def escapeURL(url):
    parts = list(urlparse.urlparse(url))
    safe = ['/', '/:@', '/', '/', '/?&=;', '/']
    for i in range(0,len(parts)):
      parts[i] = urllib.quote(urllib.unquote(parts[i]),safe[i])
    url = cgi.escape(urlparse.urlunparse(parts))
    try:
      return url.decode('idna')
    except:
      return url

import feedvalidator.formatter.text_html

def buildCodeListing(events, rawdata):
    # print feed
    codelines = []
    linenum = 1
    linesWithErrors = [e.params.get('line', 0) for e in events]
    for line in rawdata.split('\n'):
        line = feedvalidator.formatter.text_html.escapeAndMark(line)
        if not line: line = '&nbsp;'
        linetype = linenum in linesWithErrors and "b" or "a"
        codelines.append(applyTemplate('code_listing_line.tmpl', {"line":line, "linenum":linenum, "linetype":linetype}))
        linenum += 1
    codelisting = "".join(codelines)
    return applyTemplate('code_listing.tmpl', {"codelisting":codelisting, "url":escapeURL(url)})

def printEventList(output):
  errors, warnings = output.getErrors(), output.getWarnings()

  print output.header()
  for o in output.getErrors():
    print o
  if errors and warnings:
    print output.footer()
    if len(warnings) == 1:
      print applyTemplate('andwarn1.tmpl')
    else:
      print applyTemplate('andwarn2.tmpl')
    print output.header()
  for o in output.getWarnings():
    print o
  print output.footer()

from feedvalidator.formatter.text_html import Formatter

def postvalidate(url, events, rawdata, feedType, autofind=1):
    """returns dictionary including 'url', 'events', 'rawdata', 'output', 'specialCase', 'feedType'"""
    # filter based on compatibility level
    from feedvalidator import compatibility
    filterFunc = compatibility.AA # hardcoded for now
    events = filterFunc(events)

    specialCase = None
    formattedOutput = Formatter(events, rawdata)
    if formattedOutput:
        # check for special cases
        specialCase = compatibility.analyze(events, rawdata)
        if (specialCase == 'html') and autofind:
            try:
                try:
                    import feedfinder
                    class NotARobot:
                        base=url 
                        def get(self, url):
                            if url == self.base: return rawdata 
                            return urllib.urlopen(url).read()
                    feedfinder._gatekeeper = NotARobot()
                    rssurls = feedfinder.getFeeds(url)
                except:
                    rssurls = [url]
                if rssurls:
                    url = rssurls[0]
                    params = feedvalidator.validateURL(url, firstOccurrenceOnly=1, wantRawData=1)
                    events = params['loggedEvents']
                    rawdata = params['rawdata']
                    feedType = params['feedType']
                    return postvalidate(url, events, rawdata, feedType, autofind=0)
            except:
                pass

    return {"url":url, "events":events, "rawdata":rawdata, "output":formattedOutput, "specialCase":specialCase, "feedType":feedType}

method = os.environ['REQUEST_METHOD'].lower()
contentType = os.environ.get('CONTENT_TYPE', None)
output_option = ''

if (method == 'get') or (contentType and cgi.parse_header(contentType)[0].lower() == 'application/x-www-form-urlencoded'):
    fs = cgi.FieldStorage()
    url = fs.getvalue("url") or ''
    try:
      if url: url = url.decode('utf-8').encode('idna')
    except:
      pass
    manual = fs.getvalue("manual") or 0
    rawdata = fs.getvalue("rawdata") or ''
    output_option = fs.getvalue("output") or ''

    # XXX Should use 'charset'
    try:
        rawdata = decUTF8(rawdata)[0]
    except UnicodeError:
        rawdata = decW1252(rawdata)[0]

    rawdata = rawdata[:feedvalidator.MAXDATALENGTH].replace('\r\n', '\n').replace('\r', '\n')
else:
    url = None
    manual = None
    rawdata = None

if (output_option == "soap12"):
    # SOAP
    try:
        if ((method == 'post') and (not rawdata)): 
            params = feedvalidator.validateStream(sys.stdin, contentType=contentType)
        elif rawdata :
            params = feedvalidator.validateString(rawdata, firstOccurrenceOnly=1)
        elif url:
            url = sanitizeURL(url)
            params = feedvalidator.validateURL(url, firstOccurrenceOnly=1, wantRawData=1)
        
        events = params['loggedEvents']
        feedType = params['feedType']

        # filter based on compatibility level
        from feedvalidator import compatibility
        filterFunc = compatibility.AA # hardcoded for now
        events = filterFunc(events)

        events_error = list()
        events_warn = list()
        events_info = list()


        # format as xml
        from feedvalidator.formatter.text_xml import Formatter
        output = Formatter(events)

        for event in events:
            if isinstance(event,Error): events_error.append(output.format(event))
            if isinstance(event,Warning): events_warn.append(output.format(event))
            if isinstance(event,Info): events_info.append(output.format(event))
        if len(events_error) > 0:
            validation_bool = "false"
        else:
            validation_bool = "true"
          
        from datetime import datetime
        right_now = datetime.now()
        validationtime = str( right_now.isoformat())
        
        body = applyTemplate('soap.tmpl', {
          'errorlist':"\n".join( events_error), 'errorcount': str(len(events_error)), 
          'warninglist':"\n".join( events_warn), 'warningcount': str(len(events_warn)), 
          'infolist':"\n".join( events_info), 'infocount': str(len(events_info)),
          'home_url': HOMEURL, 'url': url, 'date_time': validationtime, 'validation_bool': validation_bool
          })        
        print 'Content-type: application/soap+xml; charset=' + ENCODING + '\r\n\r\n' + body
# this for easy debug
#        print 'Content-type: text/xml; charset=' + ENCODING + '\r\n\r\n' + body

    except:
        import traceback
        tb = ''.join(apply(traceback.format_exception, sys.exc_info()))

        from feedvalidator.formatter.text_xml import xmlEncode
        print 'Status: 500 Internal Error\r\nContent-type: text/xml; charset=' + ENCODING + '\r\n'
        print applyTemplate('fault.tmpl', {'code':sys.exc_info()[0],
          'string':sys.exc_info()[1], 'traceback':xmlEncode(tb)})

else: 
    print 'Content-type: text/html; charset=' + ENCODING
    print
    if url or rawdata:
        # validate
        goon = 0
        if rawdata:
            # validate raw data (from text form)
            try:
                params = feedvalidator.validateString(rawdata, firstOccurrenceOnly=1)
                events = params['loggedEvents']
                feedType = params['feedType']
                goon = 1
            except ValidationFailure, vfv:
                print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % escapeURL(url)})
                print applyTemplate('manual.tmpl', {'rawdata':escapeURL(url)})
                output = Formatter([vfv.event], None)
                printEventList(output)
                print applyTemplate('error.tmpl')
            except:
                print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % escapeURL(url)})
                print applyTemplate('manual.tmpl', {'rawdata':escapeURL(url)})
                print applyTemplate('error.tmpl')
        else:
            url = sanitizeURL(url)
            try:
                params = feedvalidator.validateURL(url, firstOccurrenceOnly=1, wantRawData=1)
                events = params['loggedEvents']
                rawdata = params['rawdata']
                feedType = params['feedType']
                goon = 1
            except ValidationFailure, vfv:
                print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % escapeURL(url)})
                print applyTemplate('index.tmpl', {'value':escapeURL(url)})
                output = Formatter([vfv.event], None)
                printEventList(output)
                print applyTemplate('error.tmpl')
            except:
                print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % escapeURL(url)})
                print applyTemplate('index.tmpl', {'value':escapeURL(url)})
                print applyTemplate('error.tmpl')
        if goon:
            # post-validate (will do RSS autodiscovery if needed)
            validationData = postvalidate(url, events, rawdata, feedType)
   
            # write output header
            url = validationData['url']
            feedType = validationData['feedType']
            rawdata = validationData['rawdata']
            print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % escapeURL(url)})
            if manual:
                print applyTemplate('manual.tmpl', {'rawdata':cgi.escape(rawdata)})
            else:
                print applyTemplate('index.tmpl', {'value':escapeURL(url)})
    
            output = validationData.get('output', None)

            # print special case, if any
            specialCase = validationData.get('specialCase', None)
            if specialCase:
                print applyTemplate('%s.tmpl' % specialCase)

            msc = output.mostSeriousClass()

            # Explain the overall verdict
            if msc == Error:
                from feedvalidator.logging import ObsoleteNamespace
                if len(output.getErrors())==1 and \
                    isinstance(output.data[0],ObsoleteNamespace):
                    print applyTemplate('notsupported.tmpl')
                else:
                    print applyTemplate('invalid.tmpl')
            elif msc == Warning:
                print applyTemplate('warning.tmpl')
            elif msc == Info:
                print applyTemplate('info.tmpl')

            # Print any issues, whether or not the overall feed is valid
            if output:
                printEventList(output)
    
                # print code listing
                print buildCodeListing(validationData['events'], validationData['rawdata'])

            # As long as there were no errors, show that the feed is valid
            if msc != Error:
                # valid
                htmlUrl = escapeURL(urllib.quote(url))
                try:
                  htmlUrl = htmlUrl.encode('idna')
                except:
                  pass
                print applyTemplate('valid.tmpl', {"url":htmlUrl, "srcUrl":htmlUrl, "feedType":FEEDTYPEDISPLAY[feedType], "graphic":VALIDFEEDGRAPHIC[feedType], "HOMEURL":HOMEURL, "docType":(feedType == TYPE_ATOM_ENTRY and 'entry' or 'feed')})
    else:
        # nothing to validate, just write basic form
        print applyTemplate('header.tmpl', {'title':'Feed Validator for Atom and RSS'})
        if manual:
            print applyTemplate('manual.tmpl', {'rawdata':''})
        else:
            print applyTemplate('index.tmpl', {'value':'http://'})
        print applyTemplate('special.tmpl', {})
    
    print applyTemplate('navbar.tmpl')
    print applyTemplate('footer.tmpl')
