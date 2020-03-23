import requests
import json

PORT = 80
PUBLIC_CLUSTER_API = f'http://127.0.0.1:{PORT}/api/public/cluster/v1/'
PUBLIC_TASK_API = f'http://127.0.0.1:{PORT}/api/public/task/v1/'

def main():
  cluster = get_clusters()[0]
  cluster_uuid = cluster['uuid']
  create_foundation_task(cluster_uuid)

def get_clusters():
  res = requests.get(PUBLIC_CLUSTER_API + 'clusters/')
  return res.json()

def create_foundation_task(cluster_uuid):
  d = {
    'cluster_uuid': cluster_uuid
  }
  res = requests.post(PUBLIC_TASK_API + 'foundation_tasks/', data=json.dumps(d))
  return res.json()

if __name__ == '__main__':
  main()