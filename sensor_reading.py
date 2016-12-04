import re
import os
import sys
import subprocess 
import sensors as r
import coretemp_log as log
import coretemp_config as conf
from collections import OrderedDict

''' Get sensor constants '''
from coretemp_constants import SUB_MAX_TYPE, SUB_CRT_TYPE, CHIP, NORM, HIGH, CRTC

class SensorReading:

   ''' Store sensor threshold '''
   crit = []
   high = []

   ''' Store log message '''
   MSG = ""

   ''' Store sensor reading '''
   read = OrderedDict()

   ''' Configuration '''
   CONF = conf.Config("threshold").get_config()
   ERRO = log.ExceptionLog()

   def __init__(self):
      """ 
      Constructor:
      Set chip reading and log
      message    
      """
      try:
         self.__set_chip_read()
         self.__set_message()
      except Exception as ex:
         self.ERRO.update_errlog(ex)

   def get_reading(self):
      """ 
      Get sensor reading 
      :return: sensor reading 
      """
      return self.read

   def get_message(self):
      """ 
      Get log message    
      :return: log message string
      """
      return self.MSG    

   def get_failed(self):
      """ 
      Get readings only deemed 
      as high or critical from
      the primary reading 
      :return: max/crt message string
      """
      return re.sub(".*NORMAL.*\n?","",self.MSG)

   def __collect_recommended(self, sub):
      """ 
      Gets the recommended threshold
      values as determined by the
      sensor sub-feature set
      :param str sub: the given sub-feature 
      """
      self.sub = sub

      num = sub.get_value()   
      if sub.type == SUB_MAX_TYPE:
         self.high.append(num)
      if sub.type == SUB_CRT_TYPE:
         self.crit.append(num)

   def __avg(self, arr):
      """ 
      Obtains the mean value
      of the collection
      :param list arr: any given list 
      :return: average value 
      """
      self.arr = arr
      
      try:
         avg = sum(arr)/float(len(arr)) 
         return round(avg, 2)
      except ZeroDivisionError as z:
         self.ERRO.update_errlog(z)
         return 0

   def get_avg_read(self):
      """ 
      Gets the average core value 
      of the list of chips on the
      read
      :return: average core value 
      """
      return self.__avg(self.read.values())

   def __msg_str(self, k, v, i):
      """ 
      Helper function to 
      build the log output message 
      :param str k: core #
      :param str v: reading 
      :param str i: indicator 
      :return: formatted log message 
      """
      self.k = k
      self.v = v
      self.i = i

      return "%s : %s -> %s\n" % (k, v, i)

   def __set_defaults(self, arr):
      """ 
      Sets default values for
      the thresholds in the case that
      none are provided in the config and
      a reading cannot be obtained from 
      the chip
      :param list arr: generated threshold list 
      :return: updated list with defaults 
      """
      self.arr = arr
      
      for k, v in arr.items():
         if k is 'MAX' and v == 0:
            arr[k] = 86.0
         if k is 'CRT' and v == 0:
            arr[k] = 96.0
      return arr

   def get_threshold(self):
      """ 
      The primary threshold setting
      mechanism. Sets first from the 
      config then next from the recommended
      values if no such properties exist 
      :return: dict containing max/crt values 
      """
      h = self.CONF['high']
      c = self.CONF['crit']

      if h is "" or float(h) <= 0:
         h = self.__avg(self.high)
      if c is "" or float(c) <= 0:
         c = self.__avg(self.crit)

      order = [float(h),float(c)]

      high = min(order)
      crit = max(order)

      return {'MAX':high,'CRT':crit}

   def __set_chip_read(self):
      """ 
      Queries the chip applies result 
      to the 'read' dict. Then, collects the 
      recommended threshold values 
      """
      r.init()
      try:
         for x in r.iter_detected_chips(CHIP):
            for f in x:
               if "Core" in f.label:
                  self.read[f.label] = f.get_value()
                  for sub in f:
                     self.__collect_recommended(sub)
      finally:
         r.cleanup() 

   def __set_message(self):
      """ 
      Builds the output (log) message 
      based on the standing of the chip 
      read and whether given thresholds 
      were reached 
      """
      th = self.__set_defaults(self.get_threshold())

      for k, v in self.get_reading().items():
         if v < th['MAX']:
            self.MSG += self.__msg_str(k,v,NORM)
         elif v >= th['MAX'] and v < th['CRT']:
            self.MSG += self.__msg_str(k,v,HIGH)
         elif v >= th['CRT']:
            self.MSG += self.__msg_str(k,v,CRTC)
         else:
            self.MSG += self.__msg_str(k,v,"UNKNOWN")
