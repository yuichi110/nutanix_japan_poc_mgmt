import os, json, re
import ops_fvm
import nutanix_serializer as ns
from server_base import *
from flask import Flask, jsonify, request

try:
  PORT = int(os.environ['PORT'])
  DEBUG = os.environ['DEBUG'].lower() == 'true'
except:
  PORT = 8081
  DEBUG = False
app = AppServer(PORT, DEBUG)

def api_check():
  try:
    text_json = request.get_data().decode()
    d = ns.Foundation.loads(text_json)
  except Exception as e:
    raise FormatException(str(e))
  fvm = d['fvm']
  cluster = d['cluster']
  nodes = d['nodes']
  basics = d['basics']
  foundation = d['foundation']
  report_server = d.get('report_server', {})
  (task_uuid, set_status) = app.get_callbacks(report_server)
  ops_fvm.check(cluster, nodes, basics, fvm, set_status)
  return (jsonify({'uuid': task_uuid}), 200)

def api_image():
  try:
    d = ns.Foundation.loads(request.get_data().decode())
  except Exception as e:
    raise FormatException(str(e))
  fvm = d['fvm']
  cluster = d['cluster']
  nodes = d['nodes']
  basics = d['basics']
  foundation = d['foundation']
  report_server = d.get('report_server', {})
  (task_uuid, set_status) = app.get_callbacks(report_server)
  ops_fvm.image(cluster, nodes, basics, fvm, foundation, set_status)
  return (jsonify({'uuid': task_uuid}), 200)

app.add_endpoint('/api/v1/check/', api_check, ['POST'])
app.add_endpoint('/api/v1/image/', api_image, ['POST'])
app.run()
