import os
import redis
from langgraph.checkpoint.redis import RedisSaver

# Define your Redis URI
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Create Redis client 
redis_client = redis.Redis(host= REDIS_HOST, port= REDIS_PORT, db= REDIS_DB)

# Create Redis based checkpoint 
redis_checkpoint_saver = RedisSaver(redis_client= redis_client)
