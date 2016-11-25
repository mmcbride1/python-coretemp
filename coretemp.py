import sys
import time
import coretemp_log as log
import sensor_reading as r
import coretemp_alert as alert 

''' '''
read = r.SensorReading()

''' '''
msg = read.get_message()

''' '''
ctlog = log.CoretempLog()
exlog = log.ExceptionLog()

def write_avg():
   """ """
   core_avg = read.get_avg_read()
   return "\nCore Mean: %s\n" % core_avg

def send(_msg):
   """ """
   ar = alert.Alert()
   ar.send_message(_msg)

def monitor(_msg):
   """ """
   if _msg:
      x = read.get_failed()
      _msg += write_avg()
      ctlog.update_templog(_msg)
      if x:
         send(x)

def main(_msg):
   """ """
   try:
      monitor(_msg)
   except Exception as ex:
      exlog.update_errlog(ex)

if __name__ == "__main__":
   while True:
      main(msg)
      time.sleep(120)
