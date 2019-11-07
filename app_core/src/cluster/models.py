from django.db import models
from django.core.exceptions import ValidationError
from common.errors import *
import common.nutanix_serializer as ns

import uuid
import json

class Cluster(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100, unique=True)
  data = models.TextField()

  def __str__(self):
    return 'NAME:{}, UUID:{}'.format(self.name, self.uuid)

  @classmethod
  def exists(cls, cluster_uuid):
    return Cluster.objects.filter(uuid=cluster_uuid).exists()

  @classmethod
  def create(cls, json_text):
    d = ns.Cluster.loads(json_text)
    name = d['cluster']['name']
    if Cluster.objects.filter(name=name).exists():
      raise Exception400('same name cluster already exist')

    cluster_object = Cluster.objects.create(name=d['cluster']['name'], data='')
    d['uuid'] = str(cluster_object.uuid)
    cluster_object.data = json.dumps(d, indent=2)
    cluster_object.save()
    return d

  @classmethod
  def read(cls, cluster_uuid):
    cluster_object = Cluster.objects.filter(uuid=cluster_uuid)[0]
    return json.loads(cluster_object.data)

  @classmethod
  def read_all(cls):
    cluster_objects = Cluster.objects.all()
    cluster_list = [json.loads(cluster_object.data) for cluster_object in cluster_objects]
    return cluster_list

  @classmethod
  def update(cls, cluster_uuid, json_text):
    cluster_object = Cluster.objects.filter(uuid=cluster_uuid)[0]
    d = ns.Cluster.loads(json_text)
    new_name = d['cluster']['name']
    if new_name != cluster_object.name:
      if Cluster.objects.filter(name=new_name).exists():
        raise Exception400('same name cluster already exist')

    d['uuid'] = str(cluster_uuid)
    cluster_object.name = new_name
    cluster_object.data = json.dumps(d, indent=2)
    cluster_object.save()
    return d

  @classmethod
  def delete_(cls, cluster_uuid):
    cluster_object = Cluster.objects.filter(uuid=cluster_uuid)[0]
    cluster_object.delete()
    return {}
