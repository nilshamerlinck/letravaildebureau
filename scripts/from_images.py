#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Inspired by http://wiki.scribus.net/canvas/Making_a_photobook_from_a_directory_of_images_using_a_script
# http://wiki.scribus.net/canvas/Category:Scripts
# Scripter-NG en route !

"""
(x, y) = scribus.getPosition(frame)
(w, h) = scribus.getSize(frame)
"""

import codecs, locale, os, sys
import traceback
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

from glob import glob
from PIL import Image

try:
    import scribus
except ImportError:
    print "This script only runs from within Scribus."
    sys.exit(1)

def get_page_margins():
    if (scribus.currentPage() % 2) == 1:
        return page_margins_right;
    else:
        return page_margins_left;

"""
si besoin :
topts = scribus.pt / scribus.mm
"""

min_ppi = 150.0

def calc_max():
    global page_size, page_margins_right, max_width, max_width_px, max_height, max_height_px

    # 1 inch = 25.4 mm
    max_width = (page_size[0] - (page_margins_right[1] + page_margins_right[2]))
    max_width_px = (max_width / 25.4) * min_ppi
    max_height = (page_size[1] - (page_margins_right[0] + page_margins_right[3]))
    max_height_px = (max_height / 25.4) * min_ppi

# helper
def helperNewDocument(pageWidth,
                      pageHeight,
                      leftMargin,
                      topMargin,
                      rightMargin,
                      bottomMargin,
                      orientation,
                      firstPageNumber,
                      unit,
                      pagesType,
                      firstPageOrder,
                      numPages):

    # size (height, width)
    # margins (left, top, right, bottom)
    return scribus.newDocument((pageHeight, pageWidth),
                               (leftMargin, topMargin, rightMargin, bottomMargin),
                               orientation,
                               firstPageNumber,
                               unit,
                               pagesType,
                               firstPageOrder,
                               numPages)

def create_document():
    global page_size, page_margins_right, page_margins_left

    # Default constants in mm

    page_size = (279.4, 215.9)
    
    # getPageMargins renvoit (top, left, right, bottom) mais
    # newDocument prend (left, top, right, bottom) !
    page_margins_left = (5, 5, 20, 5)
    page_margins_right = (5, 20, 5, 5)

    calc_max()

    helperNewDocument(pageWidth=page_size[0],
                      pageHeight=page_size[1],
                      leftMargin=page_margins_right[1],
                      topMargin=page_margins_right[0],
                      rightMargin=page_margins_right[2],
                      bottomMargin=page_margins_right[3],
                      orientation=scribus.LANDSCAPE,
                      firstPageNumber=1,
                      unit=scribus.UNIT_MILLIMETERS,
                      pagesType=scribus.FACINGPAGES,
                      firstPageOrder=scribus.FIRSTPAGERIGHT,
                      numPages=1
                      )

def get_settings_from_document(ignore_margins=True):
    scribus.setUnit(scribus.UNIT_MILLIMETERS)

    global page_size, page_margins_right, page_margins_left

    page_size = scribus.getPageSize()

    if ignore_margins:
        page_margins_right = (0, 0, 0, 0)
    else:
        page_margins_right = scribus.getPageMargins()

    page_margins_left = (page_margins_right[0], page_margins_right[2], page_margins_right[1], page_margins_right[3])

    calc_max()

def add_image(f):
    global page_size, page_margins_right, max_width, max_width_px, max_height, max_height_px

    try:
        im = Image.open(f)
    except:
        return False

    scribus.messagebarText("Adding " + f)
    
    ##
    # determine best frame width
    ##

    w, h = im.size

    print 'image: %s x %s px' % (w, h)
    
    # find the scale coeff
    coeff = 1
    
    # FIXME: cas où image aussi large que haute mais page en portrait
    
    if w > h:
        # scale on width
        if w >= max_width_px:
            coeff = max_width_px / w
    else:
        # scale on height
        if h >= max_height_px:
            coeff = max_height_px / h

    print 'coeff:', coeff

    # scaling and conversion to mm
    frameW = int(((coeff * w) / min_ppi) * 25.4)
    frameH = int(((coeff * h) / min_ppi) * 25.4)

    print 'frame: %s x %s mm' % (frameW, frameH)      

    # center frame
    frameX = get_page_margins()[1] + (max_width - frameW) / 2
    frameY = get_page_margins()[0] + (max_height - frameH) / 2

    frame = scribus.createImage(frameX, frameY, frameW, frameH)
    scribus.loadImage(f, frame)
    scribus.setScaleImageToFrame(scaletoframe=1, proportional=1, name=frame)

    return True

def create_content():
    dirname = scribus.fileDialog("Select Directory", "", "", False, False, True)
    files = sorted(glob(os.path.join(dirname, "*")))
    if len(files) == 0:
        return

    scribus.progressReset()
    scribus.progressTotal(len(files))
    scribus.messagebarText("Creating pages...")
    progress = 0;

    for f in files:

        scribus.progressSet(progress)
        progress = progress + 1

        add_image(f)

        if len(files) > progress:
            # add page for next image
            scribus.newPage(-1)
        
    scribus.progressReset()
    scribus.messagebarText("");
    scribus.deselectAll()
    scribus.gotoPage(1)        

if __name__ == '__main__':
    if scribus.haveDoc():
        get_settings_from_document()
    else:
        create_document()

    scribus.zoomDocument(50)

    create_content()
