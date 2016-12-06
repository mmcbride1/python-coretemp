import os
import shutil
import subprocess 
from setuptools import setup    
from setuptools.command.install import install

class PostInstallCommand(install):
   
   def mv_properties():
      b = 'coretemp/'
      f = 'coretemp.properties'
      shutil.copy2(b + f, '/etc/')

   def run(self):
      install.run(self)
   
setup(
   name = 'coretemp',
   packages = ['coretemp'],
   version = '0.1.3',
   install_requires = [
    'pysensors >= 0.0.3',
    'termcolor >= 0.0.1',
   ],
   description = 'A simple service to monitor CPU temp',
   author = 'Matthew R McBride',
   author_email = 'mrmcbride@smcm.edu',
   url = 'https://github.com/mmcbride1/python-coretemp',
   classifiers = [],
#   cmdclass = {'install': PostInstallCommand},
   data_files = [('/etc', ['coretemp.properties'])],
   entry_points = {
   'console_scripts': [
   'coretemp-monitor=monitor:cli',
  ],
 }
)
