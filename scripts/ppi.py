#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Print real size of printed image
# respecting the given PPI

import codecs, locale, os, sys
import traceback
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

from glob import glob
from PIL import Image

PPI = 150

for f in sys.argv[1:]:
    print f.decode('utf-8')

    try:
        im = Image.open(f)
    except:
        continue

    w, h = im.size
    print "%.1fx%.1fcm at %sppi" % ((w / PPI) * 2.54,
                                 (h / PPI) * 2.54,
                                 PPI)
