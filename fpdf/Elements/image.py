from .element import Boxable, Captionable


class Image(Boxable, Captionable):
    def __init__(self, nameImage: str, name='', priority=1, x1=0, y1=0, x2=0, y2=0, background='', foreground='', **kwargs):
        super(Image, self).__init__(name=name, priority=priority,
                                    x1=x1, y1=y1,
                                    x2=x2, y2=y2,
                                    background=background, foreground=foreground)
        self.nameImage = nameImage

    @staticmethod
    def init_from_dict(values):
        slef = Image(**values)
        if values["Boxable"]:
            slef.setboxing(**values)
        if values["Captionable"]:
            slef.setcaption(**values)
        return slef

    def render(self, pdf):
        if not self.nameImage:
            return False

        w = self.pointDo[0] - self.pointUp[0]
        h = self.pointDo[1] - self.pointUp[1]

        pdf.image(self.nameImage, self.pointUp[0], self.pointUp[1], w=w, h=h, type='', link='')
        return True
