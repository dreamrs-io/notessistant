import os
import re
from fs_utils import FsUtils
from datetime import datetime

# Read a Markdown file
file_path = '1.protocols/maintaining reading list.md'
markdown_content = FsUtils.read_markdown_file(file_path)
# print(markdown_content)
# print("==========")
lines = markdown_content.split('\n')
# print(len(lines))
updated_lines = ''
gpt_res = []
for index, line in enumerate(lines):
    # print(f"{index:03d}: {line}")
    if "#gpt-expand" in line:
        prompt = line.strip("-").strip("#gpt-expand").strip()
        print(f"==>[CallGPT]: {prompt}")
        res = FsUtils.call_chat_gpt(prompt)
        if res is not None:
            print(res)
            gpt_res.append(res.strip())
        
    updated_lines += f'{line}\n'
    
    if line.startswith('#') and 'Instances' in line and len(gpt_res) > 0:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_lines += f'- [#gpt-generated] {current_time}\n'
        for res_row in gpt_res:
            updated_lines += f'\t{res_row}\n'
    
# 写入 Markdown 文件
if updated_lines != '':
    current_date = datetime.now().strftime("%Y%m%d")
    new_file_name = file_path.replace(".md", f"_{current_date}.md")
    FsUtils.write_markdown_file(new_file_name, updated_lines)
    print(f'File saved to:{new_file_name}')

    