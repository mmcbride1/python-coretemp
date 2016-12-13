#!/usr/bin/env python

import sys
import time
import threading as t
import sensor_reading as r
import coretemp_log as log
import coretemp_alert as alert
import coretemp_config as conf
from coretemp_daemon import Daemon
from coretemp_constants import INV_MSG

class CoretempExecutable(Daemon):

   # poll interval    
   POLL = 300

   # Main logs 
   ctlog = log.CoretempLog()
   exlog = log.ExceptionLog()

   def get_interval(self):
      """
      Get the configured 
      polling interval otherwise
      return default 
      """
      CONF = conf.Config("poll").get_config()
      try:
         inv = float(CONF['interval'])
         if inv < 5:
            return self.POLL
         else:
            return inv
      except ValueError:
         self.exlog.update_errlog(INV_MSG % self.POLL)
         return self.POLL    

   def run(self):
      """
      Run the daemon
      """
      inv = self.get_interval()
      while True:
         self.main_x()
         time.sleep(inv)

   def write_avg(self,read):
      """ 
      Helper function for
      getting mean value from sensor
      read and writing the output str
      :param SensorReading read: sensor read
      :return: core mean message to append
      """
      self.read = read
      core_avg = read.get_avg_read()
      return "\nCore Mean: %s\n" % core_avg

   def send(self,msg_):
      """ 
      Send the alert message where
      applicable
      :param str msg_: the message to send
      """
      self.msg_ = msg_
      ar = alert.Alert()
      ar.send_message(msg_)

   def monitor(self):
      """ 
      Post to the log file and
      send the alert message where
      applicable 
      """
      read = r.SensorReading()
      msg_ = read.get_message()

      if msg_:
         x = read.get_failed()
         msg_ += self.write_avg(read)
         msg_ += "==============================================="
         self.ctlog.update_templog(msg_)
         if x:
            d = t.Thread(name='ctm',target=self.send,args=(x,))
            d.setDaemon(True)
            d.start()

   def main_x(self):
      """
      Do monitor
      """
      try:
         self.monitor()
      except Exception as ex:
         self.exlog.update_errlog(ex)

def cli():
   """
   Entry point
   """
   PID = '/var/run/coretemp.pid'

   daemon = CoretempExecutable(PID)

   if len(sys.argv)  == 2:
      if   'start'   == sys.argv[1]:
         daemon.start()
      elif 'stop'    == sys.argv[1]:
         daemon.stop()
      elif 'restart' == sys.argv[1]:
         daemon.restart()
      elif 'status'  == sys.argv[1]:
         daemon.status()
      else:
         print "Unknown command"
         sys.exit(2)
         sys.exit(0)
   else:
      print "usage: %s start|stop|restart|status" % sys.argv[0]
      sys.exit(2)
