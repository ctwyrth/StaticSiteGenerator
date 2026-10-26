import re
from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
   TEXT = ("", "")
   BOLD = ("<b>", "</b>")
   ITALIC = ("<i>", "</i>")
   CODE = ("<code>", "</code>")
   LINK = ("<a href='{url}'>", "{anchor}</a>")
   IMAGE = ("<img src='{url}'", "alt='{alt}' />")

class TextTypeDelimiter(Enum):
   BOLD = "**"
   ITALIC = "_"
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
   if text_node.text_type == TextType.TEXT:
      return LeafNode(None, text_node.text)

   if text_node.text_type == TextType.BOLD:
      return LeafNode("b", text_node.text)

   if text_node.text_type == TextType.ITALIC:
      return LeafNode("i", text_node.text)

   if text_node.text_type == TextType.CODE:
      return LeafNode("code", text_node.text)

   if text_node.text_type == TextType.LINK:
      if text_node.url == None:
         raise ValueError("LINK text type requires a URL for the href attribute.")
      return LeafNode("a", text_node.text, props={"href": text_node.url})

   if text_node.text_type == TextType.IMAGE:
      if text_node.url == None:
         raise ValueError("IMAGE text type requires a URL for the source attribute.")
      return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})

   tag = text_node.text_type.value[0][1:-1]  # Extract the tag name from the opening tag
   return LeafNode(tag, text_node.text)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
   result = []

   for node in old_nodes:
      if node.text_type != TextType.TEXT:
         result.append(node)
         continue

      new_nodes = []
      parts = node.text.split(delimiter)
      if len(parts) % 2 == 0:
         raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
      for i in range(len(parts)):
         if parts[i] == "":
            continue
         if i % 2 == 0:
            new_nodes.append(TextNode(parts[i], TextType.TEXT))
         else:
            new_nodes.append(TextNode(parts[i], text_type))
      result.extend(new_nodes)

   return result

def extract_markdown_images(text: str):
   image_pattern = r"!\[(.*?)\]\((.*?)\)"
   matches = re.findall(image_pattern, text)
   return matches

def extract_markdown_links(text: str):
   link_pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
   matches = re.findall(link_pattern, text)
   return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
   result = []

   for node in old_nodes:
      if node.text_type == TextType.TEXT:
         image_matches = extract_markdown_images(node.text)
         if not image_matches:
            result.append(node)
            continue

         last_index = 0
         for match in image_matches:
            alt_text, url = match
            start_index = node.text.find(f"![{alt_text}]({url})", last_index)
            if start_index > last_index:
               result.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            result.append(TextNode(alt_text, TextType.IMAGE, url = url))
            last_index = start_index + len(f"![{alt_text}]({url})")

         if last_index < len(node.text):
            result.append(TextNode(node.text[last_index:], TextType.TEXT))
      else:
         result.append(node)

   return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
   result = []

   for node in old_nodes:
      if node.text_type == TextType.TEXT:
         link_matches = extract_markdown_links(node.text)
         if not link_matches:
            result.append(node)
            continue

         last_index = 0
         for match in link_matches:
            anchor_text, url = match
            start_index = node.text.find(f"[{anchor_text}]({url})", last_index)
            if start_index > last_index:
               result.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            result.append(TextNode(anchor_text, TextType.LINK, url = url))
            last_index = start_index + len(f"[{anchor_text}]({url})")

         if last_index < len(node.text):
            result.append(TextNode(node.text[last_index:], TextType.TEXT))
      else:
         result.append(node)

   return result

def text_to_textnodes(text) -> list[TextNode]:
   nodes = [TextNode(text, TextType.TEXT)]
   nodes = split_nodes_image(nodes)
   nodes = split_nodes_link(nodes)
   nodes = split_nodes_delimiter(nodes, TextTypeDelimiter.BOLD.value, TextType.BOLD)
   nodes = split_nodes_delimiter(nodes, TextTypeDelimiter.ITALIC.value, TextType.ITALIC)
   nodes = split_nodes_delimiter(nodes, TextTypeDelimiter.CODE.value, TextType.CODE)
   return nodes
