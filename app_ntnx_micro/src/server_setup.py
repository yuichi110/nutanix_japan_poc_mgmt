import os, json, re
import ops_setup
import nutanix_serializer as ns
from server_base import *
from flask import Flask, jsonify, request

try:
  PORT = int(os.environ['PORT'])
  USER = os.environ['USER']
  PASSWORD = os.environ['PASSWORD']
except:
  PORT = 8083
  USER = 'user'
  PASSWORD = 'password'

app = Flask('')

@app.route('/api/v1/run/', methods=['POST'])
def api_setup():
  try:
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
    ops_setup.run(cluster, basics, containers, networks, ipam_networks, images, report_server)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

app.run(debug=False, host='0.0.0.0', port=PORT)