import os, json, re
import ops_power
import nutanix_serializer as ns
from server_base import *
from flask import Flask, jsonify, request

try:
  PORT = int(os.environ['PORT'])
  USER = os.environ['USER']
  PASSWORD = os.environ['PASSWORD']
except:
  PORT = 8084
  USER = 'user'
  PASSWORD = 'password'

app = Flask('')

@app.route('/api/v1/up/', methods=['POST'])
def api_up():
  try:
    try:
      d = ns.Power.loads(request.get_data().decode())
    except Exception as e:
      raise FormatException(str(e))
    check_credential(USER, PASSWORD, d)
    cluster = d['cluster']
    nodes = d['nodes']
    report_server = d['report_server']
    ops_power.up(cluster, nodes, report_server)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

@app.route('/api/v1/down/', methods=['POST'])
def api_down():
  try:
    try:
      d = ns.Power.loads(request.get_data().decode())
    except Exception as e:
      raise FormatException(str(e))
    check_credential(USER, PASSWORD, d)
    cluster = d['cluster']
    nodes = d['nodes']
    report_server = d['report_server']
    ops_power.down(cluster, nodes, report_server)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

app.run(debug=False, host='0.0.0.0', port=PORT)