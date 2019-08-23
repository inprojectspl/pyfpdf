"""png_image_test.py"""

import unittest
import sys
import os
sys.path.insert(0,
  os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.path.join('..', '..')
  )
)
from fpdf.template import Template
from test.utilities import relative_path_to, \
                           set_doc_date_0, \
                           calculate_hash_of_file


class RenderTemplate(unittest.TestCase):

    def test_RenderCSV(self):
        f = Template(paperformat="A4",
                     title="testCSV")

        f.parse_YML("testDefaults.yaml")
        f.add_page("testDefaults.yaml")

        pdf = f.getFPDF()
        set_doc_date_0(pdf)

        outfile = relative_path_to("testTemplateFile.pdf")
        pdf.output(outfile, 'F')

        test_hash = calculate_hash_of_file(outfile)
        # Assert versus a well know hash of TestTemplateFile
        self.assertEqual(test_hash, "8d4e2060e5d8264d03ebca707a2ed1ca")

        os.unlink(outfile)


if __name__ == '__main__':
    unittest.main()
