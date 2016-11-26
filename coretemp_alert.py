import smtplib
import coretemp_log as log
import coretemp_config as conf

''' Import exception messages '''
from coretemp_constants import ARR_MSG, SND_MSG 

class Alert:

   ''' Monitor name '''
   MONITOR = "system-coretemp-monitor"

   ''' Send object '''
   SEND = smtplib.SMTP('localhost')

   ''' Configuration '''
   CONF = conf.Config("alert").get_config()
   ERRO = log.ExceptionLog() 

   def __init__(self):
      """ 
      Constructor:
      Initialize sender and receiver
      """
      try:
         self.s = CONF['fr_email']
         self.r = CONF['to_email'].split(",")
      except Exception as ex:
         ERRO.update_errlog(ARR_MSG % ex)

   def message(self, to, msg):
      """ 
      Build the email alert 
      :param str to: email to receive alert 
      :param str msg: base message 
      :return: email to send
      """
      self.to = to
      self.msg = msg

      return """ 
      From: %s <%s>
      To: <%s>
      Subject: Coretemp Notification!

      %s      
      """ % (self.MONITOR, self.s, to, msg)

   def send_message(self, msg):
      """ 
      Send the alert message 
      :param str msg: alert message 
      """
      self.msg = msg 

      try:
         for x in self.r:
            self.SEND.sendmail(self.s,x,self.message(r,msg))
      except Exception as ex:
         log.update_errlog(SND_MSG % ex)
