import os
import re
from fs_utils import FsUtils
from datetime import datetime

# Read a Markdown file
current_dir = '1.protocols/'
file_path = f'{current_dir}maintaining reading list.md'
markdown_content = FsUtils.read_markdown_file(file_path)
# print(markdown_content)
# print("==========")
lines = markdown_content.split('\n')
# print(len(lines))
is_milestone = False
updated_lines = ''
gpt_res = []
goal = ''
update_file = False
for index, line in enumerate(lines):
    # print(f"{index:03d}: {line}")
    if line.startswith('*goal'):
        goal = line.strip('*')[5:].strip()
        print(f"==>[Goal]: {goal}")
        
    # read milestones
    if line.startswith('## '):
        is_milestone = 'Milestones' in line

    if is_milestone:
        if "#gpt-expand" in line:
            prompt = ''
            if goal != '':
                prompt += f'{goal}\n'
            prompt += line.strip("-").strip("#gpt-expand").strip()
            print(f"==>[CallGPT]: {prompt}")
            res = FsUtils.call_chat_gpt(prompt)
            if res is not None:
                update_file = True
                print(res)
                gpt_res.append(res.strip())
        # read line
        if '[[' in line:
            links = re.findall(r'\[\[(.*?)\]\]', line)
            if len(links) > 0:
                link_file = links[0]
                if '.' not in link_file:
                    link_file += '.md'
                link_file = current_dir + link_file
                print(f"==>[Link]:{link_file}")
                # read linked file
                linked_file_content = FsUtils.read_markdown_file(link_file)
                rows = linked_file_content.split('\n')
                call_gpt_script = False
                is_row_milestone = False
                row_prompt = ''
                gpt_generated = ''
                for i, row in enumerate(rows):
                    # check #gpt-script tag
                    if row.startswith('# ') and '#gpt-script' in row:
                        call_gpt_script = True
                        # read milestones
                    if row.startswith('## '):
                        is_row_milestone = 'Milestones' in row
                    if is_row_milestone and 'Milestones' not in row:
                        row_prompt += f'{row}\n'
                        
                if row_prompt != '':
                    script_prompt = 'Write python script for following content. Provide only code, no text.\n'
                    script_prompt += row_prompt
                    print(f"==>[CallGPT]: {script_prompt}")
                    script_res = FsUtils.call_chat_gpt(script_prompt)
                    if script_res is not None:
                        # only py code
                        script_path = '6.codes/' + datetime.now().strftime("%Y%m%d") + '.py'
                        with open(script_path, "w") as file:
                            file.write(script_res)
                        print(f'Script saved to:{script_path}')
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        gpt_generated = f'![Script](../{script_path}) #gpt-generated {current_time}'
                
                if gpt_generated:
                    with open(link_file, "a") as file:
                        file.write(gpt_generated)
        
    updated_lines += f'{line}\n'
    
    if line.startswith('## ') and 'Instances' in line and len(gpt_res) > 0:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_lines += f'- [#gpt-generated] {current_time}\n'
        for res_row in gpt_res:
            updated_lines += f'\t{res_row}\n'
    
# 写入 Markdown 文件
if update_file and updated_lines != '':
    current_date = datetime.now().strftime("%Y%m%d")
    new_file_name = file_path.replace(".md", f"_{current_date}.md")
    FsUtils.write_markdown_file(new_file_name, updated_lines)
    print(f'File saved to:{new_file_name}')

    