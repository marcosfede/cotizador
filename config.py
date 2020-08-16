import os
from dotenv import load_dotenv
load_dotenv()

CMKT_API_KEY = os.getenv("CMKT_API_KEY")
CMKT_SECRET = os.getenv("CMKT_SECRET")
