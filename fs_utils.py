import re
import requests

api_key = "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"
class FsUtils:
    @staticmethod
    def read_markdown_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()
        
    def write_markdown_file(file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)
            print(f'Write down: {file_path}')
            
    def parse_markdown_sections_1(content):
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

    def parse_markdown_sections(content):
        sections = {}
        current_section = ""
        lines = content.split('\n')
        for index, line in enumerate(lines):
            if line.startswith("#"):
                # Start of a new section
                if current_section:
                    # Extract the title
                    title = line.strip("#").strip()
                    title = re.sub(r"[^a-zA-Z0-9\s]", "", title).lower()
                    sections[title] = current_section.strip()
                current_section = ""
            else:
                # Add line to the current section
                current_section += line + '\n'
        # Add the last section
        if current_section:
            sections["Untitled"] = current_section.strip()
        return sections
    
    def call_openai(prompt):
        api_endpoint = "https://api.openai.com/v1/completions"
        request_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        }
        request_data = {
            "model": "text-davinci-003",
            "prompt": f"{prompt}",
            "max_tokens": 500,
            "temperature": 0.5
        }
        response = requests.post(api_endpoint, headers=request_headers, json=request_data)
        if response.status_code == 200:
            response_text = response.json()["choices"][0]["text"]
        else:
            print(f"Request failed with status code: {str(response.status_code)}")
            response_text = None
        return response_text;
    
    def call_chat_gpt(prompt):
        api_endpoint = "https://api.openai.com/v1/chat/completions"
        request_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        }
        request_data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post(api_endpoint, headers=request_headers, json=request_data)
        if response.status_code == 200:
            response_text = response.json()["choices"][0]["message"]["content"]
        else:
            print(f"Request failed with status code: {str(response.status_code)}")
            print(response.json())
            response_text = None
        return response_text;