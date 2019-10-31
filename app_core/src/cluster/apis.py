from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from .models import Cluster
from common.errors import *

from uuid import UUID
import json

class ClusterApi:

  @classmethod
  def clusters(cls, request):
    def get():
      return json.dumps(Cluster.read_all())

    def post():
      return json.dumps(Cluster.create(request.body.decode()))

    try:
      json_text = {'GET':get, 'POST':post}.get(request.method, raise_exception405)()
      return HttpResponse(json_text, content_type='application/json')
    except Exception as e:
      return get_error_response(e)

  @classmethod
  def cluster(cls, request, uuid):
    def get():
      return json.dumps(Cluster.read(uuid))
      
    def put():
      return json.dumps(Cluster.update(uuid, request.body.decode()))

    def delete():
      return json.dumps(Cluster.delete_(uuid))

    try:
      if not Cluster.exists(uuid):
        raise Exception404("cluster uuid '{}' not found".format(uuid))
      json_text = {'GET':get, 'PUT':put, 'DELETE':delete}.get(request.method, raise_exception405)()
      return HttpResponse(json_text, content_type='application/json')
    except Exception as e:
      return get_error_response(e)
