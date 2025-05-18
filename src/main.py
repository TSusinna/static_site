import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

# Defines the paths for the static and public directories, content directory, and template file
dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

# This function generates a static site by copying static files and generating HTML pages from markdown files
# It takes the base path as an argument, which is used to set the base URL for the generated pages
# It first deletes the public directory if it exists, then copies the static files to the public directory
# It then generates HTML pages from the markdown files in the content directory using the specified template
def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static directory to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
    print("Done!")

main()