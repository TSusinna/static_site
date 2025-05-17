import os
import shutil

from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

# Defines the paths for the static and public directories, content directory, and template file
dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

# This function calls copy_files_recursive to clean and copy files from the static directory to the public directory
# and then calls generate_page to generate the HTML page from the markdown file
# It also prints the progress of the operations
def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static directory to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)
    print("Done!")

main()