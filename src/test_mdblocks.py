import unittest
from mdblocks import markdown_to_blocks, block_to_blocktype, BlockType, markdown_to_html_node

class TestMdBlocks(unittest.TestCase):
   def test_markdown_to_blocks(self):
      md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
      blocks = markdown_to_blocks(md)
      self.assertEqual(
         blocks,
         [
               "This is **bolded** paragraph",
               "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
               "- This is a list\n- with items",
         ],
      )

   def test_markdown_to_blocks_with_empty_lines(self):
      md = """
This is **bolded** paragraph.



This is another paragraph with _italic_ text and `code` here.



"""
      blocks = markdown_to_blocks(md)
      self.assertEqual(
         blocks,
         [
               "This is **bolded** paragraph.",
               "This is another paragraph with _italic_ text and `code` here.",
         ],
      )

   def test_block_to_blocktype(self):
      self.assertEqual(block_to_blocktype("This is a paragraph."), BlockType.PARAGRAPH)
      self.assertEqual(block_to_blocktype("# This is a heading"), BlockType.HEADING)
      self.assertEqual(block_to_blocktype("> This is a quote"), BlockType.QUOTE)
      self.assertEqual(block_to_blocktype("- This is an unordered list item"), BlockType.UNORDERED_LIST)
      self.assertEqual(block_to_blocktype("1. This is an ordered list item"), BlockType.ORDERED_LIST)
      self.assertEqual(block_to_blocktype("```\nThis is a code block\n```"), BlockType.CODE)

   def test_block_to_blocktype_with_multiline_blocks(self):
      self.assertEqual(block_to_blocktype("This is a paragraph.\nThis is still the same paragraph."), BlockType.PARAGRAPH)
      self.assertEqual(block_to_blocktype("# This is a heading\nThis is still part of the heading."), BlockType.PARAGRAPH)
      self.assertEqual(block_to_blocktype("> This is a quote\n> This is still part of the quote."), BlockType.QUOTE)
      self.assertEqual(block_to_blocktype("- This is an unordered list item\n- This is still part of the unordered list."), BlockType.UNORDERED_LIST)
      self.assertEqual(block_to_blocktype("1. This is an ordered list item\n2. This is still part of the ordered list."), BlockType.ORDERED_LIST)
      self.assertEqual(block_to_blocktype("```\nThis is a code block\nThis is still part of the code block\n```"), BlockType.CODE)

   def test_paragraphs(self):
      md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
      node = markdown_to_html_node(md)
      html = node.to_html()
      self.assertEqual(
         html,
         "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
      )

   def test_headings_remove_all_markers_and_keep_inline_formatting(self):
      for level in range(1, 7):
         with self.subTest(level=level):
            heading = markdown_to_html_node(f"{'#' * level} A **bold** heading").children[0]
            self.assertEqual(
               heading.to_html(),
               f"<h{level}>A <b>bold</b> heading</h{level}>",
            )

   def test_codeblock_preserves_lines_and_markdown_characters(self):
      md = "```\nline with _underscores_\nline with **asterisks** and `backticks\n```"
      node = markdown_to_html_node(md)
      self.assertEqual(
         node.to_html(),
         "<div><pre><code>line with _underscores_\nline with **asterisks** and `backticks</code></pre></div>",
      )

   def test_quoteblock_removes_markers_on_every_line(self):
      md = "> first line\n>\n>second line"
      node = markdown_to_html_node(md)
      self.assertEqual(
         node.to_html(),
         "<div><blockquote>first line\n\nsecond line</blockquote></div>",
      )

def test_extract_title(markdown):
   md = "# This is our h1 title!\nAnd, this is just some paragraph text."
   self.assertEqual(
      extract_title(md), "This is our h1 title!"
   )

def test_extract_title_failed(markdown):
   md = "## Here we go again with an h2.\n### And an h3!"