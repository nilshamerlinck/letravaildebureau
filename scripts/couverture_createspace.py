#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Amazon CreateSpace
#
# Blue lines are bleed lines in this case !
#
# 1) lancer le script
# 2) ouvrir couverture-createspace.sla précédent
# 3) copier les éléments
# 4) aligner par rapport à la spine (en haut à droite toute : "aligner le côté gauche des objets à la droite de l'ancre") puis centrer les textes dans la frame
# 5) Disposition "de haut en bas" pour l'image pour voir le cadre "total"
# 6) remplacer couverture-createspace.sla
# 7) exporter en pdf, attention : format PDF/X (donc Couleurs : Imprimante)

import codecs, locale, os, sys
import traceback
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

from PIL import Image

try:
    import scribus
except ImportError:
    print "This script only runs from within Scribus."
    sys.exit(1)

TRAVAIL_DE_BUREAU = True

if TRAVAIL_DE_BUREAU:
    COVER_PHOTO = "/home/nils/travail/photos/batiment-de-nuit_-_8271988134.jpg"
    page_count = 166
    interior_width = 5
    interior_height = 8
else: # PARIS
    COVER_PHOTO = None
    page_count = 52
    interior_width = 8.5
    interior_height = 8.5

# https://www.createspace.com/Products/Book/CoverPDF.jsp
# white paper
#spine_ratio = 0.002252 # non-color books
spine_ratio = 0.002347 # color-books
spine_width = page_count * spine_ratio

bleed = 0.125
margin_out = 0.25
#margin_in = 0.75 # ça c'est vrai pour l'interior, mais pas pour la couverture !
margin_in = 0.25 # équilibrons

# Cover Width : Bleed + Back Cover Trim Size + Spine Width + Front Cover Trim Size + Bleed
cover_width = bleed + interior_width + spine_width + interior_width + bleed

# Cover Height : Bleed + Book Height Trim Size + Bleed
cover_height = bleed + interior_height + bleed

frame_width = interior_width - margin_out - margin_in
frame_height = interior_height - 2 * margin_out

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
    global interior_width, spine_width, interior_height, margin_out

    helperNewDocument(pageWidth=cover_width,
                      pageHeight=cover_height,
                      leftMargin=bleed,
                      topMargin=bleed,
                      rightMargin=bleed,
                      bottomMargin=bleed,
                      orientation=scribus.LANDSCAPE,
                      firstPageNumber=1,
                      unit=scribus.UNIT_INCHES,
                      pagesType=scribus.FACINGPAGES,
                      firstPageOrder=scribus.FIRSTPAGERIGHT,
                      numPages=1
                      )

create_document()

if COVER_PHOTO:
    frame = scribus.createImage(-0.4723, 0, 12.5788, 8.3681) # après essai, cf F2
    scribus.loadImage(COVER_PHOTO, frame)
    scribus.setScaleImageToFrame(scaletoframe=1, proportional=1, name=frame)

scribus.createText(0,
                   0,
                   cover_width,
                   cover_height,
                   "total")

# x, y, width, height
scribus.createText((bleed + margin_out),
                   (bleed + margin_out),
                   frame_width,
                   frame_height,
                   "back")
scribus.createText((bleed + interior_width),
                   0,
                   spine_width,
                   cover_height,
                   "spine")
scribus.createText((bleed + interior_width + spine_width + margin_in),
                   (bleed + margin_out),
                   frame_width,
                   frame_height,
                   "front")
