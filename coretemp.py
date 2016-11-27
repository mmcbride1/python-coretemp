import sys
import time
import coretemp_log as log
import sensor_reading as r
import coretemp_alert as alert 

''' Main logs '''
ctlog = log.CoretempLog()
exlog = log.ExceptionLog()

def write_avg(read):
   """ 
   Helper function for
   getting mean value from sensor
   read and writing the output str
   :param SensorReading read: sensor read
   :return: core mean message to append
   """
   core_avg = read.get_avg_read()
   return "\nCore Mean: %s\n" % core_avg

def send(msg_):
   """ 
   Send the alert message where
   applicable
   :param str msg_: the message to send
   """
   ar = alert.Alert()
   ar.send_message(msg_)

def monitor():
   """ 
   Post to the log file and
   send the alert message where
   applicable 
   """
   read = r.SensorReading()
   msg_ = read.get_message()
 
   if msg_:
      x = read.get_failed()
      msg_ += write_avg(read)
      msg_ += "==============================================="
      ctlog.update_templog(msg_)
      if x:
         send(x)

def main():
   """ 
   Main
   """
   try:
      monitor()
   except Exception as ex:
      exlog.update_errlog(ex)

if __name__ == "__main__":
   while True:
      main()
      time.sleep(120)
