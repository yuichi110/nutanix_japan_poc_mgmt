import hashlib
import fastapi
import redis
import uuid
import os
import pymongo
import datetime
from starlette.requests import Request
from starlette.responses import JSONResponse

from util import *
from nutanix_serializer import *

# REDIS
def get_redis():
  return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
REDIS = get_redis()

# MONGODB
def get_collections():
  client = pymongo.MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/',
    username=MONGO_USERNAME, password=MONGO_PASSWORD)
  col_task = client['task_manager']['task']
  col_progress = client['task_manager']['progress']
  col_cluster = client['api_cluster']['cluster']
  return col_task, col_progress, col_cluster
COL_TASK, COL_PROGRESS, COL_CLUSTER = get_collections()

# FASTAPI
app = fastapi.FastAPI()

@app.get("/api/public/task/v1/tasks/")
async def public_get_tasks(request: Request):
  cursol = COL_TASK.find({}, {'_id': False})
  return get_json(cursol)

@app.get("/api/public/task/v1/tasks/{task_uuid}")
async def public_get_task(request: Request, task_uuid:str):
  cursol = COL_TASK.find({}, {'_id': False})
  return get_json(cursol)

@app.post("/api/public/task/v1/foundation_tasks/")
async def public_create_task(request: Request):
  try:
    d = await request.json()
  except Exception as e:
    print(e)
    raise fastapi.HTTPException(status_code=400, detail='json format error')
  if COL_CLUSTER.find_one({'uuid': d['cluster_uuid']}, {}) is None:
    raise fastapi.HTTPException(status_code=400, detail='non register cluster uuid is provided')
  create_task(d, 'foundation')
  return {}

@app.get("/api/public/task/v1/progress/{task_uuid}")
async def public_get_progress(request: Request, task_uuid):
  cursol = COL_PROGRESS.find({}, {'_id': False})
  return get_json(cursol)

def create_task(task_dict, task_type):
  if task_type not in {'foundation', 'eula', 'setup', 'poweron', 'poweroff'}:
    print(f'Error: not supported task "{task_type}"')
    raise fastapi.HTTPException(status_code=500, detail='internal error')

  d = {
    'uuid': str(uuid.uuid4()),
    'type': task_type,
    'started': False,
    'failed': False,
    'completed': False,
    'create_timestamp': get_timestamp()
  }
  task_dict.update(d)
  COL_TASK.insert_one(task_dict)