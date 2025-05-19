import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

# This function recursively generates HTML pages from markdown files in the content directory
# It takes the content directory path, template file path, and destination directory path as arguments
# It iterates through the files in the content directory, and for each markdown file,
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

# This function generates a page from a markdown file and a template file
# and saves the generated HTML to the destination path
# It reads the markdown content, converts it to HTML, and replaces placeholders in the template with the title and content
# It also creates the destination directory if it doesn't exist
def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    clean_basepath = "/" + basepath.strip("/") + "/"
    while "//" in clean_basepath:
        clean_basepath = clean_basepath.replace("//", "/")
    if clean_basepath == "/":
        pass
    else:
        path_prefix = clean_basepath.rstrip("/")
        # Only replace if not already using the correct basepath
        template = template.replace('href="/', f'href="{path_prefix}/')
        template = template.replace('src="/', f'src="{path_prefix}/')
        # Fix double basepath if already present
        template = template.replace(f'href="{path_prefix}{path_prefix}/', f'href="{path_prefix}/')
        template = template.replace(f'src="{path_prefix}{path_prefix}/', f'src="{path_prefix}/')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

# This function extracts the title from the markdown content
# It looks for the first line that starts with "# " and returns the text after it
def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")