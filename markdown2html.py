#!/usr/bin/python3
"""
Script that converts a Markdown file to HTML.
"""

import sys
import os
import re
import hashlib

def convert_heading(line):
    """
    Converts a Markdown heading line to HTML.
    """
    match = re.match(r'^(#+)\s(.+)', line)
    if match:
        level = len(match.group(1))
        heading_text = match.group(2)
        return f"<h{level}>{heading_text}</h{level}>\n"
    return line

def convert_unordered_list(line):
    """
    Converts a Markdown unordered list item to HTML.
    """
    match = re.match(r'^- (.+)', line)
    if match:
        item_text = match.group(1)
        return f"<li>{item_text}</li>"
    return line

def convert_ordered_list(line):
    """
    Converts a Markdown ordered list item to HTML.
    """
    match = re.match(r'^\* (.+)', line)
    if match:
        item_text = match.group(1)
        return f"<li>{item_text}</li>"
    return line

def convert_paragraph(line):
    """
    Converts a Markdown paragraph to HTML.
    """
    if line.strip():
        return f"<p>{line.strip()}</p>\n"
    return line

def convert_bold(line):
    """
    Converts bold syntax in Markdown to HTML.
    """
    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
    return line

def convert_md5(line):
    """
    Converts MD5 syntax in Markdown to HTML.
    """
    match = re.match(r'\[\[(.+?)\]\]', line)
    if match:
        content = match.group(1)
        md5_hash = hashlib.md5(content.encode()).hexdigest()
        return md5_hash
    return line

def convert_remove_characters(line):
    """
    Converts remove characters syntax in Markdown to HTML.
    """
    match = re.match(r'\(\((.+?)\)\)', line)
    if match:
        content = match.group(1)
        content = re.sub(r'c', '', content, flags=re.IGNORECASE)
        return content
    return line

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py <input_file> <output_file>\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    # Read the input Markdown file
    with open(input_file, 'r') as f:
        markdown_content = f.readlines()

    # Convert Markdown to HTML
    html_lines = []
    in_unordered_list = False
    in_ordered_list = False
    in_paragraph = False
    for line in markdown_content:
        line = convert_heading(line)

        if line.startswith("<li>"):
            if not in_unordered_list and not in_ordered_list:
                html_lines.append("<ul>\n")
                in_unordered_list = True
            line = convert_unordered_list(line)
            html_lines.append(line)
        elif line.startswith("<li>"):
            if not in_ordered_list and not in_unordered_list:
                html_lines.append("<ol>\n")
                in_ordered_list = True
            line = convert_ordered_list(line)
            html_lines.append(line)
        else:
            if in_unordered_list:
                html_lines.append("</ul>\n")
                in_unordered_list = False
            elif in_ordered_list:
                html_lines.append("</ol>\n")
                in_ordered_list = False
            line = convert_paragraph(line)
            line = convert_bold(line)
            line = convert_md5(line)  # Added MD5 conversion
            line = convert_remove_characters(line)  # Added remove characters conversion
            html_lines.append(line)

    if in_unordered_list:
        html_lines.append("</ul>\n")
    elif in_ordered_list:
        html_lines.append("</ol>\n")

    html_content = ''.join(html_lines)

    # Save the HTML output to the output file
    with open(output_file, 'w') as f:
        f.write(html_content)

    sys.exit(0)
