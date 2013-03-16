#!/usr/bin/env python
# Copyright 2013 Yummy Melon Software
# Author: Charles Y. Choi

import os
import sys
import getopt
import subprocess
import shutil
import plistlib
import json
from urlparse import urlparse
import operator
import tempfile
from xml.etree.ElementTree import ElementTree, Element, SubElement
from datetime import datetime

usageString = '%s ...' % os.path.basename(sys.argv[0])
helpString = """
-h, --help                help
-v, --version             version
-n <n>, --number=<n>      return the top n sites visited

"""

class Application:
    def __init__(self):
        self.version = 1.0
        self.options = {}
        self.options['n'] = -50
        self.historyDict = None
        self.histogram = {}
        
    def run(self, optlist, args):
        sys.stdout.write('# BrowseAudit\n')

        for o, i in optlist:
            if o in ('-h', '--help'):
                sys.stderr.write(usageString)
                sys.stderr.write(helpString)
                sys.exit(1)

            elif o in ('-v', '--version'):
                sys.stdout.write('%s\n' % str(self.version))
                sys.exit(0)
                
            elif o in ('-n', '--number'):
                try:
                    n = int(i)
                    self.options['n'] = n
                except:
                    sys.stderr.write('ERROR: n must be integer.\n')
                    sys.exit(1)

        if len(args) < 1:
            infile = tempfile.NamedTemporaryFile(delete=False)
            infile.close()

            cmdList = ['/usr/bin/plutil', '-convert', 'xml1', '-o', infile.name,
                   os.path.join(os.environ['HOME'], 'Library', 'Safari', 'History.plist')]

            subprocess.call(cmdList)
            plist = plistlib.readPlist(infile.name)
            os.unlink(infile.name)

        else:
            plist = plistlib.readPlist(args[0])
        
        self.historyDict = plist['WebHistoryDates']

        for histObj in self.historyDict:
            urlObj = urlparse(histObj[''])
            domain = self.getDomain(urlObj.netloc)

            if domain in self.histogram:
                self.histogram[domain] += 1
            else:
                self.histogram[domain] = 1

        sortedHistogram = sorted(self.histogram.iteritems(), key = operator.itemgetter(1))
        n = self.options['n']
        print len(sortedHistogram)
        if n < len(sortedHistogram):
            n = n * -1
            subsetList = sortedHistogram[n:]
        else:
            subsetList = sortedHistogram

        subsetList.reverse()

        self.genCSV(subsetList)
        self.genHTML(subsetList)


    def genCSV(self, resultList):
        with open('output.csv', 'w') as outfile:
            for key, value in resultList:
                buf = '{0},{1}\n'.format(key.encode('utf-8'), value)
                outfile.write(buf)

    def genHTML(self, resultList):
        html = Element('html')
        head = SubElement(html, 'head')
        style = SubElement(head, 'link')
        style.attrib = {'rel': 'stylesheet',
                        'href': 'js/main.css',
                        'type': 'text/css'}
        body = SubElement(html, 'body')

        h1 = SubElement(body, 'h1')
        h1.text = 'BrowseAudit'

        timeStamp = datetime.now()
        
        p = SubElement(body, 'p')
        p.text = 'Generated: {0}'.format(timeStamp.strftime('%Y-%m-%d %H:%M:%S %Z'))
        
        table = SubElement(body, 'table')
        tbody = SubElement(table, 'tbody')
        
        tr = SubElement(tbody, 'tr')
        th0 = SubElement(tr, 'th')
        th0.text = 'Rank'
        th1 = SubElement(tr, 'th')
        th1.text = 'Domain'
        th2 = SubElement(tr, 'th')
        th2.text = 'Visits'
        
        counter = 1
        for key, value in resultList:
            tr = SubElement(tbody, 'tr')
            td0 = SubElement(tr, 'td')
            td0.text = '{0}'.format(counter)
            td0.attrib = {'align' : 'center'}
            td1 = SubElement(tr, 'td')
            td1.text = key.encode('utf-8')
            td2 = SubElement(tr, 'td')
            td2.text = '{0}'.format(value)
            td2.attrib = {'align' : 'center'}
            counter += 1
            
        doc = ElementTree(html)

        with open('index.html', 'w') as outfile:
            doc.write(outfile)

            
    def getDomain(self, netloc):
        domain = netloc
        tempList = netloc.split('.')
        if len(tempList) >= 3:
            domain = '.'.join(tempList[-2:])

        return domain
        
         
if __name__ == '__main__':

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hvn:',
                                      ('help',
                                       'version',
                                       'number='))
    except getopt.error, msg:
        sys.stderr.write(msg[0] + '\n')
        sys.stderr.write(usageString + '\n')
        sys.exit(1)

    
    app = Application()
    app.run(optlist, args)

    
