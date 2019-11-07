from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from common.errors import *
from cluster.models import Cluster
from task.models import Task
import common.nutanix_serializer as ns

from uuid import UUID
import json
import os
import requests
import threading

try:
  MICRO_APP_USER = os.environ['MICRO_APP_USER']
  MICRO_APP_PASSWORD = os.environ['MICRO_APP_PASSWORD']
  APP_CORE_HOST = os.environ['APP_CORE_HOST']
  APP_CORE_PORT = int(os.environ['PORT'])
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
  APP_CORE_HOST = '127.0.0.1'
  APP_CORE_PORT = 8080
  APP_NTNX_FVM_HOST = '127.0.0.1'
  APP_NTNX_FVM_PORT = 8081
  APP_NTNX_EULA_HOST = '127.0.0.1'
  APP_NTNX_EULA_PORT = 8082
  APP_NTNX_SETUP_HOST = '127.0.0.1'
  APP_NTNX_SETUP_PORT = 8083
  APP_NTNX_POWER_HOST = '127.0.0.1'
  APP_NTNX_POWER_PORT = 8084
  print('set micro service env: fail')

CREDENTIAL = {
  'user': MICRO_APP_USER,
  'password': MICRO_APP_PASSWORD
}
APP_NTNX_FVM_URL = 'http://{}:{}/api/v1'.format(APP_NTNX_FVM_HOST, APP_NTNX_FVM_PORT)
APP_NTNX_EULA_URL = 'http://{}:{}/api/v1'.format(APP_NTNX_EULA_HOST, APP_NTNX_EULA_PORT)
APP_NTNX_SETUP_URL = 'http://{}:{}/api/v1'.format(APP_NTNX_SETUP_HOST, APP_NTNX_SETUP_PORT)
APP_NTNX_POWER_URL = 'http://{}:{}/api/v1'.format(APP_NTNX_POWER_HOST, APP_NTNX_POWER_PORT)

def get_report_server(task_uuid):
  d = {
    'send': True,
    'host': APP_CORE_HOST,
    'port': APP_CORE_PORT,
    'user': MICRO_APP_USER,
    'password': MICRO_APP_PASSWORD,
    'uuid': task_uuid
  }
  return d

class OpsApi:

  @classmethod
  def foundation(cls, request, uuid):
    try:
      cluster_uuid = uuid
      if request.method != 'POST':
        raise Exception405('this method is not allowed')
      if not Cluster.exists(cluster_uuid):
        raise Exception404("cluster uuid '{}' not found".format(cluster_uuid))
      cluster_json = Cluster.read(cluster_uuid)
      cluster_json['credential'] = CREDENTIAL
      cluster_name = j['cluster']['name']
      foundation_task_uuid = Task.create('foundation:' + cluster_name)['uuid']

      def fun():
        try:
          imaging_task_uuid = Task.create_child('foundation:' + cluster_name, 
            foundation_task_uuid)['uuid']
          eula_task_uuid = Task.create_child('foundation:' + cluster_name, 
            foundation_task_uuid)['uuid']
          setup_task_uuid = Task.create_child('foundation:' + cluster_name, 
            foundation_task_uuid)['uuid']

          # imaging
          cluster_json['report_server'] = get_report_server(imaging_task_uuid)
          body = ns.Foundation.dumps(cluster_json)
          response = requests.post(APP_NTNX_FVM_URL + '/image/', data=body)
          if not response.ok:
            raise Exception()
          wait_till_task_end(imaging_task_uuid)

          # eula
          cluster_json['report_server'] = get_report_server(eula_task_uuid)
          body = ns.Eula.dumps(cluster_json)
          response = requests.post(APP_NTNX_EULA_URL + '/run/', data=body)
          if not response.ok:
            raise Exception()
          wait_till_task_end(eula_task_uuid)

          # setup
          cluster_json['report_server'] = get_report_server(setup_task_uuid)
          body = ns.Setup.dumps(cluster_json)
          response = requests.post(APP_NTNX_SETUP_URL + '/run/', data=body)
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
  def power_up(cls, request, uuid):
    try:
      if request.method != 'POST':
        raise Exception405('this method is not allowed')
      if not Cluster.exists(uuid):
        raise Exception404("cluster uuid '{}' not found".format(uuid))

      task_uuid = Task.create('power up')['uuid']
      cluster_json = Cluster.read(uuid)
      cluster_json['credential'] = CREDENTIAL
      cluster_json['report_server'] = get_report_server(task_uuid)
      try:
        body = ns.Power.dumps(cluster_json)
        response = requests.post(APP_NTNX_POWER_URL + '/up/', data=body)
      except:
        response.ok = False
      if not response.ok:
        fail_task(task_uuid)

      d = {
        'uuid':task_uuid,
        'success':response.ok
      }
      return HttpResponse(json.dumps(d), content_type='application/json')

    except Exception as e:
      return get_error_response(e)

  @classmethod
  def power_down(cls, request, uuid):
    try:
      if request.method != 'POST':
        raise Exception405('this method is not allowed')
      if not Cluster.exists(uuid):
        raise Exception404("cluster uuid '{}' not found".format(uuid))
      task_uuid = Task.create('power down')['uuid']
      task_uuid = Task.create('power up')['uuid']
      cluster_json = Cluster.read(uuid)
      cluster_json['credential'] = CREDENTIAL
      cluster_json['report_server'] = get_report_server(task_uuid)
      try:
        body = ns.Power.dumps(cluster_json)
        response = requests.post(APP_NTNX_POWER_URL + '/down/', data=body)
      except:
        response.ok = False
      if not response.ok:
        fail_task(task_uuid)

      d = {
        'uuid':task_uuid,
        'success':response.ok
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
  d = {
    progress: 100
  }
  Task.update(task_uuid, json.dumps(d))

def fail_task(task_uuid):
  d = {
    failed: True
  }
  Task.update(task_uuid, json.dumps(d))
