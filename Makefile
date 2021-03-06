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

NUMITEMS=50

setup: publicsuffix.py

publicsuffix/publicsuffix.py:
	git submodule update --init

publicsuffix.py: publicsuffix/publicsuffix.py
	cp publicsuffix/publicsuffix.py .

run: publicsuffix.py
	python browseaudit.py -n ${NUMITEMS}

html: publicsuffix.py
	python browseaudit.py -n ${NUMITEMS} --html --no-stdout
	open index.html

csv: publicsuffix.py
	python browseaudit.py -n ${NUMITEMS} --csv --no-stdout
	open output.csv

help: publicsuffix.py
	python browseaudit.py -h

clean:
	find . -name index.html -delete
	find . -name output.csv -delete
	find . -name '*~' -delete
	find . -name '*.pyc' -delete

deepclean: clean
	- rm -f publicsuffix.py publicsuffix.txt
	- rm -rf publicsuffix

