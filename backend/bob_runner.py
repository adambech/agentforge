import subprocess
import os
import tempfile
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bob_runner")

def run_bob(prompt: str, work_dir: str) -> str:
    bob_path = shutil.which("bob") or "bob"
    
    logger.info(f"Running bob in {work_dir} with timeout=1200s")
    
    try:
        result = subprocess.run(
            [
                bob_path,
                "--yolo",
                "--chat-mode", "code",
                prompt
            ],
            capture_output=True,
            text=True,
            timeout=1200,
            cwd=work_dir
        )
        logger.info(f"Bob completed with return code {result.returncode} (stdout: {len(result.stdout)} chars, stderr: {len(result.stderr)} chars)")
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        logger.warning(f"Bob timed out after 1200s in {work_dir}")
        raise

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