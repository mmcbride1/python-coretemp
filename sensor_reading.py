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
      try:
      except Exception as ex:
         ERRO.update_errlog(ex)
