import sys
import os
sys.path.insert(0, '/app')
os.chdir('/app')

print("sys.path:", sys.path, flush=True)
print("files in /app:", os.listdir('/app'), flush=True)
print("files in /app/backend:", os.listdir('/app/backend'), flush=True)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=7860)