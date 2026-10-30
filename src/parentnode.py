from htmlnode import HtmlNode

class ParentNode(HtmlNode):
   def __init__(self, tag:str = None, children: list = None, props: dict = None):
      super().__init__(tag, None, children, props)
      self.tag = tag
      self.children = children if children is not None else []
      self.props = props if props is not None else {}

   def to_html(self, basepath=""):
      if self.tag is None:
         raise ValueError("ParentNode must have a tag.")

      if self.children is None or len(self.children) == 0:
         raise ValueError("ParentNode must have at least one child.")

      props_str = self.props_to_html(basepath)

      children_html = "".join(child.to_html(basepath) for child in self.children)

      return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

   def __repr__(self):
      return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"