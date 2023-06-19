import os
import markdown


def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        markdown_content = file.read()
    return markdown_content


def write_markdown_file(file_path, markdown_content):
    with open(file_path, 'w') as file:
        file.write(markdown_content)


def process_markdown_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)
                markdown_content = read_markdown_file(file_path)

                # Modify the markdown_content as needed
                # For example, let's convert all headings to uppercase
                html_content = markdown.markdown(markdown_content)
                modified_html_content = html_content.upper()
                modified_markdown_content = markdown.markdown(modified_html_content, output_format='markdown')

                write_markdown_file(file_path, modified_markdown_content)


# Specify the folder path containing the Markdown files
folder_path = '/path/to/markdown/folder'

# Process the Markdown files in the folder
process_markdown_files(folder_path)
