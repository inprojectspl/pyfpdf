from .text import Text


class Link(Text):
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