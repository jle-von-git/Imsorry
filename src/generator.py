import os
import shutil
import re
from md_to_html import markdown_to_html_node


def copy_dir(org, dst, cleaned=False):
    """
    Function to copy a directories (org) contents into another directory (dst).
    Even though shutil.copytree does this.
    And I use the shutil library.

    org: origin directory
    
    dst: destination directory

    cleaned: Tells the function whether dst should be deleted and replaced before copying.
    """

    if not cleaned:
        if os.path.exists(dst) == False:
            raise Exception(f'"{dst}" directory not found')
        shutil.rmtree(dst)
    os.mkdir(dst)

    directory_entry_paths = os.scandir(org)

    for entry in directory_entry_paths:
        if os.path.isfile(entry):
            shutil.copy(entry, dst)
        else:
            new_path = entry.name.split("/", 2)[-1]
            copy_dir(entry, os.path.join(dst, new_path), True)


def extract_title(markdown):
    """Takes a markdown string, returns its title, raises an Exception if there is none."""
    match = re.search(r"^# .+$", markdown, re.M)

    if match == None:
        raise Exception("No h1 header found.")
    
    pos, length = match.span(0)
    header = markdown[pos : length]
    if markdown == header:
        return header[1:].strip()
    else:
        return header


def generate_page(from_path, template_path, dest_path):
    """Creates a page using content from from_path, in the format of template_path, and write it to dest_path."""

    print(f"generate_page function: {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f_p:
        from_path_markdown = f_p.read()
    
    html = markdown_to_html_node(from_path_markdown).to_html()
    title = extract_title(from_path_markdown)

    with open(template_path) as template_file:
        template_file_contents_copy = template_file.read()
        
    filled_template = template_file_contents_copy.\
        replace("{{ Title }}", title).\
        replace("{{ Content }}", html)
        
    dest_directories = dest_path.split("/")[:-1]
    current_path_in_dest = "./"

    for directory in dest_directories:
        current_path_in_dest += directory + "/"
        if os.path.exists(current_path_in_dest) == False:
            os.mkdir(current_path_in_dest)

    dest_file = open(dest_path, "x")
    dest_file.write(filled_template)
    dest_file.close()


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursive function:

    1. Crawls the directory by the 'dir_path_content' path

    2. Generates html files from markdown files in the path,
    using 'template_path' and placing them in dest_dir_path.
    """

    print(f"generate_page_recursive function: {dir_path_content} to {dest_dir_path} using {template_path}")
    entries = os.listdir(dir_path_content)

    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        dest_path  = os.path.join(dest_dir_path   , entry)
        is_markdown_file = os.path.isfile(entry_path) and entry_path[-3:] == ".md"

        if is_markdown_file:
            dest_path_html = dest_path[:-2] + "html"
            generate_page(entry_path, template_path, dest_path_html)
        elif os.path.isfile(entry_path) == False:
            generate_page_recursive(entry_path, template_path, dest_path)