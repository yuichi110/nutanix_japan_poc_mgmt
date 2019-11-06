import os, json, re
import ops_eula
import nutanix_serializer as ns
from server_base import *
from flask import Flask, jsonify, request

try:
  PORT = int(os.environ['PORT'])
  USER = os.environ['USER']
  PASSWORD = os.environ['PASSWORD']
except:
  PORT = 8082
  USER = 'user'
  PASSWORD = 'password'

app = Flask('')

@app.route('/api/v1/run/', methods=['POST'])
def api_eula():
  try:
    try:
      d = ns.Eula.loads(request.get_data().decode())
    except Exception as e:
      raise FormatException(str(e))
    check_credential(USER, PASSWORD, d)
    cluster = d['cluster']
    eula = d['eula']
    report_server = d['report_server']
    ops_eula.run(cluster, eula, report_server)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

app.run(debug=False, host='0.0.0.0', port=PORT)