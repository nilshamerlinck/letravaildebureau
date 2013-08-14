#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# - Clic droit sur une image-frame Ajuster le cadre à l'image et vice versa

from from_images import *

if __name__ == '__main__':
    get_settings_from_document(False)
    scribus.zoomDocument(50)
    f = scribus.fileDialog("Select Image", "")
    add_image(f)
