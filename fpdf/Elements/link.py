from .text import Text


class Link(Text):

    def __init__(self, link: str, text: str,
                 name='', priority=1,
                 x1=0, y1=0,
                 x2=0, y2=0,
                 background='', foreground='', **kwargs):
        super(Link, self).__init__(name=name, priority=priority,
                                   x1=x1, y1=y1,
                                   x2=x2, y2=y2,
                                   background=background, foreground=foreground)
        self.setTextPropierties(**kwargs)

        self.setText(text)
        self.link = link

    def render(self, pdf):
        if pdf.text_color is not self.rgb(self.foreground):
            pdf.set_text_color(*self.rgb(self.foreground))
        self.font = self.font.strip().lower()
        if self.font == 'arial black':
            self.font = 'arial'
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
        pdf.set_font(self.font, style, self.size)
        #  m_k = 72 / 2.54
        #  h = (size/m_k)

        pdf.set_xy(self.pointUp[0], self.pointUp[1])
        pdf.write(5, self.text, self.link)