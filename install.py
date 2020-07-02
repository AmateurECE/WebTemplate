###############################################################################
# NAME:             install.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Installation script for the template.
#
# CREATED:          07/01/2020
#
# LAST EDITED:      07/01/2020
###

import argparse
import configparser
import subprocess
import os

pkApplicationName = 'application-name'
pkAuthorName = 'author-name'
pkDescription = 'description'
pkContainerName = 'container-name'
pkNetworkName = 'network-name'
pkRootDirectory = 'root-directory'
pkConfFilename = 'conf-filename'
pkServerName = 'server-name'
pkSSLCertificate = 'ssl-certificate'
pkSSLCertificateKey = 'ssl-certificate-key'

parameterMessages = {
   pkApplicationName: 'The name of the application',
   pkAuthorName: 'Your name (the author\'s name)',
   pkDescription: 'A short description of the application',
   pkContainerName: 'The name of the development container',
   pkNetworkName: 'The name of the docker network to connect to',
   pkRootDirectory: 'The root directory of the website',
   pkConfFilename: 'Name of the Nginx conf file in deployment',
   pkServerName: 'The domain name of the website',
   pkSSLCertificate: 'File path of the SSL Certificate chain',
   pkSSLCertificateKey: 'File path of the SSL Certificate key',
}

parameterDefaults = {
   pkApplicationName: 'WebApp',
   pkAuthorName: 'Ethan D. Twardy',
   pkDescription: '',
   pkContainerName: 'test-container',
   pkNetworkName: 'nginx-net',
   pkRootDirectory: '/var/www/website.com',
   pkConfFilename: 'site.conf',
   pkServerName: 'www.website.com',
   pkSSLCertificate: '/etc/chain.pem',
   pkSSLCertificateKey: '/etc/key.pem',
}

###############################################################################
# Utilities
###

class ParameterManager:
   def __init__(self):
      self.params = {}

   def getParameter(self, key):
      if key not in self.params:
         response = input(parameterMessages[key] + ' ['
                          + parameterDefaults[key] + '] ')
         if response:
            self.params[key] = response
         else:
            self.params[key] = parameterDefaults[key]
      return self.params[key]

def sed(pattern, replacement, filename):
   cmd = "sed -i '' -e 's#" + pattern + "#" + replacement + "#' " + filename
   pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
   pipe.wait()
   if pipe.returncode != 0:
      raise SystemError('sed did not exit successfully.')
   return

def git(command):
   pipe = subprocess.Popen('git ' + command, shell=True,
                           stdout=subprocess.PIPE)
   pipe.wait()
   if pipe.returncode != 0:
      raise SystemError('git did not exit successfully.')
   return

def deleteUnnecessaryFiles(whitelist):
   for path, directories, files in os.walk('.', topdown=False):
      for directory in directories:
         if not directory.listdir(directory):
            os.rmdir(directory)

      for filename in files:
         whitelisted = False
         for entry in whitelist:
            if entry in os.path.join(path, filename):
               whitelisted = True
               break
         if not whitelisted:
            os.remove(os.path.join(path, filename))

###############################################################################
# Component Installers
###

def installDevelopmentContainer(whitelist, parameters):
   # Replace parameters in the files
   sed('CONTAINER_NAME', parameters.getParameter(pkContainerName), 'Makefile')
   sed('NETWORK_NAME', parameters.getParameter(pkNetworkName), 'Makefile')

   rootDirectory = parameters.getParameter(pkRootDirectory)
   sed('ROOT_DIRECTORY', rootDirectory, 'Makefile')
   sed('ROOT_DIRECTORY', rootDirectory, 'development-site.conf')

   # Add the files to the whitelist
   whitelist.append('Makefile')
   whitelist.append('development-site.conf')

###############################################################################
# Main
###

def main():
   parser = argparse.ArgumentParser()
   parser.add_argument('configuration',
                       help=('The configuration to install '
                             'from the template-config.ini file.'))
   arguments = parser.parse_args()

   componentInstallers = {
       'development-container': installDevelopmentContainer
   }

   config = configparser.ConfigParser()
   configurationFile = 'template-config.ini'
   if not config.read(configurationFile):
      raise FileNotFoundError(configurationFile)

   whitelist = []
   parameters = ParameterManager()
   for (key, val) in config.items(arguments.configuration):
      if val:
         componentInstallers[key](whitelist, parameters)

   deleteUnnecessaryFiles(whitelist)

if __name__ == '__main__':
    main()

###############################################################################