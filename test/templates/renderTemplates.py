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
import test

from test.utilities import relative_path_to, \
                           set_doc_date_0, \
                           calculate_hash_of_file


class RenderTemplateCSV(unittest.TestCase):

    def test_RenderCSV(self):
        f = Template(paperformat="A4",
                     title="testCSV")

        f.parse_csv("testTemplateFile.csv", delimiter=";")
        f.add_page("testTemplateFile.csv")

        f.render("testTemplateFile.pdf")
        outfile = relative_path_to("testTemplateFile.pdf")
        # print(calculate_hash_of_file(outfile))

        test_hash = calculate_hash_of_file(outfile)
        # ordered the images for reproduceability
        self.assertEqual(test_hash, "3f086c8f44935bfe19df64822974af2e")

        os.unlink(outfile)


if __name__ == '__main__':
    unittest.main()
