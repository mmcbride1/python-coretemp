import ConfigParser as cp

class Config:

   ''' Configuration dict '''
   conf = {}

   ''' Properties file '''
   CONF_FILE = "/etc/coretemp.properties"

   def __init__(self, sect):
      """ 
      Constructor takes a section argument 
      :param str sect: properties section
      """
      self.sect = sect
      self.__set_config(sect)

   def __set_config(self, sect):
      """ 
      Sets the configuration value to 
      the given section
      :param str sect: properties section
      """
      self.sect = sect
      config = cp.RawConfigParser()
      config.read(self.CONF_FILE)
      for k, v in config.items(sect):
         self.conf[k] = v

   def get_config(self):
      """ 
      Gets the configuration
      :return: the configuration dict
      """
      return self.conf
