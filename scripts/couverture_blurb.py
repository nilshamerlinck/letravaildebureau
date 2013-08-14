#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Calculs pour construire la couverture pour Blurb.com

import codecs, locale, os, sys
import traceback
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

fond_perdu = 0.317

def calculs(total_page_w, total_page_h, marge, marge_interieure):
    cadre_w = total_page_w - 4 * marge - marge_interieure
    cadre_w = cadre_w / 2
    cadre_h = total_page_h - 2 * marge
    x = cadre_w + 2 * marge
    
    print u"*Format de la page*"
    print u"Largeur : %f cm | Hauteur : %f cm" % (total_page_w, total_page_h)
    print u"Cadre texte: %f x %f cm" % (cadre_w, cadre_h)
    print u"Cadre texte marge intérieure situé à X: %f" % x

if True:
    total_page_w = 26.353
    total_page_h = 20.321
    marge = 0.635
    marge_interieure = 0.952
else:
    print u"En centimètres"
    print u"Regarder *Spécifications de la couverture*"
    total_page_w, total_page_h = raw_input("Total Taille de page ? (l x h) ").split(' x ')
    total_page_w = float(total_page_w)
    total_page_h = float(total_page_h)
    marge = float(raw_input(u"Marge ? "))
    marge_interieure = float(raw_input(u"Marge intérieure ? "))

calculs(total_page_w, total_page_h, marge, marge_interieure)
