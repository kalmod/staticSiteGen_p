from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_text,
    text_type_code,
)

from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_quote,
    block_type_ulist,
    block_type_olist,
    block_type_code,
)
import markdown_to_node

import os
import shutil


def recurCopy(targetDir, sourceDir):
    allItems = os.listdir(sourceDir)
    if len(allItems) < 1:
        print(f"Nothing within {sourceDir}")
        return
    for item in allItems:
        source = os.path.join(sourceDir, item)
        if os.path.isfile(source):
            print(f"Copying {source} to {targetDir}")
            shutil.copy(source, targetDir)

        if os.path.isdir(os.path.join(sourceDir, item)):
            newTargetDir = os.path.join(targetDir, item)
            newSourceDir = os.path.join(sourceDir, item)
            print(f"Creating directory {item} in {targetDir}")
            os.mkdir(newTargetDir)
            recurCopy(newTargetDir, newSourceDir)

    return 1


def copyDir(targetDir, sourceDir):
    if not os.path.exists(targetDir) or not os.path.exists(sourceDir):
        print("Target or Source directory does not exist")
        return
    allItems = os.listdir(sourceDir)
    if len(allItems) < 1:
        print(f"Nothing within {sourceDir}")
        return
    shutil.rmtree(targetDir)
    os.mkdir(targetDir)
    recurCopy(targetDir, sourceDir)
    return


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line
    raise ValueError("h1 NOT FOUND IN MARKDOWN")


def read_file(dir):
    file = os.open(dir, os.O_RDONLY)
    file_text = ""
    try:
        content = bytearray()
        chunk_size = 1024
        while True:
            chunk = os.read(file, chunk_size)
            if not chunk:
                break
            content.extend(chunk)
        file_text = content.decode()
    finally:
        os.close(file)
    return file_text


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read file
    markdown_content = read_file(from_path)
    title = ""

    try:
        title = extract_title(markdown_content)
    except ValueError as err:
        print(err)

    # HTML content
    markdown_node = markdown_to_node.markdown_to_html_node(markdown_content)
    html_content = markdown_node.to_html()

    # get content from template_path
    # repalce {{ title }} and {{ content }}
    # troubleshoot
    template_content = (
        read_file(template_path).replace("{{ Content }}", html_content)
    ).replace("{{ Title }}", title[2:])

    with open(os.path.join(dest_path, "index.html"), "w") as f:
        f.write(template_content)

    print("Index generated")


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    items_in_dir = os.listdir(dir_path_content)
    if len(items_in_dir) < 1:
        print(f"Nothing in {dir_path_content}")
        return
    for item in items_in_dir:
        full_path = os.path.join(dir_path_content, item)
        if os.path.isfile(full_path) and item.endswith(".md"):
            generate_page(full_path, template_path, dest_dir_path)
        if os.path.isdir(full_path):
            print("PATH")
            new_dest_path = os.path.join(dest_dir_path, item)
            print(full_path, new_dest_path)
            os.mkdir(new_dest_path)
            generate_page_recursive(
                full_path,
                template_path,
                new_dest_path
            )
    return


def main():
    # copyDir("./public", "./static")
    # Get the markdown file.

    generate_page_recursive(r"./content/", "./template.html", "./public")
    pass


if __name__ == "__main__":
    main()
