import os, json, re
import ops_fvm
import nutanix_serializer as ns
from server_base import *
from flask import Flask, jsonify, request

try:
  PORT = int(os.environ['PORT'])
  USER = os.environ['USER']
  PASSWORD = os.environ['PASSWORD']
except:
  PORT = 8081
  USER = 'user'
  PASSWORD = 'password'

app = Flask('')

@app.route('/api/v1/check/', methods=['POST'])
def api_check():
  try:
    try:
      d = ns.Foundation.loads(request.get_data().decode())
    except Exception as e:
      raise FormatException(str(e))
    check_credential(USER, PASSWORD, d)
    fvm = d['fvm']
    cluster = d['cluster']
    nodes = d['nodes']
    basics = d['basics']
    foundation = d['foundation']
    report_server = d['report_server']
    ops_fvm.check(cluster, nodes, basics, fvm, foundation, report_server)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

@app.route('/api/v1/image/', methods=['POST'])
def api_image():
  try:
    try:
      d = ns.Foundation.loads(request.get_data().decode())
    except Exception as e:
      raise FormatException(str(e))
    check_credential(USER, PASSWORD, d)
    fvm = d['fvm']
    cluster = d['cluster']
    nodes = d['nodes']
    basics = d['basics']
    foundation = d['foundation']
    report_server = d['report_server']
    ops_fvm.image(cluster, nodes, basics, fvm, foundation, report_server)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

app.run(debug=False, host='0.0.0.0', port=PORT)
