#!/usr/bin/env python
#
# Copyright 2013 Yummy Melon Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
import urllib
try:
    from publicsuffix import PublicSuffixList
except ImportError:
    sys.stderr.write("ERROR: Please run 'make setup' to run browseaudit.\n")
    sys.exit(1)
    


usageString = '%s' % os.path.basename(sys.argv[0])
helpString = """
-h, --help                help
-v, --version             version
-n <n>, --number=<n>      return the top n sites visited
-C, --csv                 generate output.csv file 
-H, --html                generate index.html file
--no-stdout               suppress display on stdout 

"""

class BrowseAudit:
    def __init__(self):
        self.version = 1.0
        self.options = {}
        self.options['n'] = 50
        self.options['html'] = False
        self.options['csv'] = False
        self.options['stdout'] = True
        self.historyDict = None
        self.histogram = {}
        self.psl = None
        self.publicSuffixURL = 'http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1'
        
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

            elif o in ('-H', '--html'):
                self.options['html'] = True
                
            elif o in ('-C', '--csv'):
                self.options['csv'] = True

            elif o in ('--no-stdout',):
                self.options['stdout'] = False
                
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

        if not os.path.exists('publicsuffix.txt'):
            infile = urllib.urlopen(self.publicSuffixURL)
            with open('publicsuffix.txt', 'w') as outfile:
                outfile.write(infile.read())
            
        
        self.historyDict = plist['WebHistoryDates']

        for histObj in self.historyDict:
            try:
                urlObj = urlparse(histObj[''])
            except ValueError, e:
                sys.stderr.write('WARNING: {0}; Not counting url {1}\n'.format(e, histObj['']))
                continue
                
            domain = self.getDomain(urlObj)
            if domain is None:
                continue
            visitCount = histObj['visitCount']

            if domain in self.histogram:
                self.histogram[domain] += visitCount
            else:
                self.histogram[domain] = visitCount

        sortedHistogram = sorted(self.histogram.iteritems(), key = operator.itemgetter(1))
        n = self.options['n']
        if n < len(sortedHistogram):
            n = n * -1
            subsetList = sortedHistogram[n:]
        else:
            subsetList = sortedHistogram

        subsetList.reverse()

        
        if self.options['csv']:
            self.genCSV(subsetList)

        if self.options['html']:
            self.genHTML(subsetList)

        if self.options['stdout']:
            for key, value in subsetList:
                buf = '{0} {1}\n'.format(key.encode('utf-8'), value)
                sys.stdout.write(buf)


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

        p2 = SubElement(body, 'p')
        p2.text = u'BrowseAudit \xa9 2013 '
        a = SubElement(p2, 'a')
        a.text = 'Yummy Melon Software LLC'
        a.attrib = {'href' : 'http://www.yummymelon.com'}
        
        doc = ElementTree(html)

        with open('index.html', 'w') as outfile:
            doc.write(outfile)

            
    def getDomain(self, urlObj):
        if self.psl is None:
            self.psl = PublicSuffixList()
        
        domain = None
        if urlObj.scheme in ('https', 'http', 'ftp', 'sftp', 'mailto'):
            domain = self.psl.get_public_suffix(urlObj.netloc)

        elif urlObj.scheme in ('file',):
            domain = 'localhost'

        else:
            sys.stderr.write('WARNING: Not counting url {0}'.format(urlObj.geturl()))
            sys.stderr.write('\n')
            
        return domain
        
         
if __name__ == '__main__':

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hvn:CH',
                                      ('help',
                                       'version',
                                       'html',
                                       'csv',
                                       'no-stdout',
                                       'number='))
    except getopt.error, msg:
        sys.stderr.write(msg[0] + '\n')
        sys.stderr.write(usageString + '\n')
        sys.exit(1)

    
    app = BrowseAudit()
    app.run(optlist, args)

    
