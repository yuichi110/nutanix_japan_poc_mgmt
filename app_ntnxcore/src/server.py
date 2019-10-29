import os, json, re
import ops_eula
import ops_setup
from flask import Flask, jsonify, request

PORT = int(os.environ['PORT'])
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']

app = Flask('')

@app.route('/api/v1/eula/', methods=['POST'])
def api_eula():
  try:
    d = get_normalized_eula_json(request.get_data().decode())
    ops_eula.run(d)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

@app.route('/api/v1/setup/', methods=['POST'])
def api_setup():
  try:
    d = get_normalized_setup_json(request.get_data().decode())
    ops_setup.run(d)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

def get_normalized_eula_json(body):
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
      'ip':           d['ip'],
      'user':         d['user'],
      'password':     d['password'],
      'eula_name':    d['eula_name'],
      'eula_company': d['eula_company'],
      'eula_title':   d['eula_title'],
      'enable_pulse': d['enable_pulse'],
    }
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