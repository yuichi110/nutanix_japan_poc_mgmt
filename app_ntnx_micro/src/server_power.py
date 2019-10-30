import os, json, re
import ops_power
from flask import Flask, jsonify, request

PORT = int(os.environ['PORT'])
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']

app = Flask('')

@app.route('/api/v1/up/', methods=['POST'])
def api_up():
  try:
    d = get_normalized_json(request.get_data().decode())
    ops_power.up(d)
    return (jsonify({}), 200)
  except Exception as e:
    return handle_error(e)

@app.route('/api/v1/up/', methods=['POST'])
def api_down():
  try:
    d = get_normalized_json(request.get_data().decode())
    ops_power.down(d)
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
      'ip':           d['ip'],
      'user':         d['user'],
      'password':     d['password'],
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