from .element import Captionable


class Barcode(Captionable):

    def __init__(self, text: str, font='interleaved 2of5 nt', name='', priority=1, x1=0, y1=0, x2=0, y2=0, background='', foreground='',**kwargs):
        super(Barcode, self).__init__(name=name, priority=priority,
                                      x1=x1, y1=y1,
                                      x2=x2, y2=y2,
                                      background=background, foreground=foreground)
        self.font = font
        self.setcaption(**kwargs)
        self.text = text

    def render(self, pdf):
        if pdf.draw_color is not self.rgb(self.foreground):
            pdf.set_draw_color(*self.rgb(self.foreground))
        font = self.font.lower().strip()

        pdf.code39(self.text, self.pointUp[0], self.pointUp[1], w=self.size, h=self.height)
