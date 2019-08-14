from .element import Boxable

class Text(Boxable):
    text = ''
    font = ''
    size = 0
    bold = False
    italic = True
    underline = True
    multiline = True
    align = ''
    spacing = 0

    def __init__(self, text:str, name='', priority=1, x1=0, y1=0, x2=0, y2=0, background='', foreground='', **kwargs):
        super(Text, self).__init__(name=name, priority=priority,
                                  x1=x1, y1=y1,
                                  x2=x2, y2=y2,
                                  background=background, foreground=foreground)
        self.setTextPropierties(**kwargs)

        self.setText(text)

    def setText(self, text):
        self.text = text

    def setTextPropierties(self, font='Arial', size=10,
                           bold=False, italic=False, underline=False, multiline=True,
                           align='', **kwargs):
        self.font = font
        self.size = size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.multiline = multiline
        self.align = align

    def render(self, pdf):
        if not self.text:
            raise AttributeError("Text doesn't have to be none nor empty.")

        if pdf.text_color != self.rgb(self.foreground):
            pdf.set_text_color(*self.rgb(self.foreground))
        if pdf.fill_color != self.rgb(self.background):
            pdf.set_fill_color(*self.rgb(self.background))

        font = self.font.strip().lower()
        if font == 'arial black':
            font = 'arial'
        style = ""
        for tag in 'B', 'I', 'U':
            if self.text.startswith("<%s>" % tag) and self.text.endswith("</%s>" % tag):
                self.text = self.text[3:-4]
                style += tag
        if self.bold:
            style += "B"
        if self.italic:
            style += "I"
        if self.underline:
            style += "U"
        align = {'L': 'L',
                 'R': 'R',
                 'I': 'L',
                 'D': 'R',
                 'C': 'C',
                 'J': 'J',
                 '': ''
                 }.get(self.align)  # D/I in spanish
        pdf.set_font(font, style, self.size)
        #  m_k = 72 / 2.54
        #  h = (size/m_k)
        pdf.set_xy(self.pointUp[0], self.pointUp[1])

        if self.multiline is None:
            # multiline==None: write without wrapping/trimming (default)
            pdf.cell(w=self.width, h=self.height, txt=self.text,
                     border=self.border, ln=0, align=align)
        elif self.multiline:
            # multiline==True: automatic word - warp
            pdf.multi_cell(w=self.width, h=self.height, txt=self.text,
                           border=0, align=align)
        else:
            # multiline==False: trim to fit exactly the space defined
            text = pdf.multi_cell(
                w=self.width, h=self.height,
                txt=self.text, align=align, split_only=True)[0]
            pdf.cell(w=self.width, h=self.height, txt=text,
                     border=0, ln=0, align=align)

        # pdf.Text(x=x1,y=y1,txt=text)