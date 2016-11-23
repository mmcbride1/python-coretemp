import re
import os
import sys
import subprocess 
import sensors as r
import coretemp_log as log
import coretemp_config as conf
from collections import OrderedDict

''' '''
from coretemp_constants import SUB_MAX_TYPE, SUB_CRT_TYPE, CHIP, NORM, HIGH, CRTC

class SensorReading:

   ''' '''
   crit = []
   high = []

   ''' '''
   MSG = ""

   ''' '''
   read = OrderedDict()

   ''' '''
   CONF = conf.Config("threshold").get_config()
   ERRO = log.ExceptionLog()

   def __init__(self):
      """ """
      try:
      except Exception as ex:
         ERRO.update_errlog(ex)

   def get_reading(self):
      """ """
      return self.read

   def get_message(self):
      """ """
      return self.MSG    

   def get_failed(self):
      """ """
      return re.sub(".*NORMAL.*\n?","",self.MSG)

   def __collect_default(self, sub):
      """ """
      self.sub = sub

      num = sub.get_value()   
      if sub.type == SUB_MAX_TYPE:
         self.high.append(num)
      if sub.type == SUB_CRT_TYPE:
         self.crit.append(num)

   def __avg(self, arr):
      """ """
      self.arr = arr
      
      try:
         avg = sum(arr)/float(len(arr)) 
         return round(avg, 2)
      except ZeroDivisionError as z:
         ERRO.update_errlog(z)
         return 0

   def get_avg_read(self):
      """ """
      return self.avg(self.read.values())
