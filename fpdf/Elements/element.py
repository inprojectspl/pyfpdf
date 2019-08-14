class Element:
    name = ''
    priority = 0
    size = 0
    pointUp = (0, 0)
    pointDo = (0, 0)
    rotate = False
    foreground = ''
    background = ''  # In INT
    height = 0
    width = 0

    def __init__(self, name='', priority=1, size=1, x1=0, y1=0, x2=0, y2=0, background='', foreground='', **kwargs):
        self.name = name
        self.size = size
        self.priority = priority
        self.pointUp = x1, y1
        self.pointDo = x2, y2
        self.width = self.pointDo[0] - self.pointUp[0]
        self.height = self.pointDo[1] - self.pointUp[1]

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

    def __init__(self, name='', priority=1, x1=0, y1=0, x2=0, y2=0, background='', foreground='', **kwargs):
        super(Boxable, self).__init__(name=name, priority=priority,
                                      x1=x1, y1=y1,
                                      x2=x2, y2=y2,
                                      background=background, foreground=foreground)
        if "Boxable" in kwargs and kwargs["Boxable"]:
            self.setboxing(**kwargs)

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

    def __init__(self, name='', priority=1, x1=0, y1=0, x2=0, y2=0, background='', foreground='', **kwargs):
        super(Captionable, self).__init__(name=name, priority=priority,
                                          x1=x1, y1=y1,
                                          x2=x2, y2=y2,
                                          background=background, foreground=foreground)
        if "Captionable" in kwargs and kwargs["Captionable"]:
            self.setcaption(**kwargs)

    def setcaption(self, margin=0, border=0, text='', **kwargs):
        self.boxing = True
        self.margin = margin
        self.border = border
        self.text = text
