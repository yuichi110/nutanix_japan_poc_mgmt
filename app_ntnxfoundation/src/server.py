import os, json, re
import ops_foundation
from flask import Flask, jsonify, request

PORT = int(os.environ['PORT'])
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']

app = Flask('')

@app.route('/api/v1/check/', methods=['POST'])
def api_check():
  try:
    d = get_normalized_json(request.get_data().decode())
    ops_foundation.check(d['fvm'], d['cluster'], d['aos_version'], d['report_server'])
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

@app.route('/api/v1/image/', methods=['POST'])
def api_image():
  try:
    d = get_normalized_json(request.get_data().decode())
    ops_foundation.image(d['fvm'], d['cluster'], d['aos_version'], d['report_server'])
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

'''
@app.route('/api/v1/abort/', methods=['POST'])
def api_abort():
  body = request.get_data().decode().strip()
  ops_foundation.abort()
  return success(data) 
'''

def get_normalized_json(body):
  try:
    d = json.loads(body)
  except Exception as e:
    raise FormatException(str(e))

  try:
    d['user']
    d['password']
  except Exception as e:
    raise FormatException(str(e))

  if d['user'] != USER:
    raise AuthException('user name wrong')
  if d['password'] != PASSWORD:
    raise AuthException('password is wrong')

  try:
    nd = {
      'report_server': {
        'send':     d['report_server']['send'],
        'host':     d['report_server']['host'],
        'user':     d['report_server']['user'],
        'password': d['report_server']['password']
      },

      'cluster': {
        'name':        d['cluster']['name'],
        'netmask':     d['cluster']['netmask'],
        'gateway':     d['cluster']['gateway'],
        'external_ip': d['cluster']['external_ip'],
        'ntp_server':  d['cluster']['ntp_server'],
        'name_server': d['cluster']['name_server'],
        # nodes
      },
      'fvm' : {
        # ips 
        "user":     d['fvm']["user"],
        "password": d['fvm']["password"],
        # nos_packages
      },
      "aos_version": d["aos_version"]
    }

    # nodes
    nodes = []
    for node in d['cluster']['nodes']:
      nnode = {
        "host_name": node["host_name"],
        "position":  node["position"],
        "ipmi_mac":  node["ipmi_mac"],
        "ipmi_ip":   node["ipmi_ip"],
        "host_ip":   node["host_ip"],
        "cvm_ip":    node["cvm_ip"],
      }
      nodes.append(nnode)
    nd['cluster']['nodes'] = nodes
    # ips
    ips = []
    for ip in d['fvm']['ips']:
      ips.append(ip)
    nd['fvm']['ips'] = ips
    # nos_packages
    nos_packages = {}
    for (key, value) in d['fvm']['nos_packages'].items():
      nos_packages[key] = value 
    nd['fvm']['nos_packages'] = nos_packages
  except Exception as e:
    raise FormatException(str(e))

  if nd["aos_version"] not in nd['fvm']['nos_packages']:
    raise FormatException('aos version not in fvm nos packages.')

  return nd

def handle_error(e):
  print(e)
  if isinstance(e, AuthException):
    d = {'error': "user name or password is invalid."}
    return (jsonify(d), 403)
  if isinstance(e, FormatException):
    d = {'error': "json body has problem. reason '{}'".format(e)}
    return (jsonify(d), 400)
  d = {'error': "unexpected error. reason '{}'".format(e)}
  return (jsonify(d), 500) 

class AuthException(Exception):
  pass

class FormatException(Exception):
  pass

app.run(debug=False, host='0.0.0.0', port=PORT)

'''
Sample JSON

{
  "report_server": {
    "send": True
    "host": "hostname",
    "user": "username",
    "password": "password"
  },

  "cluster": {
    "name" : "poc02",
    "netmask":"255.255.128.0",
    "gateway":"10.149.0.1",
    "ntp_server":"ntp.nict.jp",
    "name_server":"8.8.8.8",
    "external_ip":"10.149.2.41",
    "nodes":[
      {
        "host_name":"AHV-1",
        "position":"A",
        "ipmi_mac":"00:25:90:d6:05:24",
        "ipmi_ip":"10.149.2.11",
        "host_ip":"10.149.2.21",
        "cvm_ip":"10.149.2.31"
      },
      {
        "host_name":"AHV-2",
        "position":"B",
        "ipmi_mac":"00:25:90:d6:05:9e",
        "ipmi_ip":"10.149.2.12",
        "host_ip":"10.149.2.22",
        "cvm_ip":"10.149.2.32"
      },
      {
        "host_name":"AHV-3",
        "position":"C",
        "ipmi_mac":"00:25:90:d6:05:26",
        "ipmi_ip":"10.149.2.13",
        "host_ip":"10.149.2.23",
        "cvm_ip":"10.149.2.33"
      },
      {
        "host_name":"AHV-4",
        "position":"D",
        "ipmi_mac":"0c:c4:7a:45:e3:c4",
        "ipmi_ip":"10.149.2.14",
        "host_ip":"10.149.2.24",
        "cvm_ip":"10.149.2.34"
      }
    ]
  },

  "fvm": {
    "ips" : [
      "10.149.0.5",
      "10.149.0.6"
    ],
    "user" : "nutanix",
    "password" : "nutanix/4u",
    "nos_packages" : {
      "5.10.2" : "nutanix_installer_package-release-euphrates-5.10.2-stable.tar"
    }
  },

  "aos_version": "5.10.2"
}
'''