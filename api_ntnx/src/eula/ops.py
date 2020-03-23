import json
import sys
import logging
import threading
import time
import os
import traceback
from eula.client import NutanixEulaClient

def eula(cluster, eula, set_status):
  def fun():
    a, b, c, d, e, f, g, h, i = 0, 0, 0, 0, 0, 0, 0, 0, 0
    progress = 0
    try:
      print('run: start')
      a = 1
      is_finished = False
      is_failed = False
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
      ops = EulaOps(cluster, eula)
      b = 1
      progress = 10
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
      ops.set_temporary_password()
      c = 1
      d = 1
      progress = 20
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
      ops.connect_to_prism()
      e = 1
      progress = 30
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
      ops.set_eula()
      f = 1
      progress = 50
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
      ops.set_initial_pulse()
      g = 1
      progress = 70
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
      ops.set_initial_alert()
      h = 1
      progress = 90
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
      ops.change_password()
      i = 1
      progress = 100
      is_finished = True
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
      print('run: end')
    except Exception as exception:
      print('failed with error: {}'.format(exception))
      progress = 100
      is_finished = True
      is_failed = True
      set_status(progress, get_eula_status(a, b, c, d, e, f, g, h, i), is_finished, is_failed)
  threading.Thread(target=fun).start()

def get_eula_status(a, b, c, d, e, f, g, h, i):
  s = {
    0: '',
    1: 'Done',
    2: 'Skip',
  }
  up_status = '''connecting to prism: {}
connected to prism: {}
set temporary password: {}
reconnecting to prism: {}
connected to prism: {}
set eula: {}
set initial pulse setting: {}
set initial alert setting: {}
change password: {}
'''
  return up_status.format(s[a], s[b], s[c], s[d], s[e], s[f], s[g], s[h], s[i])

class EulaOps:
  def __init__(self, cluster, eula):
    self.INITIAL_PASSWORD = 'nutanix/4u'
    self.TEMPORARY_PASSWORD = 'DevOpsTeam4Eva!'
    
    self.session =      None
    self.ip =           cluster['ip']
    self.user =         cluster['user']
    self.password =     cluster['password']

    self.eula_user =    eula['user']
    self.eula_company = eula['company']
    self.eula_title =   eula['title']
    self.enable_pulse = eula['enable_pulse']

  def set_temporary_password(self):
    print('set_temporary_password()')
    print('ip={}, initial_password={}, temporary_password={}'.format(
      self.ip, self.INITIAL_PASSWORD, self.TEMPORARY_PASSWORD))

    (success, result) = NutanixEulaClient.change_default_system_password(
      self.ip, self.INITIAL_PASSWORD, self.TEMPORARY_PASSWORD)
    if not success:
      error = 'failed to initialize prism password. reason "{}"'.format(result['error'])
      print(error)
      raise ErrorException(error)

  def connect_to_prism(self):
    print('connect_to_prism')
    print('ip={}, user={}, password={}'.format(self.ip, self.user, self.TEMPORARY_PASSWORD))
    try:
      self.session = NutanixEulaClient(self.ip, self.user, self.TEMPORARY_PASSWORD)
    except:
      error = "failed to connect to prism"
      print(error)
      raise ErrorException(error)

  def set_eula(self):
    print('set_eula()')
    print('user={}, company={}, title={}'.format(self.eula_user, self.eula_company, self.eula_title))
    (success, result) = self.session.set_eula(self.eula_user, self.eula_company, self.eula_title)
    if not success:
      error = "set eula failed. reason '{}'".format(result['error'])
      print(error)
      raise ErrorException(error)

  def set_initial_pulse(self):
    print('set_initial_pulse()')
    print('enable={}'.format(self.enable_pulse))
    (success, result) = self.session.set_initial_pulse_enable(self.enable_pulse)
    if not success:
      error = "set pulse failed. reason '{}'".format(result['error'])
      print(error)
      raise ErrorException(error)

  def set_initial_alert(self):
    print('set_initial_alert()')
    print('disable default nutanix email')
    (success, result) = self.session.disable_default_nutanix_email()
    if not success:
      error = "set alert failed. reason '{}'".format(result['error'])
      print(error)
      raise ErrorException(error)

  def change_password(self):
    print('change_password()')
    print('temporary_password={}, password={}'.format(self.TEMPORARY_PASSWORD, self.password))
    if self.password == self.TEMPORARY_PASSWORD:
      return

    (success, result) = self.session.change_password(self.TEMPORARY_PASSWORD, self.password)
    if not success:
      error = "change password failed. reason '{}'".format(result['error'])
      print(error)
      raise ErrorException(error)

class ErrorException(Exception):
  pass