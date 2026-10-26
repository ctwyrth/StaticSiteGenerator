import os
import shutil
import re

from mdblocks import markdown_to_html_node, extract_title_from_markdown
from parentnode import ParentNode

def main():
   copy_source_directory("static", "public")
   generate_page("content/index.md", "template.html", "public/index.html")

def copy_source_directory(source_dir, destination_dir):
   if not os.path.exists(source_dir):
      raise ValueError(f"Source directory '{source_dir}' does not exist.")
   
   if os.path.exists(destination_dir) and os.listdir(destination_dir) != []:
      # blocking out confirmation for now to allow tests to work without user input
      # destination_exists = input(f"Destination directory '{destination_dir}' is not empty. Do you want to overwrite it? (y/n): ")
      # if destination_exists.lower() != 'y':
      #    print("Aborting copy operation.")
      #    return
      # can consider using the copy portion of this function to "backup" the contents of the destination directory before overwriting it, but for now, just delete the contents
      shutil.rmtree(destination_dir)
      print(f"Deleted contents of destination directory '{destination_dir}'.")

   if not os.path.exists(destination_dir):
      os.makedirs(destination_dir)

   for item in os.listdir(source_dir):
      source_item = os.path.join(source_dir, item)
      destination_item = os.path.join(destination_dir, item)

      if os.path.isdir(source_item):
         print(f"Moving to directory: {source_item}")
         copy_source_directory(source_item, destination_item)
      else:
         print(f"Copying file: {source_item} to {destination_item}")
         shutil.copy2(source_item, destination_item)

   print(f"Copied contents of '{source_dir}' to '{destination_dir}'.")

def generate_page(from_path, template_path, dest_path):
   print(f"Generating page from {from_path} to {dest_path} using {template_path}")

   with open(from_path, 'r') as md_f, open(template_path, 'r') as temp_f, open(dest_path, 'w') as index_f:
      md = md_f.read()
      md_to_html = markdown_to_html_node(md).to_html()
      page_title = extract_title_from_markdown(md)

      html_temp = temp_f.read()
      title_html = html_temp.replace("{{ Title }}", page_title)
      index_html = title_html.replace("{{ Content }}", md_to_html)

      index_f.write(index_html)


if __name__ == "__main__":
   main()