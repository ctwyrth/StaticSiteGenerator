import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):
   def test_eq(self):
      node = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a text node", TextType.BOLD)
      self.assertEqual(node, node2)
   
   def test_repr(self):
      node = TextNode("This is a text node", TextType.ITALIC)
      expected_repr = "TextNode(text=This is a text node, text_type=TextType.ITALIC, url=None)"
      self.assertEqual(repr(node), expected_repr)

   def test_eq_different_text(self):
      node = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a different text node", TextType.BOLD)
      self.assertNotEqual(node, node2)

   def test_eq_different_type(self):
      node = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a text node", TextType.ITALIC)
      self.assertNotEqual(node, node2)

   def test_eq_different_url(self):
      node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
      node2 = TextNode("This is a text node", TextType.LINK, url="https://different.com")
      self.assertNotEqual(node, node2)

   def test_text(self):
      node = TextNode("This is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "")
      self.assertEqual(html_node.value, "This is a text node")

   def test_image(self):
      node = TextNode("This is an image", TextType.IMAGE, url="https://example.com/image.png")
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "img")
      self.assertEqual(html_node.props["src"], "https://example.com/image.png")
      self.assertEqual(html_node.props["alt"], "This is an image")

   def test_split_nodes_bold(self):
      old_nodes = [
         TextNode("This is a **bold** text", TextType.TEXT),
         TextNode("italic", TextType.ITALIC),
         TextNode("code", TextType.CODE),
      ]
      delimiter = "**"
      text_type = TextType.BOLD
      new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
      self.assertEqual(len(new_nodes), 5)
      self.assertEqual(new_nodes[0].text, "This is a ")
      self.assertEqual(new_nodes[1].text, "bold")
      self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
      self.assertEqual(new_nodes[2].text, " text")

   def test_split_nodes_italic(self):
      old_nodes = [
         TextNode("This is an *italic* text", TextType.TEXT),
         TextNode("bold", TextType.BOLD),
         TextNode("code", TextType.CODE),
      ]
      delimiter = "*"
      text_type = TextType.ITALIC
      new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
      self.assertEqual(len(new_nodes), 5)
      self.assertEqual(new_nodes[0].text, "This is an ")
      self.assertEqual(new_nodes[1].text, "italic")
      self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
      self.assertEqual(new_nodes[2].text, " text")

   def test_split_nodes_code(self):
      old_nodes = [
         TextNode("This is a `code` text", TextType.TEXT),
         TextNode("bold", TextType.BOLD),
         TextNode("italic", TextType.ITALIC),
      ]
      delimiter = "`"
      text_type = TextType.CODE
      new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
      self.assertEqual(len(new_nodes), 5)
      self.assertEqual(new_nodes[0].text, "This is a ")
      self.assertEqual(new_nodes[1].text, "code")
      self.assertEqual(new_nodes[1].text_type, TextType.CODE)
      self.assertEqual(new_nodes[2].text, " text")

   def test_extract_link(self):
      matches = extract_markdown_links("This is a [link](https://example.com) in the text.")
      self.assertEqual([("link", "https://example.com")], matches)

   def test_extract_image(self):
      matches = extract_markdown_images("This is an ![image](https://example.com/image.png) in the text.")
      self.assertEqual([("image", "https://example.com/image.png")], matches)

   def test_not_extract_link_from_image(self):
      matches = extract_markdown_links("This is an ![image](https://example.com/image.png) in the text.")
      self.assertEqual([], matches)

   def test_split_images(self):
      node = TextNode(
         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
         TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
         [
               TextNode("This is text with an ", TextType.TEXT),
               TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
               TextNode(" and another ", TextType.TEXT),
               TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
         ],
         new_nodes,
      )

   def test_split_links(self):
      node = TextNode(
         "This is text with a [link](https://example.com) and another [second link](https://example.org)",
         TextType.TEXT,
      )
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
         [
               TextNode("This is text with a ", TextType.TEXT),
               TextNode("link", TextType.LINK, "https://example.com"),
               TextNode(" and another ", TextType.TEXT),
               TextNode("second link", TextType.LINK, "https://example.org"),
         ],
         new_nodes,
      )

   def test_text_to_textnodes(self):
      text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
      nodes = text_to_textnodes(text)
      self.assertEqual(len(nodes), 10)
      self.assertListEqual(
         [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
         ],
         nodes,
      )

if __name__ == '__main__':
   unittest.main()