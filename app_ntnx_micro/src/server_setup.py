import os, json, re
import ops_setup
from flask import Flask, jsonify, request

PORT = int(os.environ['PORT'])
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']

app = Flask('')

@app.route('/api/v1/run/', methods=['POST'])
def api_setup():
  try:
    d = get_normalized_json(request.get_data().decode())
    ops_setup.run(d['cluster'], d['containers'], d['networks'], d['ipam_networks'], d['images'])
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

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
      'cluster': {
        'ip':           d['cluster']['ip'],
        'user':         d['cluster']['user'],
        'password':     d['cluster']['password'],
        'language':     d['cluster']['language']
      },
      'containers':[],
      'networks':[],
      'ipam_networks':[],
      'images':[],
    }

    for container in d['containers']:
      c = {
        'name': container['name']
      }
      nd['containers'].append(c)

    for network in d['networks']:
      n = {
        'name': network['name'],
        'vlan': int(network['vlan'])
      }
      nd['networks'].append(n)

    for ipam_network in d['ipam_networks']:
      n = {
        'name': ipam_network['name'],
        'vlan': int(ipam_network['vlan']),
        'network': ipam_network['network'],
        'prefix': int(ipam_network['prefix']),
        'gateway': ipam_network['gateway'],
        'dns': ipam_network['dns'],
        'pools': []
      }
      for pool in ipam_network['pools']:
        p = {
          'from': pool['from'],
          'to':   pool['to']
        }
        n['pools'].append(p)
      nd['ipam_networks'].append(n)

    for image in d['images']:
      d = {
        'name': image['name'],
        'container': image['container'],
        'url': image['url']
      }
      nd['images'].append(image)

  except Exception as e:
    raise FormatException(str(e))

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