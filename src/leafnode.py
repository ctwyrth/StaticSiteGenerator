from htmlnode import HtmlNode

class LeafNode(HtmlNode):
   def __init__(self, tag: str = None, value: str = None, props: dict = None):
      super().__init__(tag, value, None, props)
      self.tag = tag
      self.value = value
      self.props = props if props is not None else {}

   def to_html(self, basepath=""):
      if self.value is None:
         raise ValueError("LeafNode must have a value.")

      if self.tag is None:
         return self.value if self.value is not None else ""

      props_str = self.props_to_html(basepath)

      return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

   def __repr__(self):
      return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"