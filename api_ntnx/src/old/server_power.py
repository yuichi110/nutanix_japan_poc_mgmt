import os, json, re
import ops_power
import nutanix_serializer as ns
from server_base import *
from flask import Flask, jsonify, request

try:
  PORT = int(os.environ['PORT'])
  DEBUG = os.environ['DEBUG'].lower() == 'true'
except:
  PORT = 8084
  DEBUG = False
app = AppServer(PORT, DEBUG)

def api_up():
  try:
    try:
      d = ns.Power.loads(request.get_data().decode())
    except Exception as e:
      raise FormatException(str(e))
    cluster = d['cluster']
    nodes = d['nodes']
    report_server = d['report_server']
    ops_power.up(cluster, nodes, report_server)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

def api_down():
  try:
    try:
      d = ns.Power.loads(request.get_data().decode())
    except Exception as e:
      raise FormatException(str(e))
    cluster = d['cluster']
    nodes = d['nodes']
    report_server = d['report_server']
    ops_power.down(cluster, nodes, report_server)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

app.add_endpoint('/api/v1/up/', api_up, ['POST'])
app.add_endpoint('/api/v1/down/', api_down, ['POST'])
app.run()