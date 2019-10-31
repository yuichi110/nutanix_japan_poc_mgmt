from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from common.errors import *
from cluster.models import Cluster

from uuid import UUID
import json
import os
import requests
import threading

try:
  MICRO_APP_USER = os.environ['MICRO_APP_USER']
  MICRO_APP_PASSWORD = os.environ['MICRO_APP_PASSWORD']
  CREDENTIAL = {
    'user': MICRO_APP_USER,
    'password': MICRO_APP_PASSWORD
  }
  APP_NTNX_FVM_HOST = os.environ['APP_NTNX_FVM_HOST']
  APP_NTNX_FVM_PORT = int(os.environ['APP_NTNX_FVM_PORT'])
  APP_NTNX_EULA_HOST = os.environ['APP_NTNX_EULA_HOST']
  APP_NTNX_EULA_PORT = int(os.environ['APP_NTNX_EULA_PORT'])
  APP_NTNX_SETUP_HOST = os.environ['APP_NTNX_SETUP_HOST']
  APP_NTNX_SETUP_PORT = int(os.environ['APP_NTNX_SETUP_PORT'])
  APP_NTNX_POWER_HOST = os.environ['APP_NTNX_POWER_HOST']
  APP_NTNX_POWER_PORT = int(os.environ['APP_NTNX_POWER_PORT'])
  print('set micro service env: success')
except:
  MICRO_APP_USER = 'user'
  MICRO_APP_PASSWORD = 'password'
  CREDENTIAL = {
    'user': MICRO_APP_USER,
    'password': MICRO_APP_PASSWORD
  }
  APP_NTNX_FVM_HOST = '127.0.0.1'
  APP_NTNX_FVM_PORT = 8080
  APP_NTNX_EULA_HOST = '127.0.0.1'
  APP_NTNX_EULA_PORT = 8080
  APP_NTNX_SETUP_HOST = '127.0.0.1'
  APP_NTNX_SETUP_PORT = 8080
  APP_NTNX_POWER_HOST = '127.0.0.1'
  APP_NTNX_POWER_PORT = 8080
  print('set micro service env: fail')

APP_NTNX_FVM_URL = 'http://{}:{}/api/v1'.format(APP_NTNX_FVM_HOST, APP_NTNX_FVM_PORT)
APP_NTNX_EULA_URL = 'http://{}:{}/api/v1'.format(APP_NTNX_EULA_HOST, APP_NTNX_EULA_PORT)
APP_NTNX_SETUP_URL = 'http://{}:{}/api/v1'.format(APP_NTNX_SETUP_HOST, APP_NTNX_SETUP_PORT)
APP_NTNX_POWER_URL = 'http://{}:{}/api/v1'.format(APP_NTNX_POWER_HOST, APP_NTNX_POWER_PORT)

class OpsApi:

  @classmethod
  def foundation(cls, request, cluster_uuid):
    try:
      if request.method != 'POST':
        raise Exception405('this method is not allowed')
      if not Cluster.exists(cluster_uuid):
        raise Exception404("cluster uuid '{}' not found".format(cluster_uuid))
      j = Cluster.read(cluster_uuid)
      j['credential'] = CREDENTIAL
      cluster_name = j['cluster']['name']
      foundation_task_uuid = Task.create('foundation:' + cluster_name)

      def fun():
        tasks = [parent_task_uuid]
        try:
          # foundation
          imaging_task_uuid = Task.create_child('foundation:' + cluster_name, foundation_task_uuid)
          eula_task_uuid = Task.create_child('foundation:' + cluster_name, foundation_task_uuid)
          setup_task_uuid = Task.create_child('foundation:' + cluster_name, foundation_task_uuid)

          j['task_uuid'] = imaging_task_uuid
          response = requests.post(APP_NTNX_FVM_URL + '/image/', data=json.loads(j))
          if not response.ok:
            raise Exception()
          wait_till_task_end(imaging_task_uuid)
          # eula
          j['task_uuid'] = eula_task_uuid
          response = requests.post(APP_NTNX_EULA_URL + '/run/', data=json.loads(j))
          if not response.ok:
            raise Exception()
          wait_till_task_end(eula_task_uuid)
          # setup
          j['task_uuid'] = setup_task_uuid
          response = requests.post(APP_NTNX_SETUP_URL + '/run/', data=json.loads(j))
          if not response.ok:
            raise Exception()
          wait_till_task_end(setup_task_uuid)
          end_task(foundation_task_uuid)
        except Exception:
          fail_task(foundation_task_uuid)
      threading.Thread(target=fun).start()

      d = {
        'uuid':foundation_task_uuid
      }
      return HttpResponse(json.dumps(d), content_type='application/json')

    except Exception as e:
      return get_error_response(e)

  @classmethod
  def power_up(cls, request, cluster_uuid):
    try:
      if request.method != 'POST':
        raise Exception405('this method is not allowed')
      if not Cluster.exists(cluster_uuid):
        raise Exception404("cluster uuid '{}' not found".format(cluster_uuid))
      task_uuid = Task.create()
      j = Cluster.read(cluster_uuid)
      j['credential'] = CREDENTIAL
      j['task_uuid'] = task_uuid
      response = requests.post(APP_NTNX_POWER_URL + '/up/', data=json.loads(j))
      if not response.ok:
        fail_task(task_uuid)
      d = {
        'uuid':foundation_task_uuid
      }
      return HttpResponse(json.dumps(d), content_type='application/json')

    except Exception as e:
      return get_error_response(e)

  @classmethod
  def power_down(cls, request, cluster_uuid):
    try:
      if request.method != 'POST':
        raise Exception405('this method is not allowed')
      if not Cluster.exists(cluster_uuid):
        raise Exception404("cluster uuid '{}' not found".format(cluster_uuid))
      task_uuid = Task.create()
      j = Cluster.read(cluster_uuid)
      j['credential'] = CREDENTIAL
      j['task_uuid'] = task_uuid
      response = requests.post(APP_NTNX_POWER_URL + '/down/', data=json.loads(j))
      if not response.ok:
        fail_task(task_uuid)
      d = {
        'uuid':foundation_task_uuid
      }
      return HttpResponse(json.dumps(d), content_type='application/json')

    except Exception as e:
      return get_error_response(e)

def wait_till_task_end(task_uuid):
  failed = False
  error_count = 0
  while True:
    try:
      response = requests.get('/api/v1/tasks/' + task_uuid)
      if not response.ok:
        error_count += 1
        raise Exception()

      error_count = 0
      j = response.json()
      if j['progress'] == 100:
        return
      elif j['failed']:
        failed = True
        raise Exception()

      # wait and re check
    except:
      pass

    if failed:
      raise Exception()
    if error_count > 5:
      raise Exception()
    time.sleep(1)

def end_task(task_uuid):
  pass

def fail_task(task):
  pass
