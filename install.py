
###############################################################################
# NAME:             install.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Installation script for the template.
#
# CREATED:          07/01/2020
#
# LAST EDITED:      07/12/2020
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
pkServerName = 'server-name'
pkSSLCertificate = 'ssl-certificate'
pkSSLCertificateKey = 'ssl-certificate-key'
pkRemoteRepositoryPath = 'remote-repository-path'
pkRemoteRepositoryName = 'remote-repository-name'
pkRemoteUser = 'remote-user'
pkRemoteHost = 'remote-host'
pkRemotePort = 'remote-port'

parameterMessages = {
   pkApplicationName: 'The name of the application',
   pkAuthorName: 'Your name (the author\'s name)',
   pkDescription: 'A short description of the application',
   pkContainerName: 'The name of the development container',
   pkNetworkName: 'The name of the docker network to connect to',
   pkRootDirectory: 'The root directory of the website',
   pkServerName: 'The domain name of the website',
   pkSSLCertificate: 'File path of the SSL Certificate chain',
   pkSSLCertificateKey: 'File path of the SSL Certificate key',
   pkRemoteRepositoryPath: 'Path of the repository on the remote',
   pkRemoteRepositoryName: 'Name of the remote in the local repository',
   pkRemoteUser: 'Name of the remote user',
   pkRemoteHost: 'Remote hostname to connect to',
   pkRemotePort: 'Port to connect to on the remote',
}

parameterDefaults = {
   pkApplicationName: 'WebApp',
   pkAuthorName: 'Ethan D. Twardy',
   pkDescription: '',
   pkContainerName: 'test-container',
   pkNetworkName: 'nginx-net',
   pkRootDirectory: '/var/www/website.com',
   pkServerName: 'www.website.com',
   pkSSLCertificate: '/etc/chain.pem',
   pkSSLCertificateKey: '/etc/key.pem',
   pkRemoteRepositoryName: 'deployment',
   pkRemoteUser: 'edtwardy',
   pkRemoteHost: '192.168.1.60',
   pkRemotePort: '5000',
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

def installDevelopmentContainer(whitelist, parameters, completionHooks):
   # Replace parameters in the files
   sed('CONTAINER_NAME', parameters.getParameter(pkContainerName), 'Makefile')
   sed('NETWORK_NAME', parameters.getParameter(pkNetworkName), 'Makefile')

   rootDirectory = '/var/dev/container.com' # It doesn't matter
   sed('ROOT_DIRECTORY', rootDirectory, 'Makefile')
   sed('ROOT_DIRECTORY', rootDirectory, 'development-site.conf')

   # Initialize component files
   os.mkdir('log')

   # Add the files to the whitelist
   whitelist.append('Makefile')
   whitelist.append('development-site.conf')
   whitelist.append('log')
   whitelist.append('.gitignore')

def installStaticBase(whitelist, parameters, completionHooks):
   sed('APPLICATION_NAME', parameters.getParameter(pkApplicationName),
       'static/index.html')

   description = parameters.getParameter(pkDescription)
   if description:
      sed('<!--DESCRIPTION-->', '<meta name="description" content="'
          + description + '" />', 'static/index.html')

   whitelist.append('static/index.html')

def installExtension(whitelist, parameters, completionHooks):
   applicationName = parameters.getParameter(pkApplicationName)
   sed('APPLICATION_NAME', applicationName, 'extension/popup.html')

   sed('APPLICATION_NAME', applicationName, 'manifest.json')
   sed('DESCRIPTION', parameters.getParameter(pkDescription), 'manifest.json')

   whitelist.append('manifest.json')
   whitelist.append('extension/popup.html')
   whitelist.append('extension/popup.js')

def installNodePackages(whitelist, parameters, completionHooks):
   sed('APPLICATION_NAME', parameters.getParameter(pkApplicationName),
       'package.json')
   sed('DESCRIPTION', parameters.getParameter(pkDescription), 'package.json')
   sed('AUTHOR', parameters.getParameter(pkAuthorName), 'package.json')

   whitelist.append('static/js/main.js')
   whitelist.append('webpack.config.js')
   whitelist.append('package-lock.json')
   whitelist.append('package.json')
   whitelist.append('node_modules')
   if '.gitignore' not in whitelist:
      whitelist.append('.gitignore')

   npm('install')

def installDeployStatic(whitelist, parameters, completionHooks):
   host = parameters.getParameter(pkRemoteHost)
   user = parameters.getParameter(pkRemoteUser)
   port = parameters.getParameter(pkRemotePort)

   applicationName = parameters.getParameter(pkApplicationName)
   parameterDefaults[pkRemoteRepositoryPath] = \
      f'/home/{user}/Git/Serve/{applicationName}'
   path = parameters.getParameter(pkRemoteRepositoryPath)
   parameterDefaults[pkRootDirectory] = \
      f'{parameterDefaults[pkRemoteRepositoryPath]}/source'
   rootDirectory = parameters.getParameter(pkRootDirectory)

   # Create hook to add production remote after git reinitialization
   remote = parameters.getParameter(pkRemoteRepositoryName)
   remoteUri = f'ssh://{user}@{host}:{port}{path}'
   completionHooks.append(lambda: git(f'remote add {remote} {remoteUri}'))

   sed('SERVER_NAME', parameters.getParameter(pkServerName),
       'deployment-site.conf')
   sed('ROOT_DIRECTORY', rootDirectory, 'deployment-site.conf')
   sed('SSL_CERTIFICATE', parameters.getParameter(pkSSLCertificate),
       'deployment-site.conf')
   sed('SSL_CERTIFICATE_KEY', parameters.getParameter(pkSSLCertificateKey),
       'deployment-site.conf')

   # If there is an update hook, save it.
   hookCommand = ''
   with open('post-update.hook', 'r') as postUpdateHook:
      hookCommand = """echo exec ../post-update.hook > .git/hooks/post-update;
                     chmod +x .git/hooks/post-update;"""
   script = f"""\
   ssh -p {port} {user}@{host} '
   mkdir -p {path};
   cd {path};
   git init;
   git config --local receive.denyCurrentBranch updateInstead;
   {hookCommand}
   '"""

   execute(script)
   whitelist.append('deployment-site.conf')
   whitelist.append('post-update.hook')

def installDjangoApp(whitelist, parameters, completionHooks):
   # TODO: Modify static/index.html to create a template
   #   This will require moving static/index.html to template/app/index.html,
   #   and modifying the file to make it extend a base template.
   appName = parameters.getParameter(pkApplicationName)
   pwd = os.path.realpath('.')
   completionHooks.extend([
      lambda: execute(f'django-admin startapp {appName} {pwd}')
   ])

# TODO: pre-commit hook to generate bundle.js
# TODO: LiveReloadServer component (Makefile)

def installMiddleman(whitelist, parameters, completionHooks):
   """Install the Middleman component"""
   completionHooks.extend([
      lambda: execute('middleman init'),
      lambda: execute('echo "activate :relative_assets" >> config.rb')
   ])

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
      'deploy-static': {
         'handler': installDeployStatic,
         'description': 'Infrastructure for deploying static web pages'},
      'django-app': {
         'handler': installDjangoApp,
         'description': 'Django Application template.'},
      'middleman': {
         'handler': installMiddleman,
         'description': 'Middleman project initialization'},
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
   hooks = []
   for (key, val) in config.items(arguments.configuration):
      if val:
         componentInstallers[key]['handler'](whitelist, parameters, hooks)

   deleteUnnecessaryFiles(whitelist)
   git('init')
   for function in hooks:
      function()
   git('add .')
   git('commit -m "Initialize from WebTemplate"')

if __name__ == '__main__':
    main()

###############################################################################
