import re
from typing import Dict

def parse_bob_output(output: str) -> dict[str, str]:
    files = {}
    pattern = r'===\s*(.+?)\s*===\n(.*?)(?====\s*.+?\s*===|\Z)'
    matches = re.findall(pattern, output, re.DOTALL)
    
    for filename, content in matches:
        filename = filename.strip()
        content = content.strip()
        if filename and content:
            files[filename] = content
    
    return files

def extract_files_simple(output: str) -> dict[str, str]:
    files = {}
    lines = output.split('\n')
    current_file = None
    current_content = []
    
    for line in lines:
        if line.strip().startswith('===') and line.strip().endswith('==='):
            if current_file and current_content:
                files[current_file] = '\n'.join(current_content).strip()
            current_file = line.strip().replace('===', '').strip()
            current_content = []
        elif current_file is not None:
            current_content.append(line)
    
    if current_file and current_content:
        files[current_file] = '\n'.join(current_content).strip()
    
    return files