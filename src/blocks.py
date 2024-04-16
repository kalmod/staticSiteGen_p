import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"


def markdown_to_blocks(markdown):
    filtered_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


# Let's tackle these one by one.
def block_to_block_type(block):
    pattern = r"(^\#{1,6} )"
    if len(re.findall(pattern, block)) == 1:
        return block_type_heading
    pattern = r"(^```[\w\W]*?```$)"
    if len(re.findall(pattern, block)) == 1:
        return block_type_code
    pattern = r"(^[*-].*)"
    lines = block.split("\n")
    if len(re.findall(pattern, block, re.MULTILINE)) == len(lines):
        return block_type_ulist
    pattern = r"(^>.*)"
    if len(re.findall(pattern, block, re.MULTILINE)) == len(lines):
        return block_type_quote
    pattern = r"(^[*-].*)"
    if len(re.findall(pattern, block, re.MULTILINE)) == len(lines):
        return block_type_ulist
    pattern = r"(^\d\. .*)"
    if len(re.findall(pattern, block, re.MULTILINE)) == len(lines):
        current = int(lines[0][0])
        if current != 1:
            return block_type_paragraph
        for i in range(1, len(lines)):
            next = int(lines[i][0])
            if current + 1 != next:
                return block_type_paragraph
            current = next
        return block_type_olist

    return block_type_paragraph
