import re
from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
   TEXT = ("", "")
   BOLD = ("<strong>", "</strong>")
   ITALIC = ("<em>", "</em>")
   CODE = ("<code>", "</code>")
   LINK = ("<a href='{url}'>", "{anchor}</a>")
   IMAGE = ("<img src='{url}'", "alt='{alt}' />")

class TextTypeDelimiter(Enum):
   BOLD = "**"
   ITALIC = "*"
   CODE = "`"
   LINK = "[]()"
   IMAGE = "![]()"

class TextNode:
   def __init__(self, text: str, text_type: TextType = None, url: str = None):
         self.text = text
         self.text_type = text_type
         self.url = url

   def __eq__(self, other):
         if not isinstance(other, TextNode):
            return False
         return self.text == other.text and self.text_type == other.text_type and self.url == other.url

   def __repr__(self):
      return f"TextNode(text={self.text}, text_type={self.text_type}, url={self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
   if text_node.text_type is TextType.TEXT:
      return LeafNode("", text_node.text)

   if text_node.text_type == TextType.BOLD:
      return LeafNode("strong", text_node.text)
   if text_node.text_type == TextType.ITALIC:
      return LeafNode("em", text_node.text)

   if text_node.text_type == TextType.CODE:
      return LeafNode("code", text_node.text)

   if text_node.text_type == TextType.LINK:
      if text_node.url is None:
         raise ValueError("LINK text type requires a URL for the href attribute.")
      return LeafNode("a", text_node.text, props={"href": text_node.url})

   if text_node.text_type == TextType.IMAGE:
      if text_node.url is None:
         raise ValueError("IMAGE text type requires a URL for the source attribute.")
      return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})

   tag = text_node.text_type.value[0][1:-1]  # Extract the tag name from the opening tag
   return LeafNode(tag, text_node.text)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
   result = []

   for node in old_nodes:
      if node.text_type == TextType.TEXT:
         if delimiter not in node.text:
            raise Exception(f"Delimiter '{delimiter}' not found in text: '{node.text}'")
         
         parts = node.text.split(delimiter)
         for i in range(len(parts)):
            if i % 2 == 1:  # Odd indices are the delimited parts
               result.append(TextNode(parts[i], text_type))
            else:  # Even indices are the non-delimited parts
               result.append(TextNode(parts[i], TextType.TEXT))
      else:
         result.append(node)
   return result

def extract_markdown_images(text: str):
   image_pattern = r"!\[(.*?)\]\((.*?)\)"
   matches = re.findall(image_pattern, text)
   return matches

def extract_markdown_links(text: str):
   link_pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
   matches = re.findall(link_pattern, text)
   return matches