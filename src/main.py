import os
import shutil
import re
import pathlib

from mdblocks import markdown_to_html_node, extract_title_from_markdown
from parentnode import ParentNode

def main():
   copy_source_directory("static", "public")
   generate_pages_recursive("content", "template.html", "public")

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
   content_source = pathlib.Path(dir_path_content)
   destination = pathlib.Path(dest_dir_path)

   # check if dir_path_content is a directory or a file
   # if dir_path_content is a file...
   if content_source.is_file():
      # is file markdown
      # yes, create destination path then generate page
      if content_source.suffix.lower() == ".md":
         dest_path = destination / f"{content_source.stem}.html"
         generate_page(content_source, template_path, dest_path)
      # if not a markdown file, copy the file to the destination
      else:
         shutil.copy2(content_source, destination / content_source.name)
      return

   # if dir_path_content is a directory get the contents of the directory
   if content_source.is_dir():
      # create the directory in the destination, if not the root source directory
      directory = content_source.parts[-1]
      if directory != "content":
         new_path = os.path.join(destination, directory)
         os.makedirs(new_path)
         destination = new_path
      # iterate through each item in directory and call generate_pages_recursive on each item in directory
      for item in content_source.iterdir():
         generate_pages_recursive(item, template_path, destination)
      return

   raise ValueError("The source path does not point to a file or directory")

if __name__ == "__main__":
   main() 