#!/usr/bin/env python
# Copyright (c) 2010 SubDownloader Developers - See COPYING - GPLv3

import sys, re

print re.sub('QtGui\.QApplication\.translate\(\".*?\",\s(.*),\sNone,\sQtGui\.QApplication\.UnicodeUTF8\)', r'_(\1)',sys.stdin.read())
