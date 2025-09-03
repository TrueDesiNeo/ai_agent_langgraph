import os
import redis
from langgraph.checkpoint.redis import RedisSaver
import logging

# -------------------- Setup Logging --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Redis Configuration --------------------
# Define Redis connection parameters
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
SESSION_TTL = 1  # TTL in minute
REDIS_DB = int(os.getenv("REDIS_DB", 0))  # Default to DB 0 if not set
logger.info("Connecting to Redis at %s:%d (DB: %d)", REDIS_HOST, REDIS_PORT, REDIS_DB)

# Create Redis client instance
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# -------------------- TTL Configuration --------------------
# TTL (Time-To-Live) settings for checkpoints
ttl_config = {
    "default_ttl": SESSION_TTL,  # TTL in minutes (e.g., 1 minute)
    "refresh_on_read": True,  # Extend TTL on each read
}
logger.info("TTL configuration set: %s", ttl_config)

# -------------------- Initialize RedisSaver --------------------
# Create a RedisSaver instance for LangGraph checkpointing
redis_checkpoint_saver = RedisSaver(redis_client=redis_client, ttl=ttl_config)
logger.info("Redis checkpoint saver initialized.")