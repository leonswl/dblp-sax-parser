import unittest
import pandas as pd
from src.dblp_sax_parser import DBLP_Handler

class TestDBLPHandler(unittest.TestCase):
    def setUp(self):
        # Create an instance of DBLP_Handler for testing
        self.handler = DBLP_Handler()

    def test_startElement(self):
        # Test startElement method
        tag = 'article'
        attributes = {'mdate': '2022-01-01', 'publtype': 'conference', 'key': 'article1'}
        self.handler.startElement(tag, attributes)
        self.assertEqual(self.handler.article['mdate'], '2022-01-01')
        self.assertEqual(self.handler.article['publtype'], 'conference')
        self.assertEqual(self.handler.article['key'], 'article1')

    def test_characters(self):
        # Test characters method
        content = 'Example content'
        self.handler.characters(content)
        self.assertIn(content, self.handler.text)

    def test_endElement(self):
        # Test endElement method
        tag = 'article'
        self.handler.article = {'type': 'article', 'author': ['John Doe'], 'title': 'Example Title'}
        self.handler.path = ['article']
        self.handler.text = ['John Doe', 'Example Title']
        self.handler.endElement(tag)
        self.assertEqual(len(self.handler.articles), 1)
        self.assertDictEqual(self.handler.article, {})

    def test_to_df(self):
        # Test to_df method
        self.handler.articles = [{'type': 'article', 'author': ['John Doe'], 'title': 'Example Title'}]
        self.handler.to_df()
        self.assertIsNotNone(self.handler.df)
        self.assertEqual(len(self.handler.df), 1)

    def test_to_csv(self):
        # Test to_csv method
        self.handler.df = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
        self.handler.to_csv(filename='test_output')
        # Assert that the file exists in the specified location

    def test_save(self):
        # Test save method
        self.handler.df = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
        self.handler.save(filename='test_output')
        # Assert that the file exists in the specified location

if __name__ == '__main__':
    unittest.main()
