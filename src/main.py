import logging
import shutil
import os
import sys
import re

from extract_title import extract_title
from tohtml import markdown_to_html_node


SRC_PATH = "./src"
CONTENT_PATH = "./content"
MARKDOWN_FILE_NAME = "index"
HTML_TEMPLATE_FILE_NAME = "template"
HTML_TEMPLATE_PATH = os.path.join(".", f"{HTML_TEMPLATE_FILE_NAME}.html")

STATIC_PATH = "./static"
#PUBLIC_PATH = "./public"
#public_exists = os.path.exists(PUBLIC_PATH)
#if public_exists is False:
#    os.mkdir(PUBLIC_PATH)
DOC_PATH = "./doc"
doc_exists = os.path.exists(DOC_PATH)
if doc_exists is False:
    os.mkdir(DOC_PATH)



def remove_all(path:str):
    children = os.listdir(path)

    for item in children:
        item_path = os.path.join(path, item)
        Is_File, Is_Dir = os.path.isfile(item_path), os.path.isdir(item_path)

        if Is_File is True:
            os.remove(item_path)
        elif Is_Dir is True:
            remove_all(item_path)
            os.rmdir(item_path)

def copy_and_move_all(src_path:str, dst_path:str):
    children = os.listdir(src_path)

    for item in children:
        item_path = os.path.join(src_path, item)
        new_dst_path = os.path.join(dst_path, item)
        Is_File, Is_Dir = os.path.isfile(item_path), os.path.isdir(item_path)

        if Is_Dir is True:
            os.mkdir(new_dst_path)
            copy_and_move_all(item_path, new_dst_path)
        elif Is_File is True:
            shutil.copy(item_path, new_dst_path)

def generate_page(base_path, from_path, template_path, dest_path):
    print(f"Generating new page from {from_path} to {dest_path} using {template_path}")

    md_file = os.path.join(from_path, f"{MARKDOWN_FILE_NAME}.md")
    markdown_file = open(md_file)
    html_template_file = open(HTML_TEMPLATE_PATH)

    markdown = markdown_file.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    html_template = html_template_file.read()
    html_template = html_template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    html_template = html_template.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    markdown_file.close(); html_template_file.close()

    new_html_file_path = os.path.join(dest_path, "index.html")
    new_html_file = open(new_html_file_path, mode="a")
    new_html_file.write(html_template)
    new_html_file.close()

def generate_pages_recursive(base_path, from_path, template_path, dest_path):
    print(f"Creating new pages from {from_path} to {dest_path} using {template_path}")

    children = os.listdir(from_path)

    for item in children:
        item_path = os.path.join(from_path, item)
        Is_File, Is_Dir = os.path.isfile(item_path), os.path.isdir(item_path)
        
        if Is_File is True:
            print(item_path, Is_File, Is_Dir)
            generate_page(base_path, from_path, template_path, dest_path)
        elif Is_Dir is True:
            dir_src_path = os.path.join(from_path, item)
            dir_dst_path = os.path.join(dest_path, item)

            dir_dst_exists = os.path.exists(dir_dst_path)
            if dir_dst_exists is False:
                os.mkdir(dir_dst_path)

            generate_pages_recursive(base_path, dir_src_path, template_path, dir_dst_path)


def main():
    base_path = "/"
    args = sys.argv
    if len(args) > 1:
        base_path = args[1]

    remove_all(DOC_PATH)
    copy_and_move_all(STATIC_PATH, DOC_PATH)
    generate_pages_recursive(base_path, CONTENT_PATH, HTML_TEMPLATE_PATH, DOC_PATH)
    

if __name__ == '__main__':
    main()