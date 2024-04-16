import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_bold,
    text_type_italic,
    text_type_link,
    text_type_image,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        delimited_string = node.text.split(
            delimiter
        )  # if arr[0] = "" > starts with delimeted, else doesn't start
        if len(delimited_string) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(delimited_string)):
            if delimited_string[i] == "":
                continue
            elif i % 2 == 0:
                new_nodes.append(TextNode(delimited_string[i], text_type_text))
            else:
                new_nodes.append(TextNode(delimited_string[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    # I need to return a list of tuples (altText, Url)
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    # I need to return a list of tuples (altText, Url)
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_images(text)
        if not matches:
            result.append(node)
            continue
        for tup in matches:
            found_text = text.split(f"![{tup[0]}]({tup[1]})", 1)
            # Must check if exists. If starts on split, it'll be empty
            if found_text[0]:
                new_node = TextNode(found_text[0], text_type_text)
                result.append(new_node)
            if len(found_text) > 1:
                new_node = TextNode(tup[0], text_type_image, tup[1])
                result.append(new_node)
            text = found_text[1]

        if text:
            new_node = TextNode(text, text_type_text)
            result.append(new_node)
    return result


def split_nodes_link(old_nodes):
    result = []

    for node in old_nodes:
        text = node.text
        matches = extract_markdown_links(text)
        if not matches:
            result.append(node)
            continue
        for tup in matches:
            found_text = text.split(f"[{tup[0]}]({tup[1]})", 1)
            # Must check if exists. If starts on split, it'll be empty
            if found_text[0]:
                new_node = TextNode(found_text[0], text_type_text)
                result.append(new_node)
            if len(found_text) > 1:
                new_node = TextNode(tup[0], text_type_link, tup[1])
                result.append(new_node)
            text = found_text[1]
        if text:
            new_node = TextNode(text, text_type_text)
            result.append(new_node)
    return result


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


# I think the function below would work for nested or multiple markdown delimiters
# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     delim_stack = []
#     for node in old_nodes:
#         prev = 0
#         for i in range(len(node.text)):
#             if node.text[i] == delimiter:
#                 new_text = node.text[prev:i]
#                 text_type = ""
#                 if delim_stack and delim_stack[-1] == node.text[i]:
#                     text_type = delim_stack.pop()
#                 else:
#                     delim_stack.append(delimiter)

#                 new_nodes.append(TextNode(new_text, delimiter_type[text_type]))
#                 prev = i + 1
#         new_nodes.append(TextNode(node.text[prev:], delimiter_type[""]))
#     if len(delim_stack) > 0:
#         raise TypeError("That's invalid Markdown syntax")
#     return new_nodes
