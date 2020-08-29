import os
from dotenv import load_dotenv
load_dotenv()

CMKT_API_KEY = os.getenv("CMKT_API_KEY")
CMKT_SECRET = os.getenv("CMKT_SECRET")
PAXFUL_API_KEY = os.getenv("PAXFUL_API_KEY")
PAXFUL_SECRET = os.getenv("PAXFUL_SECRET")

