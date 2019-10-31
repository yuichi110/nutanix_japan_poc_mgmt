from django.http import HttpResponse
import json
import traceback

def get_error_response(e):
  (code, description) = {
    Exception400:(400, 'bad request') ,
    Exception404:(404, 'resource not found'), 
    Exception405:(405, 'method not allowed')
  }.get(type(e), (500, 'server error'))
  d = {
    'code': code,
    'description': description,
    'message': str(e)
  }
  if code == 500:
    d['stack_trace'] = traceback.format_exc()

  json_text = json.dumps(d)
  print(json_text)
  return HttpResponse(json_text, content_type='application/json', status=code)

def raise_exception405():
  raise Exception405()

class Exception400(Exception):
  '''bad request'''
  pass

class Exception404(Exception):
  '''resource not found'''
  pass

class Exception405(Exception):
  '''method not allowed'''
  pass

