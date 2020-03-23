import os, json, re
import ops_setup
import nutanix_serializer as ns
from server_base import *
from flask import Flask, jsonify, request

try:
  PORT = int(os.environ['PORT'])
  DEBUG = os.environ['DEBUG'].lower() == 'true'
except:
  PORT = 8083
  DEBUG = False
app = AppServer(PORT, DEBUG)

def api_setup():
  try:
    d = ns.Setup.loads(request.get_data().decode())
  except Exception as e:
    raise FormatException(str(e))
  check_credential(USER, PASSWORD, d)
  cluster = d['cluster']
  basics = d['basics']
  containers = d['containers']
  networks = d['networks']
  ipam_networks = d['ipam_networks']
  images = d['images']
  report_server = d['report_server']
  (task_uuid, set_status) = app.get_callbacks(report_server)
  ops_setup.run(cluster, basics, containers, networks, ipam_networks, images, set_status)
  return (jsonify({'uuid': task_uuid}), 200)

app.add_endpoint('/api/v1/run/', api_setup, ['POST'])
app.run()