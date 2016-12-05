import os
import subprocess 
from distutils.core import setup
from setuptools.command.install import install

class PostInstallCommand(install):
   
   def mv_properties():
      f = 'coretemp/coretemp.properties'
      os.rename(f, "/etc/%s" % f)

   def run(self):
      install.run(self)
   
setup(
   name = 'coretemp',
   packages = ['coretemp'],
   version = '0.1',
   install_requires=['pysensors','termcolor'],
   description = 'A simple service to monitor CPU temp',
   author = 'Matthew R McBride',
   author_email = 'mrmcbride@smcm.edu',
   url = 'https://github.com/mmcbride1/python-coretemp',
   download_url = 'https://github.com/mmcbride1/python-coretemp/tarball/0.1',
   keywords = ['cpu', 'monitor', 'service'],
   classifiers = []
   cmdclass = {'install': PostInstallCommand},
   entry_points = {
   'console_scripts': [
   'coretemp-monitor=monitor:cli',
  ],
 }
)
