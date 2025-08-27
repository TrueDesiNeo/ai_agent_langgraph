import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver

# -----------------------------
# Setup Logging Configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI")

if not mongodb_uri:
    logger.error("MONGODB_URI not found in environment variables.")
    raise ValueError("Missing MongoDB URI in .env file")

logger.info("Environment variables loaded successfully.")

# -----------------------------
# Define MongoDB Checkpoint Configuration
# -----------------------------
CHECKPOINT_DB_NAME = 'DB'
CHECKPOINT_COLLECTION_NAME = 'Blog_Chekpoint'
CHECKPOINT_WRITE_COLLECTION_NAME = 'Blog_Chekpoint_Write'
TTL_SECONDS = 300  # Time-to-live for checkpoint entries in seconds

logger.info("Checkpoint configuration set: DB=%s, Collection=%s, WriteCollection=%s, TTL=%d",
            CHECKPOINT_DB_NAME, CHECKPOINT_COLLECTION_NAME, CHECKPOINT_WRITE_COLLECTION_NAME, TTL_SECONDS)

# -----------------------------
# Initialize MongoDB Client
# -----------------------------
try:
    mongodb_client = MongoClient(mongodb_uri)
    logger.info("MongoDB client initialized successfully.")
except Exception as e:
    logger.exception("Failed to initialize MongoDB client.")
    raise

# -----------------------------
# Create MongoDBSaver Instance
# -----------------------------
try:
    mongodb_memory = MongoDBSaver(
        client=mongodb_client,
        db_name=CHECKPOINT_DB_NAME,
        checkpoint_collection_name=CHECKPOINT_COLLECTION_NAME,
        writes_collection_name=CHECKPOINT_WRITE_COLLECTION_NAME,
        ttl=TTL_SECONDS
    )
    logger.info("MongoDBSaver instance created successfully.")
except Exception as e:
    logger.exception("Failed to create MongoDBSaver instance.")
    raise