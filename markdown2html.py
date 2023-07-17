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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
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
    html_lines = [convert_heading(line) for line in markdown_content]
    html_content = ''.join(html_lines)

    # Save the HTML output to the output file
    with open(output_file, 'w') as f:
        f.write(html_content)

    sys.exit(0)
