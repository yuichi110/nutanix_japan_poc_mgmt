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

@app.get("/api/public/cluster/v1/clusters/")
async def public_get_clusters(request: Request):
  cursol = COLLECTION.find({}, {'_id': False})
  return get_json(cursol)

@app.post("/api/public/cluster/v1/clusters/")
async def public_create_clusters(request: Request):
  try:
    #d = Cluster.loads(await request.json())
    d = await request.json()
    d['uuid'] = str(uuid.uuid4())
    COLLECTION.insert_one(d)
  except Exception as e:
    print(e)
    raise fastapi.HTTPException(status_code=400, detail='json format error')
  return {}

@app.delete("/api/public/cluster/v1/clusters/{cluster_uuid}")
async def public_get_clusters(request: Request, cluster_uuid:str):
  result = COLLECTION.delete_one({'uuid':cluster_uuid}, {'_id': False})
  if result.deleted_count == 0:
    raise fastapi.HTTPException(status_code=404, detail='cluster not found')
  return {}
