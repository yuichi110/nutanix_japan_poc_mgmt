from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid
import json

class Task(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)
  data = models.TextField()
  parent_task = models.UUIDField(default=None)
  progress = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
  failed = models.BooleanField(default=False)
  complete = models.BooleanField(default=False)
  creation_time = models.DateTimeField(auto_now_add=True)
  update_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return 'Name:{}, UUID:{}'.format(self.name, self.uuid)

  class Meta:
    ordering = ['-creation_time']

  def get_dict(self):
    d = {
      'uuid':str(self.uuid),
      'name':self.name,
      'status':self.data,
      'is_complete':self.is_complete,
      'creation_time':str(self.creation_time).split('.')[0],
      'update_time':str(self.update_time).split('.')[0]
    }
    return d

  @classmethod
  def exists(cls, uuid):
    return Task.objects.filter(uuid=uuid).exists()

  @classmethod
  def read(cls, uuid):
    task_object = Task.objects.filter(uuid=uuid)[0]
    return task_object.get_dict()

  @classmethod
  def read_all(cls):
    task_objects = Task.objects.all()
    task_list = [task_object.get_dict() for task_object in task_objects]
    return task_list

  @classmethod
  def create(cls, name):
    return {}

  @classmethod
  def create_child(self, name, parent_uuid):
    return {}

  @classmethod
  def update(self, uuid, json_text):
    return {}

  @classmethod
  def update_progress(self, uuid, progress):
    return {}

  @classmethod
  def update_failed(self, uuid, failed):
    return {}

  @classmethod
  def delete_(self, uuid):
    # childs
    childs = Task.objects.filter(parent_task=uuid)
    [child.delete() for child in childs]
    # itself
    task_object = Task.objects.filter(uuid=uuid)[0]
    task_object.delete()
    return {}