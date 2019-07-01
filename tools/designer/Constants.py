__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2011 Mariano Reingart"
__license__ = "GPL 3.0"
__version__ = "1.01e"


PAPER_SIZES = ['A4', 'Letter', 'Legal']
PAPER_ORIENTATIONS = ['Portrait', 'Landscape']
DEFAULT_PAPER_ORIENTATION = 'P'
DEFAULT_PAPER_SIZE = 'Letter'
PAPER_SIZE_OPTIONS = dict([
        ('Legal_portrait', (216, 356)),
        ('A4_portrait', (210, 297)),
        ('Letter_portrait', (216, 279)),
        ('Legal_landscape', (356, 216)),
        ('A4_landscape', (297, 210)),
        ('Letter_landscape', (279, 216))
    ])
