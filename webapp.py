import logging
import os
import subprocess


from fastapi import FastAPI, HTTPException

app = FastAPI()

log_file_dir = os.getenv("LOG_FILE_DIR")
if not log_file_dir:
    raise ValueError("Environment variable LOG_FILE_DIR is missing")

log_file_path = os.path.join(log_file_dir, "log.log")
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

commands = [
    "echo 'Starting process'",
    "rm -rf /tmp/test-dir",
    "mkdir /tmp/test-dir",
    "touch /tmp/test-dir/file1.txt",
    "ls -lah /tmp/test-dir",
    "rm -rf /tmp/test-dir",
    "mkdir /tmp/test-dir",
    "touch /tmp/test-dir/file1.txt",
    "echo H >> /tmp/test-dir/file1.txt",
    "echo E >> /tmp/test-dir/file1.txt",
    "echo L >> /tmp/test-dir/file1.txt",
    "echo L >> /tmp/test-dir/file1.txt",
    "echo O >> /tmp/test-dir/file1.txt",
    "cat /tmp/test-dir/file1.txt"
]


def exec_command(command):
    result = subprocess.run(["bash", "-c", command], capture_output=True, text=True)
    rc = result.returncode
    stdout = result.stdout.replace("\n\n", "\n")
    stderr = result.stderr.replace("\n\n", "\n")
    return stdout, stderr, rc


def generate_log():
    for c in commands:
        stdout, stderr, rc = exec_command(c)
        logger.info(f"Executing '{c}'")
        logger.info(f"RC: '{rc}'")
        logger.info(f"OUTPUT: \n{stdout if stdout else stderr if stderr else None}")
        if rc != 0:
            return False
    return True


@app.post("/execute")
def execute():
    try:
        result = generate_log()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
