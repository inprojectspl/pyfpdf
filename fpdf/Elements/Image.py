from .Element import Boxable, Captionable


class Image(Boxable, Captionable):
    def render(self, pdf):
        if not self.text:
            return False

        w = self.pointDo[0] - self.pointUp[0]
        h = self.pointDo[1] - self.pointUp[1]

        pdf.image(self.text, self.pointUp[0], self.pointUp[1], w=w, h=h, type='', link='')
        return True
