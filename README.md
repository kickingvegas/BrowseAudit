# BrowseAudit

A Python script to read your OS X Safari history file and list your most frequently visited websites. Output includes HTML, CSV, and listing to stdout.

## Quick Start Using Make

Run the following:

To generate a HTML file and open in Safari:

    $ make html

To generate a CSV file and open:

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
    
To generate a CSV file `index.html`:

    $ python browseaudit.py -C

To get help: 

    $ python browseaudit.py -h
    

## License

    Copyright 2013 Yummy Melon Software LLC

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Author: Charles Y. Choi <charles.choi@yummymelon.com>








