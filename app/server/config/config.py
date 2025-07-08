import logging
import os
from dotenv import load_dotenv
from tools.get_order_status import get_order_status
from websocket.websocket import BaseWebSocketServer

# Load environment variables for API keys
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Project Configuration
PROJECT_ID = "dara_ai_assistant_companion"

# API Configuration
VERTEX_API = True  # Set to true to use Vertex AI endpoint
LOCATION = "us-central1"  # Required when VERTEX_API=true

# Model Configuration
MODEL = "gemini-2.0-flash-live-preview-04-09"
VOICE_NAME = "Orus"
# Gemini TTS models support the following 30 voice options in the voice_name field:
# Zephyr: Bright, Puck: Upbeat, Charon: Informative, Kore: Firm, 
# Fenrir: Excitable, Leda: Youthful, Orus: Firm, Aoede: Breez

# API Keys (loaded from environment variables)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Optional - only needed for dev endpoint (VERTEX_API=false)
MEM0_API_KEY = os.getenv("MEM0_API_KEY")  # Required for Mem0 long-term memory functionality

# Audio sample rates for input/output
RECEIVE_SAMPLE_RATE = 24000  # Rate of audio received from Gemini
SEND_SAMPLE_RATE = 16000     # Rate of audio sent to Gemini

# Load system instruction from file
SYSTEM_INSTRUCTION_PATH = os.path.join(os.path.dirname(__file__), "system_instruction.txt")
with open(SYSTEM_INSTRUCTION_PATH, "r", encoding="utf-8") as f:
    SYSTEM_INSTRUCTION = f.read()




