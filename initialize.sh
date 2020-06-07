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
# LAST EDITED:      06/07/2020
###

printf '%s\n' "Please enter the following information."
# NAME
prompt="The name of the application [WebApp]: "
read -p "$prompt" applicationName
applicationName=${applicationName:-WebApp}

# AUTHOR
prompt="Your name (the author's name) [Ethan D. Twardy]: "
read -p "$prompt" authorName
authorName=${authorName:-"Ethan D. Twardy"}

# DESCRIPTION
prompt="A short description of the application []: "
read -p "$prompt" description

# CONTAINER_NAME
prompt="The name of the development container be [test-container]: "
read -p "$prompt" containerName
containerName=${containerName:-"test-container"}

# NETWORK_NAME
prompt="The name of the docker network to connect to [nginx-net]: "
read -p "$prompt" networkName
networkName=${networkName:-"nginx-net"}

# ROOT_DIRECTORY
prompt="The root directory of the website [/var/www/website.com]: "
read -p "$prompt" rootDirectory
rootDirectory=${rootDirectory:-/var/www/website.com}

# CONF_FILENAME
prompt="The name of the Nginx conf file in deployment [site.conf]: "
read -p "$prompt" confFilename
confFilename=${confFilename:-site.conf}

# SERVER_NAME
prompt="The domain name of the website [www.website.com]: "
read -p "$prompt" serverName
serverName=${serverName:-www.website.com}

# SSL_CERTIFICATE
prompt="The file path of the SSL certificate chain [/etc/chain.pem]: "
read -p "$prompt" sslCertificate
sslCertificate=${sslCertificate:-/etc/chain.pem}

# SSL_CERTIFICATE KEY
prompt="The file path of the SSL certificate key [/etc/key.pem]: "
read -p "$prompt" sslCertificateKey
sslCertificateKey=${sslCertificateKey:-/etc/key.pem}

# Makefile
sed -i '' -e 's/CONTAINER_NAME/'$containerName'/' Makefile
sed -i '' -e 's/NETWORK_NAME/'$networkName'/' Makefile
sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' Makefile

# deploy.sh
sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' deploy.sh
sed -i '' -e 's/CONF_FILENAME/'$confFilename'/' deploy.sh

# development-site.conf
sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' development-site.conf

# site.conf
sed -i '' -e 's/SERVER_NAME/'$serverName'/' site.conf
sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' site.conf
sed -i '' -e 's#SSL_CERTIFICATE_KEY#'$sslCertificateKey'#' site.conf
sed -i '' -e 's#SSL_CERTIFICATE#'$sslCertificate'#' site.conf

# package.json
sed -i '' -e 's/NAME/'$applicationName'/' package.json
sed -i '' -e 's/AUTHOR/'"$authorName"'/' package.json
sed -i '' -e 's/DESCRIPTION/'"$description"'/' package.json

###############################################################################
