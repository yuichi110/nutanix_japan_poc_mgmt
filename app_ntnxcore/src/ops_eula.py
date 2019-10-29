import json
import sys
import logging
import threading
import time
import os
import traceback
from nutanix_eula_client import NutanixEulaClient

def run(fvm, eula):
  def fun():
    try:
      ops = EulaOps(eula)
      ops.set_temporary_password()
      ops.connect_to_prism()
      ops.set_eula()
      ops.set_initial_pulse()
      ops.set_initial_alert()
      ops.change_password()
    except Exception as e:
      print(e)
  threading.Thread(target=fun).start()

class EulaOps:
  def __init__(self, eula):
    self.INITIAL_PASSWORD = 'nutanix/4u'
    self.TEMPORARY_PASSWORD = 'DevOpsTeam4Eva!'
    
    self.session =      None
    self.ip =           eula['ip']
    self.user =         eula['user']
    self.password =     eula['password']
    self.eula_name =    eula['eula_name']
    self.eula_company = eula['eula_company']
    self.eula_title =   eula['eula_title']
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
    print('name={}, company={}, title={}'.format(self.eula_name, self.eula_company, self.eula_title))
    (success, result) = self.session.set_eula(self.eula_name, self.eula_company, self.eula_title)
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