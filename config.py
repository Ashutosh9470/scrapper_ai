# config.py
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

# API key
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Search settings
TOP_N = int(os.getenv("TOP_N", 20))
KEYWORDS = [k.strip() for k in os.getenv(
    "KEYWORDS",
    "smart fan,bldc fan,energy saving fan"
).split(",") if k.strip()]

# Brand aliases & descriptions for semantic detection
BRAND_ALIASES = {
    "Atomberg": [
        "atomberg",
        "gorilla fan",
        "atomberg renesa",
        "atomberg studio",
        "atomberg bldc fan",
    ],
    "Havells": [
        "havells",
        "havells smart fan",
    ],
    "Crompton": [
        "crompton",
        "crompton smart fan",
        "crompton greaves",
    ],
    "Orient": [
        "orient",
        "orient electric",
    ],
    "Bajaj": [
        "bajaj",
        "bajaj fan",
    ],
    "Usha": [
        "usha",
        "usha fan",
    ],
}

BRAND_DESCRIPTIONS = {
    "Atomberg": "Atomberg BLDC smart energy saving ceiling fans, Gorilla fans brand",
    "Havells": "Havells ceiling fans and smart fans brand in India",
    "Crompton": "Crompton Greaves ceiling fans and smart fans",
    "Orient": "Orient Electric ceiling fans and smart fans brand",
    "Bajaj": "Bajaj ceiling fans and home appliances brand",
    "Usha": "Usha ceiling fans and home appliances brand",
}

BRANDS = list(BRAND_ALIASES.keys())
