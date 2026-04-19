# Loads configuration from the .env file
import os
from dotenv import load_dotenv

# Reads the .env file and loads the variables into the envirnoment
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")