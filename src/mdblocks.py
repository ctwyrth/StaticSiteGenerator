import re
from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, text_to_textnodes

class BlockType(Enum):
   PARAGRAPH = "p"
   HEADING = "h"
   CODE = "code"
   QUOTE = "blockquote"
   UNORDERED_LIST = "ul"
   ORDERED_LIST = "ol"

class MdBlocks:
   def __init__(self, markdown: str):
      self.markdown = markdown

   def __eq__(self, other):
      if not isinstance(other, MdBlocks):
         return False
      return self.markdown == other.markdown

def markdown_to_blocks(markdown: str):
   basic_blocks = markdown.split("\n\n")
   clean_blocks = []

   for block in basic_blocks:
      if block.strip() == "":
         continue
      clean_blocks.append(block.strip())

   return clean_blocks

def block_to_blocktype(block: str) -> BlockType:
   if block.startswith("```\n") and block.endswith("\n```"):
      return BlockType.CODE

   if re.match(r"\A#{1,6}\s[^\n]*\Z", block):
      return BlockType.HEADING

   if re.match(r"\A(> ?.*\n?)+\Z", block, re.M):
      return BlockType.QUOTE

   if re.match(r"\A([*\-+] .*\n?)+\Z", block, re.M):
      return BlockType.UNORDERED_LIST

   if re.match(r"\A(\d+\. .*\n?)+\Z", block, re.M):
      return BlockType.ORDERED_LIST

   return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> ParentNode:
   blocks = markdown_to_blocks(markdown)
   nodes = []

   for block in blocks:
      block_type = block_to_blocktype(block)

      if block_type == BlockType.PARAGRAPH:
         text_nodes = text_to_textnodes(no_linebreaks_in_block(block))
         html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
         nodes.append(ParentNode("p", html_nodes))
      elif block_type == BlockType.HEADING:
         match = re.match(r"\A(#{1,6})\s", block)
         if match:
            heading_level = len(match.group(1))
            heading_text = block[match.end():]
            text_nodes = text_to_textnodes(no_linebreaks_in_block(heading_text))
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            nodes.append(ParentNode(f"h{heading_level}", html_nodes))
      elif block_type == BlockType.CODE:
         code_content = block[4:-4]  # Remove the ``` markers
         nodes.append(ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])]))
      elif block_type == BlockType.QUOTE:
         quote_lines = block.splitlines()
         quote_text = "\n".join(re.sub(r"^> ?", "", line) for line in quote_lines)
         quote_text_nodes = text_to_textnodes(quote_text)
         quote_html_nodes = [text_node_to_html_node(text_node) for text_node in quote_text_nodes]
         nodes.append(ParentNode("blockquote", quote_html_nodes))
      elif block_type == BlockType.UNORDERED_LIST:
         list_items = block.splitlines()
         list_nodes = []
         for item in list_items:
            item_text = item[2:]  # Remove the "- " or "* " or "+ "
            item_text_nodes = text_to_textnodes(item_text)
            item_html_nodes = [text_node_to_html_node(text_node) for text_node in item_text_nodes]
            list_nodes.append(ParentNode("li", item_html_nodes))
         nodes.append(ParentNode("ul", list_nodes))
      elif block_type == BlockType.ORDERED_LIST:
         list_items = block.splitlines()
         list_nodes = []
         for item in list_items:
            item_text = re.sub(r"^\d+\.\s", "", item)  # Remove the "1. ", "2. ", etc.
            item_text_nodes = text_to_textnodes(item_text)
            item_html_nodes = [text_node_to_html_node(text_node) for text_node in item_text_nodes]
            list_nodes.append(ParentNode("li", item_html_nodes))
         nodes.append(ParentNode("ol", list_nodes))

   return ParentNode("div", nodes)  # Wrap all nodes in a parent div

def extract_title_from_markdown(markdown: str) -> str:
   lines = markdown.splitlines()

   for line in lines:
      if line.startswith("# "):
         return line.lstrip("# ").strip()

   raise Exception("No h1 header is present.") # loop finishes with no h1, exception is raised

def no_linebreaks_in_block(block: str) -> str:
   return block.replace("\n", " ")