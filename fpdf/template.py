# -*- coding: iso-8859-1 -*-

"""PDF Template Helper for FPDF.py"""

from __future__ import with_statement

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010 Mariano Reingart"
__license__ = "LGPL 3.0"

from .fpdf import FPDF
from .py3k import PY3K, unicode
from .Elements.factory import parse_csv, parse_yaml, generate_elements


def rgb(col):
    return (col // 65536), (col // 256 % 256), (col % 256)


class Template:
    def __init__(self, infile=None, elements=None, defaults=None,
                 paperformat='A4', orientation='portrait',
                 title='', author='', subject='', creator='', keywords=''):
        if elements:
            self.load_elements(elements)
        pdf = self.pdf = FPDF(format=paperformat,
                              orientation=orientation, unit="mm")
        pdf.set_title(title)
        pdf.set_author(author)
        pdf.set_creator(creator)
        pdf.set_subject(subject)
        pdf.set_keywords(keywords)
        self.pg_no = 0
        self.pages = []
        self.templates = {}
        self.defaults = defaults

    def load_elements(self, elements):
        """Initialize the internal element structures"""
        self.pg_no = 0
        self.templates[id(elements)] = elements

    def parse_csv(self, infile, delimiter=",", decimal_sep="."):
        self.pg_no = 0
        self.templates[infile] = parse_csv(infile, delimiter=delimiter, decimal_sep=decimal_sep)

    def parse_YML(self, infile):
        self.pg_no = 0
        elements = parse_yaml(infile)
        self.templates[infile] = elements

    def add_page(self, templatename=None):
        if len(self.templates) == 0:
            raise AttributeError("You must add templates first.")
        if not templatename:
            if len(self.templates) > 1:
                raise AttributeError("You have more than one template, specify the name")
            else:
                self.pages.append(self.firsttemplatename())
        else:
            if templatename not in self.templates:
                raise AttributeError("The template name doesn't exist in templates.")
            else:
                self.pages.append(templatename)
        self.pg_no += 1
        # self.texts[self.pg_no] = {}

    def __setitem__(self, name, value):
        """
        Setting the text value of the tuple name(template, name element) to value.
        For Backward compatibility: if you specified name as string it means you had only one template,
        and this function must be work as a dictionary to that only template.
        """
        nametemplate, nameelement = self.__getElementKeys(name)
        if not PY3K and isinstance(value, unicode):
            value = value.encode("latin1", "ignore")
        elif value is None:
            value = ""
        else:
            value = str(value)
        temp = self.templates[nametemplate]
        element = temp[nameelement]
        element['text'] = value
        # self.texts[self.pg_no][name.lower()] = value

    # setitem shortcut (may be further extended)
    set = __setitem__

    def has_key(self, name):
        """
        Iterate over the templates and his elements search check for coincidences.
        """
        for template in self.templates:
            if name.lower() in template:
                return True
        return False

    def __contains__(self, name):
        return name in self

    def __getitem__(self, name):
        """
        :return: Only the first coincidence of a element named as :name.
        TODO: should this return all the coincidences of elements named as :name=?
        """
        if not self.has_key(name):
            raise AttributeError("The element ", name, " doesn't exist.")
        nametemplate, nameelement = self.__getElementKeys(name)
        return self.templates[nametemplate][nameelement]['text']

    def split_multicell(self, text, element_name):
        """Divide (\n) a string using a given element width"""
        if not self.has_key(element_name):
            raise AttributeError("The element ", element_name, " doesn't exist.")

        pdf = self.pdf
        element = None
        for template in self.templates:
            if element_name.lower() in template:
                element = template[element_name.lower()]
                break

        style = ""
        if element['bold']:
            style += "B"
        if element['italic']:
            style += "I"
        if element['underline']:
            style += "U"
        pdf.set_font(element['font'], style, element['size'])
        align = {
            'L': 'L',
            'R': 'R',
            'I': 'L',
            'D': 'R',
            'C': 'C',
            'J': 'J',
            '': ''
        }.get(element['align'])  # D/I in spanish
        if isinstance(text, unicode) and not PY3K:
            text = text.encode("latin1", "ignore")
        else:
            text = str(text)
        return pdf.multi_cell(
            w=element['x2'] - element['x1'],
            h=element['y2'] - element['y1'],
            txt=text, align=align, split_only=True
        )

    def __generateFPDF__(self):
        for pg in range(self.pg_no):
            self.pdf.add_page()
            self.pdf.set_font('Arial', 'B', 16)
            self.pdf.set_auto_page_break(False, margin=0)
            templatename = self.pages[pg]
            template = self.templates[templatename]

            for element in generate_elements(sorted(template.values(), key=lambda x: x['priority'])):
                element.render(self.pdf)

    def render(self, outfile, fate="F"):
        self.__generateFPDF__()
        return self.pdf.output(outfile, fate)

    def getFPDF(self):
        self.__generateFPDF__()
        return self.pdf

    def firsttemplatename(self):
        if len(self.templates) == 0:
            raise IndexError("You must add first a template")
        return next(iter(self.templates))

    def __getElementKeys(self, name):
        if isinstance(name, tuple):  # more than one tuple
            nametemplate, nameelement = name
        if isinstance(name, str):
            nametemplate = self.firsttemplatename()
            nameelement = name
        return nametemplate, nameelement
