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
import setup.ops as sops

# FASTAPI
app = fastapi.FastAPI()
task_dict = {}

@app.get("/api/public/setup/v1/setups/")
async def public_get_setups(request: Request):
  return task_dict

@app.get("/api/public/setup/v1/setups/{task_uuid}")
async def public_get_setup(request: Request, task_uuid):
  if task_uuid not in task_dict:
    raise fastapi.HTTPException(status_code=404, detail='task does not exist')
  return task_dict[task_uuid]

@app.post("/api/public/setup/v1/setups/")
async def public_start_setup(request: Request):
  try:
    d = await request.json()
    d = ns.Setup.loads(d)
    cluster = d['cluster']
    basics = d['basics']
    containers = d['containers']
    networks = d['networks']
    ipam_networks = d['ipam_networks']
    images = d['images']
  except Exception as e:
    print(e)
    raise fastapi.HTTPException(status_code=400, detail='json format error')

  task_uuid = str(uuid.uuid4())
  set_status = get_closure_set_status(task_dict, task_uuid)
  sops.setup(cluster, basics, containers, networks, ipam_networks, images, set_status)
  return {'uuid':task_uuid}
