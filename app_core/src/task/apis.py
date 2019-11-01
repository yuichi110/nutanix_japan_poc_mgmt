from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from common.errors import *
from .models import Task

from uuid import UUID
import json

class TaskApi:

  @classmethod
  def tasks(cls, request):
    try:
      if request.method != 'GET':
        raise Exception405()
      json_text = json.dumps(Task.read_all())
      return HttpResponse(json_text, content_type='application/json')
    except Exception as e:
      return get_error_response(e)

  @classmethod
  def task(cls, request, uuid):
    def get():
      return json.dumps(Task.read(uuid))
      
    def put():
      return json.dumps(Task.update(uuid, request.body.decode()))

    def delete():
      return json.dumps(Task.delete_(uuid))

    try:
      if not Task.exists(uuid):
        raise Exception404()
      json_text = {'GET':get, 'PUT':put, 'DELETE':delete}.get(request.method, raise_exception405)()
      return HttpResponse(json_text, content_type='application/json')
    except Exception as e:
      return get_error_response(e)

  @classmethod
  def tests(cls, request):
    try:
      d = Task.create('parent')
      return HttpResponse(json.dumps(d), content_type='application/json')
    except Exception as e:
      return get_error_response(e)

  @classmethod
  def test(cls, request, uuid):
    try:
      d = Task.create_child('child', uuid)
      return HttpResponse(json.dumps(d), content_type='application/json')
    except Exception as e:
      return get_error_response(e)