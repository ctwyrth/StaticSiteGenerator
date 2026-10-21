import unittest
from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
   def test_eq(self):
      node = HtmlNode("div", "This is a div", props={"class": "container"})
      node2 = HtmlNode("div", "This is a div", props={"class": "container"})
      self.assertEqual(node, node2)

   def test_repr(self):
      node = HtmlNode("a", "Click Here", props={"html": "https://www.example.com"})
      expected_repr = "HtmlNode(tag=a, value=Click Here, children=[], props={'html': 'https://www.example.com'})"
      self.assertEqual(repr(node), expected_repr)

   def test_eq_different_tag(self):
      node = HtmlNode("div", "This is a div", props={"class": "container"})
      node2 = HtmlNode("span", "This is a div", props={"class": "container"})
      self.assertNotEqual(node, node2)

   def test_eq_different_value(self):
      node = HtmlNode("div", "This is a div", props={"class": "container"})
      node2 = HtmlNode("div", "This is a different div", props={"class": "container"})
      self.assertNotEqual(node, node2)

   def test_eq_different_props(self):
      node = HtmlNode("div", "This is a div", props={"class": "container"})
      node2 = HtmlNode("div", "This is a div", props={"id": "main"})
      self.assertNotEqual(node, node2)
