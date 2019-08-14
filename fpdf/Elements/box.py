from .element import Element


class Box(Element):
    border = 1

    def __init__(self, name='', priority=1, x1=0, y1=0, x2=0, y2=0, background='', foreground='', **kwargs):
        super(Box, self).__init__(name=name, priority=priority,
                                  x1=x1, y1=y1,
                                  x2=x2, y2=y2,
                                  background=background, foreground=foreground)

    def render(self, pdf):
        if pdf.draw_color is not self.rgb(self.foreground):
            pdf.set_draw_color(*self.rgb(self.foreground))
        if pdf.fill_color is not self.rgb(self.background):
            pdf.set_fill_color(*self.rgb(self.background))
        pdf.set_line_width(self.size)

        pdf.rect(self.pointUp[0], self.pointUp[1], self.width, self.height)
        return True
