import zipfile
import io
from typing import Dict

def create_zip(files: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename, content in files.items():
            zf.writestr(filename, content)
    
    buffer.seek(0)
    return buffer.read()