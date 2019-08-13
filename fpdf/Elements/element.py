class Element:
    name = ''
    priority = 0
    pointUp = (0, 0)
    pointDo = (0, 0)
    rotate = False
    foreground = ''
    background = ''  # In INT

    def __init__(self, name='', priority=1, x1=0, y1=0, x2=0, y2=0, background='', foreground='', **kwargs):
        self.name = name
        self.priority = priority
        self.pointUp = x1, y1
        self.pointDo = x2, y2
        self.background = background
        self.foreground = foreground

    @staticmethod
    def init_from_dict(values):
        return Element(**values)

    def rgb(self, col):
        return (col // 65536), (col // 256 % 256), (col % 256)

    def render(self, pdf):
        pass


class Boxable(Element):
    boxing = False
    margin = 0
    border = 0

    def setBos(self, margin=0, border=0):
        self.boxing = True
        self.margin = margin
        self.border = border


class Captionable(Element):
    text = ''
    caption = False
    align = ''
    boxing = False
    margin = 0
    border = 0

    def setcaption(self, margin=0, border=0, text=''):
        self.boxing = True
        self.margin = margin
        self.border = border
        self.text = text
