"""Public-source extraction regressions; these tests do not assess writing."""
import importlib.util
from pathlib import Path
import unittest

import fitz


SCRIPT = Path(__file__).resolve().parents[1] / 'distill/20261018/fetch_sources.py'
SPEC = importlib.util.spec_from_file_location('distill_fetch_sources', SCRIPT)
FETCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FETCH)


class SourceExtractionTests(unittest.TestCase):
    def test_publisher_pdf_with_leading_newline_retains_text(self):
        with fitz.open() as document:
            page = document.new_page()
            page.insert_text((72, 72), 'A public English research article.')
            raw = document.tobytes()
        expected = FETCH.extract(raw, 'application/pdf')
        actual = FETCH.extract(b'\r\n' + raw, 'application/pdf')
        self.assertEqual(actual, expected)
        self.assertEqual(actual[0], 'pdf')
        self.assertIn('A public English research article.', actual[1])
        self.assertEqual(actual[2]['pages'], 1)

    def test_pdf_mime_type_does_not_turn_a_landing_page_into_full_text(self):
        with self.assertRaises(ValueError):
            FETCH.extract(b'<html><body>Article abstract only</body></html>', 'application/pdf')

    def test_pdf_signature_alone_is_not_a_valid_article(self):
        with self.assertRaises(fitz.FileDataError):
            FETCH.extract(b'\r\n%PDF-1.5\nnot a document', 'application/pdf')


if __name__ == '__main__':
    unittest.main()
