from django.db import models
from django.core.exceptions import ValidationError
from common.errors import *

import uuid
import json

class Fvm(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100, unique=True)
  data = models.TextField()

  def __str__(self):
    return 'NAME:{}, UUID:{}'.format(self.name, self.uuid)

  @classmethod
  def exists(cls, cluster_uuid):
    return Fvm.objects.filter(uuid=cluster_uuid).exists()

  @classmethod
  def read(cls, cluster_uuid):
    vvm_object = Fvm.objects.filter(uuid=cluster_uuid)[0]
    return json.loads(fvm_object.data)

  @classmethod
  def read_all(cls):
    fvm_objects = Fvm.objects.all()
    fvm_list = [json.loads(fvm_object.data) for fvm_object in fvm_objects]
    return fvm_list