import os
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT_MANIFESTS = os.getenv("API_ENDPOINT_MANIFESTS")
API_ENDPOINT_TITLES = os.getenv("API_ENDPOINT_TITLES")
API_USER = os.getenv("API_USER")
API_PASSWORD = os.getenv("API_PASSWORD")
