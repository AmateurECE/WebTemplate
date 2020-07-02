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
      print('Please enter the following information: ')

   def getParameter(self, key):
      if key not in self.params:
         response = input(parameterMessages[key] + ' ['
                          + parameterDefaults[key] + ']: ')
         if response:
            self.params[key] = response
         else:
            self.params[key] = parameterDefaults[key]
      return self.params[key]

def execute(command):
   pipe = subprocess.Popen(command, shell=True)
   pipe.wait()
   if pipe.returncode != 0:
      raise SystemError()
   return

def sed(pattern, replacement, filename):
   execute("sed -i '' -e 's#" + pattern + "#" + replacement + "#' " + filename)

def git(command):
   execute('git ' + command)

def npm(command):
   execute('npm ' + command)

def isWhitelisted(whitelist, path):
   for entry in whitelist:
      if os.path.realpath(entry) in os.path.realpath(path):
         return True

def deleteUnnecessaryFiles(whitelist):
   for path, directories, files in os.walk('.', topdown=False):
      for directory in directories:
         joinedPath = os.path.join(path, directory)
         if not os.listdir(joinedPath) \
            and not isWhitelisted(whitelist, joinedPath):
            os.rmdir(os.path.join(path, directory))

      for filename in files:
         joinedPath = os.path.join(path, filename)
         if not isWhitelisted(whitelist, joinedPath):
            os.remove(joinedPath)

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

   # Initialize component files
   os.mkdir('log')

   # Add the files to the whitelist
   whitelist.append('Makefile')
   whitelist.append('development-site.conf')
   whitelist.append('log')
   whitelist.append('.gitignore')

def installStaticBase(whitelist, parameters):
   sed('APPLICATION_NAME', parameters.getParameter(pkApplicationName),
       'source/index.html')

   description = parameters.getParameter(pkDescription)
   if description:
      sed('<!--DESCRIPTION-->', '<meta name="description" content="'
          + description + '" />', 'source/index.html')

   whitelist.append('source/index.html')

def installExtension(whitelist, parameters):
   applicationName = parameters.getParameter(pkApplicationName)
   sed('APPLICATION_NAME', applicationName, 'source/popup.html')

   sed('APPLICATION_NAME', applicationName, 'manifest.json')
   sed('DESCRIPTION', parameters.getParameter(pkDescription), 'manifest.json')

   whitelist.append('manifest.json')
   whitelist.append('source/popup.html')
   whitelist.append('source/popup.js')

def installNodePackages(whitelist, parameters):
   sed('APPLICATION_NAME', parameters.getParameter(pkApplicationName),
       'package.json')
   sed('DESCRIPTION', parameters.getParameter(pkDescription), 'package.json')
   sed('AUTHOR', parameters.getParameter(pkAuthorName), 'package.json')

   whitelist.append('source/js/main.js')
   whitelist.append('webpack.config.js')
   whitelist.append('package-lock.json')
   whitelist.append('package.json')
   whitelist.append('node_modules')
   if '.gitignore' not in whitelist:
      whitelist.append('.gitignore')

   npm('install')

# TODO: deployment component (deploy.sh, site.conf)
# TODO: django component
# TODO: LiveReloadServer component (Makefile)

###############################################################################
# Main
###

def main():
   componentInstallers = {
      'development-container': {
         'handler': installDevelopmentContainer,
         'description': ('Docker container implementing an Nginx'
                         ' server for development')},
      'static-base': {
         'handler': installStaticBase,
         'description': 'Base files for static web pages'},
      'extension': {
         'handler': installExtension,
         'description': 'Base files for Chrome Extensions'},
      'node-packages': {
         'handler': installNodePackages,
         'description': 'Webpack and Babel, for bundling js applications'},
   }

   componentKeys = 'Components:\n'
   for key in componentInstallers:
      componentKeys += '  ' + key + ': ' \
         + componentInstallers[key]['description'] + '\n'

   parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=componentKeys)
   parser.add_argument('configuration',
                       help=('The configuration to install '
                             'from the template-config.ini file.'))
   arguments = parser.parse_args()

   config = configparser.ConfigParser()
   configurationFile = 'template-config.ini'
   if not config.read(configurationFile):
      raise FileNotFoundError(configurationFile)

   whitelist = []
   parameters = ParameterManager()
   for (key, val) in config.items(arguments.configuration):
      if val:
         componentInstallers[key]['handler'](whitelist, parameters)

   deleteUnnecessaryFiles(whitelist)
   git('init')
   git('add .')
   git('commit -m "Initialize from WebTemplate"')

if __name__ == '__main__':
    main()

###############################################################################
