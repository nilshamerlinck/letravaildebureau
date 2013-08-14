#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FIXME: page_margins_right

import codecs, locale, os, sys
import traceback
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

try:
    import scribus
except ImportError:
    print "This script only runs from within Scribus."
    sys.exit(1)

import random

def insert_text_frame():
    page_size = scribus.getPageSize()

    page_margins_right = scribus.getPageMargins()
    page_margins_left = (page_margins_right[0], page_margins_right[2], page_margins_right[1], page_margins_right[3])

    if (scribus.currentPage() % 2) == 1:
        page_margins = page_margins_right
    else:
        page_margins = page_margins_left

    name = 'test%d' % random.randint(100, 999)

    # x, y, width, height
    scribus.createText(page_margins[0],
                       page_margins[1],
                       page_size[0] - (page_margins[0] + page_margins[2]),
                       page_size[1] - (page_margins[1] + page_margins[3]),
                       name)
    scribus.setText("test", name)

if __name__ == '__main__':
    if scribus.haveDoc():
        insert_text_frame()
