import os
import shutil
import subprocess
from setuptools import setup
from pkg_resources import resource_string
from setuptools.command.install import install

''' coretemp - setup.py '''

class PostInstallCommand(install):
   """ 
   Post installation command to
   copy the daemon properties file.    
   """

   def mv_properties(self):
      """ 
      Copy the properties file 
      to the conf directory.
      """
      f = '/coretemp/coretemp.properties'
      b = os.getcwd()
      shutil.copy2(b+f, '/etc/')

   def run(self):
      """ 
      Run (override).
      """
      self.mv_properties()
      install.run(self)

# setup # 
setup(
   name = 'coretemp',
   packages = ['coretemp'],
   version = '0.1',
   install_requires = [
    'pysensors >= 0.0.3',
    'termcolor >= 0.0.1',
   ],
   package_data = {'coretemp': ['*.properties']},
   description = 'lightweight service to monitor CPU temp',
   author = 'Matthew R McBride',
   author_email = 'mrmcbride@smcm.edu',
   url = 'https://github.com/mmcbride1/python-coretemp',
   classifiers = [],
   cmdclass = {'install': PostInstallCommand},
   entry_points = {
   'console_scripts': [
   'coretemp-monitor=coretemp.monitor:cli',
  ],
 }
)
