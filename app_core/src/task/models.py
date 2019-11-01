from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from common.errors import *

import uuid
import json

class Task(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)
  status = models.TextField(default='')
  parent_task = models.UUIDField(default=None, null=True)
  progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  failed = models.BooleanField(default=False)
  finished = models.BooleanField(default=False)
  creation_time = models.DateTimeField(auto_now_add=True)
  update_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return 'Name:{}, UUID:{}'.format(self.name, self.uuid)

  class Meta:
    ordering = ['-creation_time']

  def get_dict(self):
    d = {
      'uuid':          str(self.uuid),
      'name':          self.name,
      'status':        self.status,
      'parent_task':   str('' if self.parent_task is None else self.parent_task),
      'progress':      self.progress,
      'finished':      self.finished,
      'failed':        self.failed,
      'creation_time': str(self.creation_time).split('.')[0],
      'update_time':   str(self.update_time).split('.')[0]
    }
    return d

  @classmethod
  def exists(cls, task_uuid):
    return Task.objects.filter(uuid=task_uuid).exists()

  @classmethod
  def read(cls, task_uuid):
    task_object = Task.objects.filter(uuid=task_uuid)[0]
    return task_object.get_dict()

  @classmethod
  def read_all(cls):
    task_objects = Task.objects.all()
    task_list = [task_object.get_dict() for task_object in task_objects]
    return task_list

  @classmethod
  def create(cls, name):
    task_object = Task.objects.create(name=name)
    return task_object.get_dict()

  @classmethod
  def create_child(cls, name, parent_uuid):
    if not Task.objects.filter(uuid=parent_uuid).exists():
      raise Exception404('parent uuid does not exist')

    task_object = Task.objects.create(name=name, parent_task=parent_uuid)
    return task_object.get_dict()

  @classmethod
  def update(cls, task_uuid, json_text):
    try:
      update_dict = json.loads(json_text)
    except:
      raise Exception400('failed to parse json')

    task_object = Task.objects.filter(uuid=task_uuid)[0]
    if 'status' in update_dict:
      task_object.status = update_dict['status']
    cls.update_progress(task_object, update_dict)
    cls.update_failed(task_object, update_dict)
    task_object.save()

    return task_object.get_dict()

  @classmethod
  def update_progress(cls, task_object, update_dict):
    if 'progress' not in update_dict:
      return
    if task_object.failed:
      raise Exception400('unable to update progress on failed task')
    try:
      progress = int(update_dict['progress'])
      if progress < 0 or 100 < progress:
        raise Exception()
    except:
      raise Exception400('progress must be between 0-100')
    
    task_object.progress = progress
    if progress == 100:
      task_object.finished = True

  @classmethod
  def update_failed(self, task_object, update_dict):
    if 'failed' not in update_dict:
      return

    if not update_dict['failed']:
      raise Exception400('can not update to failed=false')

    child_tasks = Task.objects.filter(parent_task=str(task_object.uuid))
    for child_task in child_tasks:
      if child_task.finished:
        continue
      child_task.finished = True
      child_task.failed = True
      child_task.save()

    task_object.finished = True
    task_object.failed = True

  @classmethod
  def delete_(self, uuid):
    # childs
    childs = Task.objects.filter(parent_task=uuid)
    [child.delete() for child in childs]
    # itself
    task_object = Task.objects.filter(uuid=uuid)[0]
    task_object.delete()
    return {}