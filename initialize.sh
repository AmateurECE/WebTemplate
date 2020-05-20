#!/bin/sh
###############################################################################
# NAME:             initialize.sh
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Initialize the repository and fill in the prerequisites.
#
# CREATED:          05/19/2020
#
# LAST EDITED:      05/19/2020
###

# CONTAINER_NAME
printf '%s\n' "Please enter the following information."
prompt="The name of the development container be (e.g. test-container): "
read -p "$prompt" containerName

# NETWORK_NAME
prompt="The name of the docker network to connect to (e.g. test-net): "
read -p "$prompt" networkName

# ROOT_DIRECTORY
prompt="The root directory of the website (e.g. mywebsite.com): "
read -p "$prompt" rootDirectory

# CONF_FILENAME
prompt="The name of the Nginx conf file in deployment (e.g. site.conf): "
read -p "$prompt" confFilename

# SERVER_NAME
prompt="The domain name of the website (e.g. www.mywebsite.com): "
read -p "$prompt" serverName

# SSL_CERTIFICATE
prompt="The file path of the SSL certificate chain (e.g. /etc/chain.pem): "
read -p "$prompt" sslCertificate

# SSL_CERTIFICATE KEY
prompt="The file path of the SSL certificate key (e.g. /etc/key.pem): "
read -p "$prompt" sslCertificateKey

# Makefile
sed -i '' -e 's/CONTAINER_NAME/'$containerName'/' Makefile
sed -i '' -e 's/NETWORK_NAME/'$networkName'/' Makefile
sed -i '' -e 's/ROOT_DIRECTORY/'$rootDirectory'/' Makefile

# deploy.sh
sed -i '' -e 's/ROOT_DIRECTORY/'$rootDirectory'/' deploy.sh
sed -i '' -e 's/CONF_FILENAME/'$confFilename'/' deploy.sh

# development-site.conf
sed -i '' -e 's/ROOT_DIRECTORY/'$rootDirectory'/' development-site.conf

# site.conf
sed -i '' -e 's/SERVER_NAME/'$serverName'/' site.conf
sed -i '' -e 's/ROOT_DIRECTORY/'$rootDirectory'/' site.conf
sed -i '' -e 's#SSL_CERTIFICATE_KEY#'$sslCertificateKey'#' site.conf
sed -i '' -e 's#SSL_CERTIFICATE#'$sslCertificate'#' site.conf

###############################################################################
