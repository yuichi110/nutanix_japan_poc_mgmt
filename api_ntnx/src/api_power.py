import hashlib
import fastapi
import redis
import uuid
import os
import pymongo
from starlette.requests import Request
from starlette.responses import JSONResponse

from util import *
from nutanix_serializer import *

# REDIS
def get_redis():
  return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
REDIS = get_redis()

# MONGODB
def get_collection():
  client = pymongo.MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/',
    username=MONGO_USERNAME, password=MONGO_PASSWORD)
  col_cluster = client['api_cluster']['cluster']
  return col_cluster
COLLECTION = get_collection()

# FASTAPI
app = fastapi.FastAPI()

@app.post("/api/public/foundation/v1/image/")
async def public_get_clusters(request: Request):
  cursol = COLLECTION.find({}, {'_id': False})
  return get_json(cursol)

@app.post("/api/private/foundation/v1/image/")
async def public_get_clusters(request: Request):
  cursol = COLLECTION.find({}, {'_id': False})
  return get_json(cursol)
