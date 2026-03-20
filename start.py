import sys
import os
sys.path.insert(0, '/app')
os.chdir('/app')

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=7860)