import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/'data'; GENERATED_DIR=BASE_DIR/'generated'
DATA_DIR.mkdir(exist_ok=True); GENERATED_DIR.mkdir(exist_ok=True)
load_dotenv(BASE_DIR/'.env')
MCP_API_KEY=os.getenv('MCP_API_KEY','change-me')
HOST=os.getenv('HOST','127.0.0.1'); PORT=int(os.getenv('PORT','8000'))
MAX_PAGES=int(os.getenv('MAX_PAGES','10')); REQUEST_TIMEOUT=float(os.getenv('REQUEST_TIMEOUT','15'))
