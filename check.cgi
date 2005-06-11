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

def applyTemplate(templateFile, params={}):
    params['CSSURL'] = CSSURL
    fsock = open(os.path.join(WEBDIR, 'templates', templateFile))
    data = fsock.read() % params
    fsock.close()
    return data

def sanitizeURL(url):
    scheme, domain, path, u1, u2, u3 = urlparse.urlparse(url)
    if scheme.lower() <> 'http':
        url = 'http://%s' % url
        scheme, domain, path, u1, u2, u3 = urlparse.urlparse(url)
    url = url.strip()

    # strip user and password
    url = re.sub(r'^(\w*://)[-+.\w]*(:[-+.\w]+)?@', r'\1' ,url)

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
    return applyTemplate('code_listing.tmpl', {"codelisting":codelisting, "url":url})

def printEventList(output):
  print output.header()
  for o in output:
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

if (method == 'get') or (contentType and cgi.parse_header(contentType)[0].lower() == 'application/x-www-form-urlencoded'):
    fs = cgi.FieldStorage()
    url = fs.getvalue("url") or ''
    manual = fs.getvalue("manual") or 0
    rawdata = fs.getvalue("rawdata") or ''

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

if (method == 'post') and (not rawdata):
    # SOAP
    try:
        # validate
        params = feedvalidator.validateStream(sys.stdin, contentType=contentType)
        events = params['loggedEvents']
        feedType = params['feedType']

        # filter based on compatibility level
        from feedvalidator import compatibility
        filterFunc = compatibility.AA # hardcoded for now
        events = filterFunc(events)

        # format as xml
        from feedvalidator.formatter.text_xml import Formatter
        output = Formatter(events)

        # output
        if output:
            body = applyTemplate('soap.tmpl', {'body':"\n".join(output)})
        else:
            body = applyTemplate('soap.tmpl' , {'body':''})
        print 'Content-type: text/xml; charset=' + ENCODING + '\r\n\r\n' + body

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
                print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % cgi.escape(url)})
                print applyTemplate('manual.tmpl', {'rawdata':cgi.escape(url)})
                output = Formatter([vfv.event], None)
                printEventList(output)
                print applyTemplate('error.tmpl')
            except:
                print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % cgi.escape(url)})
                print applyTemplate('manual.tmpl', {'rawdata':cgi.escape(url)})
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
                print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % cgi.escape(url)})
                print applyTemplate('index.tmpl', {'value':cgi.escape(url)})
                output = Formatter([vfv.event], None)
                printEventList(output)
                print applyTemplate('error.tmpl')
            except:
                print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % cgi.escape(url)})
                print applyTemplate('index.tmpl', {'value':cgi.escape(url)})
                print applyTemplate('error.tmpl')
        if goon:
            # post-validate (will do RSS autodiscovery if needed)
            validationData = postvalidate(url, events, rawdata, feedType)
   
            # write output header
            url = validationData['url']
            feedType = validationData['feedType']
            rawdata = validationData['rawdata']
            print applyTemplate('header.tmpl', {'title':'Feed Validator Results: %s' % cgi.escape(url)})
            if manual:
                print applyTemplate('manual.tmpl', {'rawdata':cgi.escape(rawdata)})
            else:
                print applyTemplate('index.tmpl', {'value':cgi.escape(url)})
    
            output = validationData.get('output', None)

            # print special case, if any
            specialCase = validationData.get('specialCase', None)
            if specialCase:
                print applyTemplate('%s.tmpl' % specialCase)

            msc = output.mostSeriousClass()

            # Explain the overall verdict
            if msc == Error:
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
                htmlUrl = cgi.escape(urllib.quote(url, '/:'))
                print applyTemplate('valid.tmpl', {"url":htmlUrl, "srcUrl":cgi.escape(htmlUrl), "feedType":FEEDTYPEDISPLAY[feedType], "graphic":VALIDFEEDGRAPHIC[feedType], "HOMEURL":HOMEURL})
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
