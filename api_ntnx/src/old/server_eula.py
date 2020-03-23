import os, json, re
import ops_eula
import nutanix_serializer as ns
from server_base import *
from flask import Flask, jsonify, request

try:
  PORT = int(os.environ['PORT'])
  DEBUG = os.environ['DEBUG'].lower() == 'true'
except:
  PORT = 8082
  DEBUG = False
app = AppServer(PORT, DEBUG)

def api_eula():
  try:
    d = ns.Eula.loads(request.get_data().decode())
  except Exception as e:
    raise FormatException(str(e))
  check_credential(USER, PASSWORD, d)
  cluster = d['cluster']
  eula = d['eula']
  report_server = d['report_server']
  (task_uuid, set_status) = app.get_callbacks(report_server)  
  ops_eula.run(cluster, eula, set_status)
  return (jsonify({'uuid': task_uuid}), 200)

app.add_endpoint('/api/v1/run/', api_eula, ['POST'])
app.run()