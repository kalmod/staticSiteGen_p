import blocks
import htmlnode
import inline_markdown
import textnode
import re


block_type_map = {
    blocks.block_type_paragraph: "p",
    blocks.block_type_quote: "blockquote",
    blocks.block_type_code: "code",
    blocks.block_type_ulist: "ul",
    blocks.block_type_olist: "ol",
    blocks.block_type_heading: "h",
}


def convert_to_leafNodes(inline_nodes):
    leafNodes = []
    for node in inline_nodes:
        leafNodes.append(textnode.text_node_to_html_node(node))
    return leafNodes


def block_to_paragraphNode(block, block_type):
    inline_nodes = inline_markdown.text_to_textnodes(block)
    leafNodes = convert_to_leafNodes(inline_nodes)
    return htmlnode.ParentNode(block_type_map[block_type], leafNodes)


def block_to_quoteNode(block, block_type):
    content = " ".join(re.findall(r"^> (.*)", block, re.MULTILINE))
    inline_nodes = inline_markdown.text_to_textnodes(content)
    leafNodes = convert_to_leafNodes(inline_nodes)
    return htmlnode.ParentNode(block_type_map[block_type], leafNodes)


def block_to_codeNode(block, block_type):
    inline_nodes = inline_markdown.text_to_textnodes(block)
    leafNodes = convert_to_leafNodes(inline_nodes)
    return htmlnode.ParentNode("pre", leafNodes)


def block_to_ulNode(block, block_type):
    li = []
    pattern = r"^[*-] (.*)"
    # for m in re.findall(pattern, block, re.MULTILINE):
    #     inline_nodes.append(htmlnode.LeafNode("li", m))
    for m in re.findall(pattern, block, re.MULTILINE):
        leaf = convert_to_leafNodes(inline_markdown.text_to_textnodes(m))
        li.append(htmlnode.ParentNode("li", leaf))
    return htmlnode.ParentNode(block_type_map[block_type], li)


def block_to_olNode(block, block_type):
    li = []
    pattern = r"^\d\. (.*)"
    for m in re.findall(pattern, block, re.MULTILINE):
        leaf = convert_to_leafNodes(inline_markdown.text_to_textnodes(m))
        li.append(htmlnode.ParentNode("li", leaf))
    return htmlnode.ParentNode(block_type_map[block_type], li)


def block_to_hNode(block, block_type):
    count = 0
    while block[count] == "#":
        count += 1
    header = inline_markdown.text_to_textnodes(re.findall(r"#{1,6} (.*)", block)[0])
    leafNodes = convert_to_leafNodes(header)

    return htmlnode.ParentNode(block_type_map[block_type] + str(count), leafNodes)


def block_to_node(block):
    block_type = blocks.block_to_block_type(block)
    if block_type == blocks.block_type_paragraph:
        return block_to_paragraphNode(block, block_type)
    elif block_type == blocks.block_type_heading:
        return block_to_hNode(block, block_type)
    elif block_type == blocks.block_type_quote:
        return block_to_quoteNode(block, block_type)
    elif block_type == blocks.block_type_ulist:
        return block_to_ulNode(block, block_type)
    elif block_type == blocks.block_type_olist:
        return block_to_olNode(block, block_type)
    elif block_type == blocks.block_type_code:
        return block_to_codeNode(block, block_type)
    else:
        return htmlnode.HTMLNode()


# TODO: Need to make sure children for code blocks are within the code block.
# Currently children override the code block
# TODO: Surround ol & ul children with <li> tags.
def markdown_to_html_node(markdown):
    markdown_blocks = blocks.markdown_to_blocks(markdown)
    childNodes = []
    for markdown_block in markdown_blocks:
        node = block_to_node(markdown_block)
        childNodes.append(node)
    return htmlnode.ParentNode("div", childNodes, None)
