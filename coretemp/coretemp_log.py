import os
import logging
from datetime import datetime

class CoretempLog:

   ''' Max file size '''
   MAX_SIZE_KB = 1000 * 100

   ''' Log file '''
   LOG_FILE = "/var/log/coretemp.log"

   def __get_size(self, f):
      """ 
      Gets the current size of
      the log file if it exist
      :param str f: Log file
      :return: size in bytes    
      """
      self.f = f
      return os.path.getsize(f)

   def __format_message(self, read):
      """ 
      Formats the log message str
      to include required information
      :param str read: A sensor reading 
      :return: formatted log message    
      """
      self.read = read
      
      name = "coretemp-reading"
      head = "%s - %s : \n%s"
      return head % (datetime.now(), name, read)

   def update_templog(self, msg):
      """ 
      Writes to the coretemp log.
      Recycles the log file if
      threshold is met
      :param str msg: log message to append
      """
      self.msg = msg
      
      logf = self.LOG_FILE    
      if os.path.isfile(logf):
         size = self.__get_size(logf)
         if size > self.MAX_SIZE_KB:
            os.remove(logf)
      with open(logf, "a") as log:
         log.write(self.__format_message(msg) + "\n")

class ExceptionLog:

   ''' Log file '''
   LOG_FILE = "/var/log/coretemp_error.log"

   ''' Log format '''
   FORMAT = '%(asctime)-15s %(user)-8s - %(message)s'

   ''' Log object '''
   LOGGER = logging.getLogger("coretemp_monitor")

   def update_errlog(self, msg):
      """ 
      Append message to error log
      :param str msg: message to append
      """
      self.msg = msg

      out = "Coretemp Monitor Notice: %s"

      d = {'user':'coretemp'}
      h = logging.FileHandler(self.LOG_FILE)
      f = logging.Formatter(self.FORMAT)
      h.setFormatter(f)

      self.LOGGER.addHandler(h)
      self.LOGGER.error(out, msg, extra=d)
