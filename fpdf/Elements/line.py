from .Element import Element


class Line(Element):
    def render(self, pdf):
        if pdf.draw_color is not self.rgb(self.foreground):
            # print "SetDrawColor", hex(foreground)
            pdf.set_draw_color(*self.rgb(self.foreground))
        # print "SetLineWidth", size
        pdf.set_line_width(self.size)
        pdf.line(self.pointUp[0], self.pointUp[1], self.pointDo[0], self.pointDo[1])
