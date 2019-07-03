# -*- coding: iso-8859-1 -*-

"""PDF Template Helper for FPDF.py"""

from __future__ import with_statement

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010 Mariano Reingart"
__license__ = "LGPL 3.0"

import csv
from .fpdf import FPDF
from .py3k import PY3K, unicode
from PIL import Image


def rgb(col):
    return (col // 65536), (col // 256 % 256), (col % 256)


class Template:
    def __init__(self, infile=None, elements=None,
                 paperformat='A4', orientation='portrait',
                 title='', author='', subject='', creator='', keywords=''):
        if elements:
            self.load_elements(elements)
        self.handlers = {'T': self.text, 'L': self.line, 'I': self.image,
                         'B': self.rect, 'BC': self.barcode, 'W': self.write, }
        self.texts = {}
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

    def load_elements(self, elements):
        """Initialize the internal element structures"""
        self.pg_no = 0
        self.templates[id(elements)] = elements

    def parse_csv(self, infile, delimiter=",", decimal_sep="."):
        """Parse template format csv file and create elements dict"""
        keys = (
            'name', 'type', 'x1', 'y1', 'x2', 'y2', 'font', 'size',
            'bold', 'italic', 'underline', 'foreground', 'background',
            'align', 'text', 'priority', 'multiline'
        )
        # self.elements = []
        elements = {}
        self.pg_no = 0
        if not PY3K:
            f = open(infile, 'rb')
        else:
            f = open(infile, encoding='utf-8')
        with f:
            for row in csv.reader(f, delimiter=delimiter):
                kargs = {}
                for i, v in enumerate(row):
                    if not v.startswith("'") and decimal_sep != ".":
                        v = v.replace(decimal_sep, ".")
                        v = eval(v.strip())
                    else:
                        v = str(v)
                    if v == '':
                        v = None
                    else:
                        try:
                            v = eval(v.encode().strip())
                        except SyntaxError as se:
                            print("Bad Encoding in ", infile,
                                  "Please, check for binary strings with non latin characters")
                            raise SyntaxError
                    kargs[keys[i]] = v
                elements[kargs['name']] = kargs
        # self.keys = [v['name'].lower() for v in elements]
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
        elif isinstance(value, Image.Image):
            value = value  # Yes, I know :c
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

    def render(self, outfile, fate="F"):
        pdf = self.pdf
        for pg in range(self.pg_no):
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.set_auto_page_break(False, margin=0)
            templatename = self.pages[pg]
            template = self.templates[templatename]
            for element in sorted(template.values(), key=lambda x: x['priority']):
                if 'rotate' in element:
                    pdf.rotate(element['rotate'], element['x1'], element['y1'])
                self.handlers[element['type'].upper()](pdf, **element)
                if 'rotate' in element:
                    pdf.rotate(0)
        if fate:
            return pdf.output(outfile, fate)

    def text(self, pdf, x1=0, y1=0, x2=0, y2=0, text='', font="arial", size=10,
             bold=False, italic=False, underline=False, align="",
             foreground=0, backgroud=65535, multiline=None,
             *args, **kwargs):
        if not text:
            raise AttributeError("Text doesn't have to be none nor empty.")

        if pdf.text_color != rgb(foreground):
            pdf.set_text_color(*rgb(foreground))
        if pdf.fill_color != rgb(backgroud):
            pdf.set_fill_color(*rgb(backgroud))

        font = font.strip().lower()
        if font == 'arial black':
            font = 'arial'
        style = ""
        for tag in 'B', 'I', 'U':
            if text.startswith("<%s>" % tag) and text.endswith("</%s>" % tag):
                text = text[3:-4]
                style += tag
        if bold:
            style += "B"
        if italic:
            style += "I"
        if underline:
            style += "U"
        align = {'L': 'L',
                 'R': 'R',
                 'I': 'L',
                 'D': 'R',
                 'C': 'C',
                 'J': 'J',
                 '': ''
                 }.get(align)  # D/I in spanish
        pdf.set_font(font, style, size)
        #  m_k = 72 / 2.54
        #  h = (size/m_k)
        pdf.set_xy(x1, y1)
        if multiline is None:
            # multiline==None: write without wrapping/trimming (default)
            pdf.cell(w=x2 - x1, h=y2 - y1, txt=text,
                     border=0, ln=0, align=align)
        elif multiline:
            # multiline==True: automatic word - warp
            pdf.multi_cell(w=x2 - x1, h=y2 - y1, txt=text,
                           border=0, align=align)
        else:
            # multiline==False: trim to fit exactly the space defined
            text = pdf.multi_cell(
                w=x2 - x1, h=y2 - y1,
                txt=text, align=align, split_only=True)[0]
            pdf.cell(w=x2 - x1, h=y2 - y1, txt=text,
                     border=0, ln=0, align=align)

        # pdf.Text(x=x1,y=y1,txt=text)

    def line(self, pdf, x1=0, y1=0, x2=0, y2=0, size=0, foreground=0, *args, **kwargs):
        if pdf.draw_color is not rgb(foreground):
            # print "SetDrawColor", hex(foreground)
            pdf.set_draw_color(*rgb(foreground))
        # print "SetLineWidth", size
        pdf.set_line_width(size)
        pdf.line(x1, y1, x2, y2)

    def rect(self, pdf, x1=0, y1=0, x2=0, y2=0, size=0, foreground=0, backgroud=65535, *args, **kwargs):
        if pdf.draw_color is not rgb(foreground):
            pdf.set_draw_color(*rgb(foreground))
        if pdf.fill_color is not rgb(backgroud):
            pdf.set_fill_color(*rgb(backgroud))
        pdf.set_line_width(size)
        pdf.rect(x1, y1, x2 - x1, y2 - y1)

    def image(self, pdf, x1=0, y1=0, x2=0, y2=0, text='', *args, **kwargs):
        if not text:
            return False
        pdf.image(text, x1, y1, w=x2 - x1, h=y2 - y1, type='', link='')
        return True

    def barcode(self, pdf, x1=0, y1=0, x2=0, y2=0, text='', font="arial", size=1,
                foreground=0, *args, **kwargs):
        if pdf.draw_color is not rgb(foreground):
            pdf.set_draw_color(*rgb(foreground))
        font = font.lower().strip()
        if font == 'interleaved 2of5 nt':
            pdf.interleaved2of5(text, x1, y1, w=size, h=y2 - y1)

    # Added by Derek Schwalenberg Schwalenberg1013@gmail.com
    # Allow (url) links in templates (using write method) 2014-02-22
    def write(self, pdf, x1=0, y1=0, x2=0, y2=0, text='', font="arial", size=1,
              bold=False, italic=False, underline=False, align="", link='http://example.com',
              foreground=0, *args, **kwargs):
        if pdf.text_color is not rgb(foreground):
            pdf.set_text_color(*rgb(foreground))
        font = font.strip().lower()
        if font == 'arial black':
            font = 'arial'
        style = ""
        for tag in 'B', 'I', 'U':
            if text.startswith("<%s>" % tag) and text.endswith("</%s>" % tag):
                text = text[3:-4]
                style += tag
        if bold:
            style += "B"
        if italic:
            style += "I"
        if underline:
            style += "U"
        pdf.set_font(font, style, size)
        #  m_k = 72 / 2.54
        #  h = (size/m_k)
        pdf.set_xy(x1, y1)
        pdf.write(5, text, link)

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
