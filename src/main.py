from textnode import TextNode, TextType

def main():
   test_node = TextNode("Hello, World!", TextType.BOLD, url="https://example.com")
   print(test_node)
   # print("Hello, World!")

if __name__ == "__main__":
   main()