import smtplib
import coretemp_log as log
import coretemp_config as conf

''' Import exception messages '''
from coretemp_constants import ARR_MSG, SND_MSG 

class Alert:

   ''' Monitor name '''
   MONITOR = "system-coretemp-monitor"

   ''' Server timeout '''
   TIMEOUT = 30

   ''' Configuration '''
   CONF = conf.Config("alert").get_config()
   ERRO = log.ExceptionLog() 

   def __init__(self):
      """ 
      Constructor:
      Initialize sender and receiver
      """
      try:
         self.s = self.CONF['fr_email']
         self.r = self.CONF['to_email'].split(",")
      except Exception as ex:
         self.ERRO.update_errlog(ARR_MSG % ex)

   def server(self):
      """
      Get the configured mail server
      :return: mail server
      """
      if not self.CONF['server']:
         return 'localhost'
      else:
         return self.CONF['server']

   def port(self):
      """
      Get configured port
      :return: port
      """
      try:
         port = int(self.CONF['port'])
      except:
         return 25
      else:
         return port

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

      port_ = self.port()
      serv_ = self.server()

      SEND = smtplib.SMTP(serv_,port_,self.TIMEOUT)

      try:
         for x in self.r:
            SEND.sendmail(self.s,x,self.message(self.r,msg))
      except Exception as ex:
         self.ERRO.update_errlog(SND_MSG % ex)
      SEND.quit()
