import subprocess
import os
import tempfile
import shutil

def run_bob(prompt: str, work_dir: str) -> str:
    bob_path = shutil.which("bob") or "bob"
    
    result = subprocess.run(
        [
            bob_path,
            "--yolo",
            "--chat-mode", "code",
            "--hide-intermediary-output",
            prompt
        ],
        capture_output=True,
        text=True,
        timeout=600,
        cwd=work_dir
    )
    
    return result.stdout + result.stderr

def collect_files(work_dir: str) -> dict:
    files = {}
    for root, dirs, filenames in os.walk(work_dir):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.bob']]
        for filename in filenames:
            filepath = os.path.join(root, filename)
            relpath = os.path.relpath(filepath, work_dir)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    files[relpath] = f.read()
            except:
                pass
    return files