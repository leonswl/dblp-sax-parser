import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.dblp_parser import DBLP_Parser


class DBLPParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = DBLP_Parser()

    def test_download_dtd(self):
        with patch('requests.get') as mock_get, \
             patch('builtins.open', create=True) as mock_open:
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1000'
            mock_response.iter_content.return_value = [b'data']
            mock_get.return_value = mock_response

            self.parser._DBLP_Parser__download_dtd()

            mock_get.assert_called_once_with(
                'https://dblp.uni-trier.de/xml/dblp.dtd', stream=True)
            mock_open.assert_called_once_with('dblp.dtd', 'wb')
            mock_open.return_value.__enter__.return_value.write.assert_called_once_with(b'data')

    def test_download_file(self):
        with patch('requests.get') as mock_get, \
             patch('builtins.open', create=True) as mock_open:
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1000'
            mock_response.iter_content.return_value = [b'data']
            mock_get.return_value = mock_response

            is_downloaded = self.parser._DBLP_Parser__download_file('url', 'filename')

            self.assertTrue(is_downloaded)
            mock_get.assert_called_once_with('url', stream=True)
            mock_open.assert_called_once_with('filename', 'wb')
            mock_open.return_value.__enter__.return_value.write.assert_called_once_with(b'data')

    def test_execute_parser(self):
        with patch('xml.sax.make_parser') as mock_make_parser, \
             patch.object(self.parser.handler, 'startElement'), \
             patch.object(self.parser.handler, 'characters'), \
             patch.object(self.parser.handler, 'endElement'):
            mock_parser = MagicMock()
            mock_make_parser.return_value = mock_parser

            result_parser, result_handler = self.parser.execute_parser('filename')

            mock_make_parser.assert_called_once_with()
            mock_parser.setContentHandler.assert_called_once_with(self.parser.handler)
            mock_parser.parse.assert_called_once_with('filename')
            self.assertEqual(result_parser, mock_parser)
            self.assertEqual(result_handler, self.parser.handler)\
            
if __name__ == '__main__':
    unittest.main()