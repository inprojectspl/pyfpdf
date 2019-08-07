from .Element import Element


class Box(Element):
    border = 1

    def render(self, pdf):
        if pdf.draw_color is not self.rgb(self.foreground):
            pdf.set_draw_color(*self.rgb(self.foreground))
        if pdf.fill_color is not self.rgb(self.backgroud):
            pdf.set_fill_color(*self.rgb(self.backgroud))
        pdf.set_line_width(self.size)

        pdf.line(self.pointUp[0], self.pointUp[1], self.pointDo[0], self.pointDo[1])
        return True
