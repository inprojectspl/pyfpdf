# -*- coding: utf-8 -*-

import re
import struct
import zlib
from six import BytesIO

import numpy
from PIL import Image
import urllib.request

from .errors import fpdf_error
from .php import substr
from .py3k import PY3K, b
from .util import freadint as read_integer

def load_resource(filename, reason = "image"):
    "Load external file"
    # by default loading from network is allowed for all images

    if reason == "image":
        if filename.startswith("http://") or \
           filename.startswith("https://"):
            with urllib.request.urlopen(filename) as f:
                f = BytesIO(f.read())
        else:
            fl = open(filename, "rb")
            f = BytesIO(fl.read())
            fl.close()
        return f
    else:
        fpdf_error("Unknown resource loading reason \"%s\"" % reason)


def parse_PIL(img):
    if img.mode not in ['L', 'LA', 'RGBA']:
        img = img.convert('RGBA')
    w, h = img.size
    info = {
        'w': w,
        'h': h,
    }
    pal = ''
    trns = ''
    if img.mode == 'L':
        dpn = 1
        bpc = 8
        colspace = 'DeviceGray'
        data = numpy.asarray(img)
        z_data = numpy.insert(data, 0, 0, axis=1)
        info['data'] = zlib.compress(z_data)
    elif img.mode == 'LA':
        dpn = 1
        bpc = 8
        colspace = 'DeviceGray'

        rgba_data = numpy.reshape(numpy.asarray(img), w * h * 2)
        a_data = numpy.ascontiguousarray(rgba_data[1::2])
        rgb_data = numpy.ascontiguousarray(rgba_data[0::2])

        a_data = numpy.reshape(a_data, (h, w))
        rgb_data = numpy.reshape(rgb_data, (h, w))

        za_data = numpy.insert(a_data.reshape((h, w)), 0, 0, axis=1)
        zrgb_data = numpy.insert(rgb_data.reshape((h, w)), 0, 0, axis=1)
        info['data'] = zlib.compress(zrgb_data)
        info['smask'] = zlib.compress(za_data)
    elif img.mode == 'RGBA':
        dpn = 3
        bpc = 8
        colspace = 'DeviceRGB'

        rgba_data = numpy.reshape(numpy.asarray(img), w * h * 4)
        a_data = numpy.ascontiguousarray(rgba_data[3::4])
        rgb_data = numpy.delete(rgba_data, numpy.arange(3, len(rgba_data), 4))

        a_data = numpy.reshape(a_data, (h, w))
        rgb_data = numpy.reshape(rgb_data, (h, w * 3))

        za_data = numpy.insert(a_data.reshape((h, w)), 0, 0, axis=1)
        zrgb_data = numpy.insert(rgb_data.reshape((h, w * 3)), 0, 0, axis=1)
        info['data'] = zlib.compress(zrgb_data)
        info['smask'] = zlib.compress(za_data)
    else:
        raise ValueError('Unsupport image: {}'.format(img.mode))

    dp = '/Predictor 15 /Colors ' + str(dpn)
    dp = dp + ' /BitsPerComponent ' + str(bpc)
    dp = dp + ' /Columns ' + str(w) + ''

    info.update({
        'cs': colspace,
        'bpc': bpc,
        'f': 'FlateDecode',
        'dp': dp,
        'pal': pal,
        'trns': trns
    })
    return info


def get_img_info(file_):
    img = Image.open(file_)
    return parse_PIL(img)


def is_Instanse_of_PIL(blob):
    return isinstance(blob, Image.Image)
