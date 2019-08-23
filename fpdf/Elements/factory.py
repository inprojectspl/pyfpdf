import csv
import yaml
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
        return Text(**values)
    if values["type"] == "W":
        return Link(**values)
    if values["type"] == "B":
        return Box(**values)

    if values["type"] == "I":
        return Image(**values)
    if values["type"] == "BC":
        return Barcode(**values)
    if values["type"] == "L":
        return Line(**values)


def generate_elements(values: list):
    for element in values:
        yield factory_get_element(element)


def parse_csv(infile, delimiter=",", decimal_sep="."):
    """
    Parse template format csv file and create elements dict
    """
    keys = (
        'name', 'type', 'x1', 'y1', 'x2', 'y2', 'font', 'size',
        'bold', 'italic', 'underline', 'foreground', 'background',
        'align', 'text', 'priority', 'multiline', 'Boxable', 'Captionable'
    )
    # self.elements = []
    elements = {}
    with open(infile, encoding='utf-8') as f:
        for row in csv.reader(f, delimiter=delimiter):
            attributes = {}
            for i, ielement in enumerate(row):
                if not ielement.startswith("'") and decimal_sep != ".":
                    ielement = ielement.replace(decimal_sep, ".")
                    ielement = eval(ielement.strip())
                else:
                    ielement = str(ielement)
                if ielement == '':
                    ielement = None
                else:
                    try:
                        ielement = eval(ielement.encode().strip())
                    except SyntaxError as se:
                        print("Bad Encoding in ", infile,
                              "Please, check for binary strings with non latin characters")
                        raise SyntaxError
                attributes[keys[i]] = ielement
            elements[attributes['name']] = attributes
    return elements


def parse_yaml(infile):
    """
    Parse template format yaml file and create elements dict
    """
    with open(infile, encoding='utf-8') as f:
        text = f.read()
        yamlDict = yaml.safe_load(text)
        defs = yamlDict['Defaults'] if 'Defaults' in yamlDict else {}
        ret = {}
        for name, vals in yamlDict['Elements'].items():
            ret[name] = {**defs, **vals}

        return ret
