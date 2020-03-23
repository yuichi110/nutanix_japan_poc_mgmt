import hashlib
import redis
import uuid
import os
import pymongo
import schedule
import time

'''
def get_collection():
  client = pymongo.MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/',
    username=MONGO_USERNAME, password=MONGO_PASSWORD)
  col_user = client['api_foundation']['task']
  return col_user
COLLECTION = get_collection()
'''

def main():
  schedule.every(1).seconds.do(handle_foundation_task)
  schedule.every(1).seconds.do(handle_eula_task)
  schedule.every(1).seconds.do(handle_setup_task)
  schedule.every(1).seconds.do(handle_power_task)

  while True:
    try:
      schedule.run_pending()
      time.sleep(1)
    except Exception as e:
      print(e)

def handle_foundation_task():
  time.sleep(5)
  print(datetime.datetime.now())

def handle_setup_task():
  ...

def handle_eula_task():
  ...

def handle_power_task():
  ...

if __name__ == '__main__':
  main()