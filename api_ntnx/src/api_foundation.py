import hashlib
import fastapi
import redis
import uuid
import os
import pymongo
from starlette.requests import Request
from starlette.responses import JSONResponse

from util import *
import nutanix_serializer as ns
import foundation.ops as fops

'''
# REDIS
def get_redis():
  return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
REDIS = get_redis()
'''

# FASTAPI
app = fastapi.FastAPI()
task_dict = {}

@app.get("/api/public/foundation/v1/imagings/")
async def public_get_imagings(request: Request):
  return task_dict

@app.get("/api/public/foundation/v1/imagings/{task_uuid}")
async def public_get_imaging(request: Request, task_uuid):
  if task_uuid not in task_dict:
    raise fastapi.HTTPException(status_code=404, detail='task does not exist')
  return task_dict[task_uuid]

@app.post("/api/public/foundation/v1/imagings/")
async def public_start_imaging(request: Request):
  try:
    d = await request.json()
    d = ns.Foundation.loads(d)
    fvm = d['fvm']
    cluster = d['cluster']
    nodes = d['nodes']
    basics = d['basics']
    foundation = d['foundation']
  except Exception as e:
    print(e)
    raise fastapi.HTTPException(status_code=400, detail='json format error')

  task_uuid = str(uuid.uuid4())
  set_status = get_closure_set_status(task_dict, task_uuid)
  fops.image(cluster, nodes, basics, fvm, foundation, set_status)
  return {'uuid':task_uuid}
