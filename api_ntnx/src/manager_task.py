import hashlib
import redis
import uuid
import os
import pymongo
import schedule
import time
import threading

from util import *

DEBUG = True

def dprint(text):
  if DEBUG:
    print(text, flush=True)

def get_collections():
  client = pymongo.MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/',
    username=MONGO_USERNAME, password=MONGO_PASSWORD)
  col_task = client['task_manager']['task']
  col_progress = client['task_manager']['progress']
  col_cluster = client['api_cluster']['cluster']
  return col_task, col_progress, col_cluster
(COL_TASK, COL_PROGRESS, COL_CLUSTER) = get_collections()

def main():
  schedule.every(1).seconds.do(start_task)
  while True:
    try:
      schedule.run_pending()
      time.sleep(1)
    except Exception as e:
      print(e)

def start_task():
  try:
    #dprint('start_task()')
    task_dict = COL_TASK.find_one({'started':False}, {})
    if task_dict is None:
      return
    task_uuid = task_dict['uuid']
    COL_TASK.update_one({'uuid':task_uuid}, {'$set':{'started':True}})
  except Exception as e:
    dprint(e)
    COL_TASK.delete_one({'_id':task_dict['_id']})
    return

  try:
    del task_dict['_id']
    dprint(f'found task: {task_uuid}')
    task_type = task_dict['type']
    function_map = {
      'foundation': handle_foundation,
      'eula': handle_eula,
      'setup': handle_setup,
      'poweron': handle_poweron,
      'poweroff': handle_poweroff
    }
    if task_type not in function_map:
      raise Exception(f'task type "{task_type}" not found.')

    def thread_fun():
      fun = function_map[task_type]
      dprint(f'start task: {fun.__name__}')
      try:
        fun(copy.deepcopy(task_dict))
        COL_TASK.update_one({'uuid':task_uuid}, {'$set':{'finished':True}})
      except Exception as e:
        dprint(e)
        COL_TASK.update_one({'uuid':task_uuid}, {'$set':{'finished':True, 'failed':True}})

    t = threading.Thread(target=thread_fun)
    t.start()

  except Exception as e:
    dprint(e)
    COL_TASK.update_one({'uuid':task_uuid}, {'$set':{'finished':True, 'failed':True}})


def handle_foundation(task_dict):
  cluster_uuid = task_dict['cluster_uuid']
  cluster = COL_CLUSTER.find_one({'uuid': cluster_uuid}, {})
  if cluster is None:
    raise Exception(f'cluster "{cluster_uuid}" not found')

  d = {
    'cluster': cluster,
    'version': '',
    'hypervisor': '',
  }
  imaging_url = f'http://{API_FOUNDATION_HOST}:{API_FOUNDATION_PORT}/api/public/foundation/v1/imagings/'
  req = requests.post(imaging_url, data=json.dumps(d))
  if not req.ok:
    raise Exception('imaging request failed')
  foundation_task_uuid = req.json()['uuid']

  start_time = get_timestamp()
  while get_timestamp() - start_time < 7200:
    req = requests.get(imaging_url + foundation_task_uuid)
    if not req.ok:
      raise Exception('get imaging progress failed')

    imaging_progress = req.json()
    if imaging_progress['finished']:
      break
    time.sleep(15)

  d = {
    'uuid': str(uuid.uuid4()),
    'type': 'eula',
    'started': False,
    'failed': False,
    'completed': False,
    'create_timestamp': get_timestamp()
  }
  task_dict.update(d)
  COL_TASK.insert_one(task_dict)


def handle_eula(task):
  ...

def handle_setup(task):
  ...

def handle_poweron(task):
  ...

def handle_poweroff(task):
  ...

if __name__ == '__main__':
  main()