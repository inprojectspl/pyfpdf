class Element:
    name = ''
    priority = 0
    pointUp = (0, 0)
    pointDo = (0, 0)
    rotate = False
    foreground = ''
    background = ''  # In INT

    def __init__(self, name='', priority=1, pointup=(0, 0), pointdo=(0, 0), background='', foreground=''):
        self.name = name
        self.priority = priority
        self.pointUp = pointup
        self.pointDo = pointdo
        self.background = background
        self.foreground = foreground

    def rgb(self, col):
        return (col // 65536), (col // 256 % 256), (col % 256)

    def render(self, pdf):
        pass


class Boxable(Element):
    boxing = False
    margin = 0
    border = 0

    def setboxing(self, margin=0, border=0):
        self.boxing=True
        self.margin = margin
        self.border = border


class Captionable(Element):
    text = ''
    caption = False
    align = ''

    def setboxing(self, margin=0, border=0):
        self.boxing=True
        self.margin = margin
        self.border = border
