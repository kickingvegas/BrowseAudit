# BrowseAudit

A Python script to read your OS X Safari history file and privately list your most frequently visited website domains. Output includes HTML, CSV, and listing to stdout.

Surprise yourself today. 

## Installation

In a command line, please run the following:

    $ git clone git@github.com:kickingvegas/BrowseAudit.git
    
Note that *BrowseAudit* uses the 3rd party Python module [`publicsuffix`](https://pypi.python.org/pypi/publicsuffix/) as a `git submodule`. Please disregard any GitHub generated `tar.gz` or `zip` buttons as the `publicsuffix` submodule source will not be included in them.

## Quick Start Using Make

Run the following:

To generate a HTML file `index.html` and open via Finder:

    $ make html

To generate a CSV file `output.csv` and open via Finder:

    $ make csv
    
To display results on `stdout`:

    $ make 
    
To get help:

    $ make help


## Operation by Example

The basic operation of BrowseAudit is:

    $ python browseaudit.py 
    
To generate a HTML file `index.html`:

    $ python browseaudit.py -H
    
To generate a CSV file `output.csv`:

    $ python browseaudit.py -C

To get help: 

    $ python browseaudit.py -h


## Recent Changes

* Changed to use public suffix lookup 
    
## Licenses

### BrowseAudit 

Copyright &copy; 2013 Yummy Melon Software LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Charles Y. Choi <charles.choi@yummymelon.com>


### Public Suffix

Copyright (c) 2011 Toma&#158; &#138;olc <tomaz.solc@tablix.org>

Python module included in this distribution is based on the code downloaded
from [http://code.google.com/p/python-public-suffix-list/](http://code.google.com/p/python-public-suffix-list/), which is
available under the following license:

Copyright (c) 2009 David Wilson

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

The Public Suffix List included in this distribution has been downloaded
from [http://publicsuffix.org/](http://publicsuffix.org/) and is covered by a separate license. Please
see the license block at the top of the file itself.







