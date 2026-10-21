import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
   def test_leaf_to_html_p(self):
      node = LeafNode("p", "Hello, world!")
      self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

   def test_leaf_to_html_span_with_props(self):
      node = LeafNode("span", "Hello, world!", props={"class": "highlight"})
      self.assertEqual(node.to_html(), '<span class="highlight">Hello, world!</span>')

   def test_leaf_to_html_no_tag(self):
      node = LeafNode(None, "Only the text, not tag, no props!")
      self.assertEqual(node.to_html(), "Only the text, not tag, no props!")