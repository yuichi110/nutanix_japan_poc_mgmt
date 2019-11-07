import json
import requests
from flask import jsonify

def check_credential(user, password, d):
  if d['credential']['user'] != user:
    raise AuthException('user not found')
  if d['credential']['password'] != password:
    raise AuthException('password invalid')

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

def send_report(report_server, progress, message):
  if not report_server['send']:
    return
  progress = int(progress)
  if progress < 0:
    print('progress must be <0')
    return
  if progress > 100:
    print('progress must be >100')
    return

  #print(progress)
  #print(message)

  try:
    url = 'http://{}:{}/api/v1/tasks/{}'.format(
      report_server['host'], report_server['port'], report_server['uuid'])
    d = {
      'user': report_server['user'],
      'password': report_server['password'],
      'progress': progress,
      'status': message
    }
    response = requests.put(url, data=json.dumps(d))
    if not response.ok:
      raise Exception('got failed response from report server. {}'.format(response.text))
  except Exception as e:
    print(e)

def send_fail_report(report_server, message):
  if not report_server['send']:
    return

  try:
    url = 'http://{}:{}/api/v1/tasks/{}'.format(
      report_server['host'], report_server['port'], report_server['uuid'])
    d = {
      'user': report_server['user'],
      'password': report_server['password'],
      'failed': True,
      'status': message
    }
    response = requests.post(url, data=json.dumps(d))
    if not response.ok:
      raise Exception('got failed response from report server. {}'.format(response.text))
  except Exception as e:
    print(e)

class AuthException(Exception):
  pass

class FormatException(Exception):
  pass