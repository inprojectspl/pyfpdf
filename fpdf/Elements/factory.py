from .text import Text
from .box import Box
from .image import Image
from .barcode import Barcode
from .line import Line
from .link import Link


def factory_get_element(values):
    """
    'T': self.text, 'L': self.line, 'I': self.image,
    'B': self.rect, 'BC': self.barcode, 'W': self.write,
    :param values: a dictionary with all properties of each element.
                   Note that for images, fpdf can handle an image, but
                   the template system cannot, it always load a file from the a file.
    """
    if values["type"] == "T":
        return Text.init_from_dict(**values)
    if values["type"] == "W":
        return Link.init_from_dict(**values)
    if values["type"] == "B":
        return Box.init_from_dict(**values)

    if values["type"] == "I":
        return Image.init_from_dict(**values)
    if values["type"] == "BC":
        return Barcode.init_from_dict(**values)
    if values["type"] == "L":
        return Line.init_from_dict(**values)


