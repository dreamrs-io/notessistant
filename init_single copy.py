import os
import re


def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def write_markdown_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def modify_markdown_file(file_path, modification_func):
    content = read_markdown_file(file_path)
    modified_content = modification_func(content)
    write_markdown_file(file_path, modified_content)


def add_header(content, header_text, header_level=1):
    header = '#' * header_level
    modified_content = f'{header} {header_text}\n\n{content}'
    return modified_content


def replace_text(content, pattern, replacement):
    modified_content = re.sub(pattern, replacement, content)
    return modified_content

def parse_markdown_sections(content):
    sections = []
    current_section = ""
    lines = content.split('\n')
    for line in lines:
        if line.startswith("#"):
            # Start of a new section
            if current_section:
                sections.append(current_section.strip())
            current_section = line
        else:
            # Add line to the current section
            current_section += '\n' + line
    if current_section:
        sections.append(current_section.strip())
    return sections
# Example usage:


# Read a Markdown file
file_path = '1.protocols/maintaining reading list.md'
markdown_content = read_markdown_file(file_path)
print(markdown_content)
print("==========")

# 解析Markdown文件内容为分段
sections = parse_markdown_sections(markdown_content)

# 打印每个分段
for index, section in enumerate(sections):
    print(f"Section {index+1}:")
    print(section)
    print("--------------------")
    
# Modify the content by adding a header
# modified_content = add_header(
#     markdown_content, 'Modified Example', header_level=2)

# Write the modified content back to the file
# write_markdown_file('example.md', modified_content)

# Modify the file using a custom modification function


def custom_modification(content):
    # Replace all occurrences of 'Hello' with 'Hi'
    modified_content = replace_text(content, r'Hello', 'Hi')
    return modified_content


# modify_markdown_file('example.md', custom_modification)
