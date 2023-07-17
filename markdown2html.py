#!/usr/bin/python3
"""
Script that converts a Markdown file to HTML.
"""

import sys
import os
import re

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
    match = re.match(r'^\* (.+)', line)
    if match:
        item_text = match.group(1)
        return f"<li>{item_text}</li>"
    return line

def convert_ordered_list(line):
    """
    Converts a Markdown ordered list item to HTML.
    """
    match = re.match(r'^\d+\. (.+)', line)
    if match:
        item_text = match.group(1)
        return f"<li>{item_text}</li>"
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
    in_list = False
    for line in markdown_content:
        line = convert_heading(line)
        line = convert_unordered_list(line)
        line = convert_ordered_list(line)

        if line.startswith("<li>"):
            if not in_list:
                html_lines.append("<ol>\n")
                in_list = True
        else:
            if in_list:
                html_lines.append("</ol>\n")
                in_list = False

        html_lines.append(line)

    if in_list:
        html_lines.append("</ol>\n")

    html_content = ''.join(html_lines)

    # Save the HTML output to the output file
    with open(output_file, 'w') as f:
        f.write(html_content)

    sys.exit(0)
