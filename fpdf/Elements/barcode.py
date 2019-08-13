from .element import Captionable


class Barcode(Captionable):

    @staticmethod
    def init_from_dict(values):
        slef = Barcode(**values)
        slef.setTextPropierties(**values)
        if values["Boxable"]:
            slef.setboxing(**values)
        if values["Captionable"]:
            slef.setcaption(**values)
        return slef

    def render(self, pdf):
        if pdf.draw_color is not self.rgb(self.foreground):
            pdf.set_draw_color(*self.rgb(self.foreground))
        font = self.font.lower().strip()
        if font == 'interleaved 2of5 nt':
            h = self.pointDo[1] - self.pointUp[1]
            pdf.interleaved2of5(self.text, self.pointUp[0], self.pointUp[1], w=self.size, h=h)
