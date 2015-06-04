#!/usr/bin/env python
# Copyright (c) 2010 SubDownloader Developers - See COPYING - GPLv3

from __future__ import print_function
import sys, re

print(re.sub('QtGui\.QApplication\.translate\(\".*?\",\s(.*),\sNone,\sQtGui\.QApplication\.UnicodeUTF8\)', r'_(\1)',sys.stdin.read()))
