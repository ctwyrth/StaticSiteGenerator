class HtmlNode:
   def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
      self.tag = tag
      self.value = value
      self.children = children if children is not None else []
      self.props = props if props is not None else {}

   def to_html(self):
      raise NotImplementedError("Subclasses must implement the to_html method.")

   def props_to_html(self):
      if not self.props:
         return ""
      props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
      return f" {props_str}"

   def __repr__(self):
      return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

   def __eq__(self, other):
      if not isinstance(other, HtmlNode):
         return False
      return (self.tag == other.tag and
               self.value == other.value and
               self.children == other.children and
               self.props == other.props)