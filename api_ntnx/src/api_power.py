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
import power.ops as pops

# FASTAPI
app = fastapi.FastAPI()
task_dict = {}

@app.get("/api/public/power/v1/tasks/")
async def public_get_imagings(request: Request):
  return task_dict

@app.get("/api/public/power/v1/tasks/{task_uuid}")
async def public_get_imaging(request: Request, task_uuid):
  if task_uuid not in task_dict:
    raise fastapi.HTTPException(status_code=404, detail='task does not exist')
  return task_dict[task_uuid]

@app.post("/api/public/power/v1/on/")
async def public_on(request: Request):
  try:
    d = await request.json()
    d = ns.Power.loads(d)
    cluster = d['cluster']
    nodes = d['nodes']
  except Exception as e:
    print(e)
    raise fastapi.HTTPException(status_code=400, detail='json format error')

  task_uuid = str(uuid.uuid4())
  set_status = get_closure_set_status(task_dict, task_uuid)
  pops.on(cluster, nodes, set_status)
  return {'uuid':task_uuid}

@app.post("/api/public/power/v1/off/")
async def public_off(request: Request):
  try:
    d = await request.json()
    d = ns.Power.loads(d)
    cluster = d['cluster']
    nodes = d['nodes']
  except Exception as e:
    print(e)
    raise fastapi.HTTPException(status_code=400, detail='json format error')

  task_uuid = str(uuid.uuid4())
  set_status = get_closure_set_status(task_dict, task_uuid)
  pops.off(cluster, nodes, set_status)
  return {'uuid':task_uuid}
