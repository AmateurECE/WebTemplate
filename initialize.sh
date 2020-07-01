#!/bin/bash
###############################################################################
# NAME:             initialize.sh
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Initialize the repository and fill in the prerequisites.
#
# CREATED:          05/19/2020
#
# LAST EDITED:      07/01/2020
###

USAGE="
Usage: initialize.sh <installType>

Where <installType> is one of (static, static-node, django, extension)"
usage() {
    printf '%s\n' "$USAGE"
    exit 1
}

promptDefault() {
    read -p "$1 [$2]: " retVal
    echo "${retVal:-$2}"
}

deleteUnnecessaryFiles() {
    if [[ -z "$@" ]]; then
        return
    fi
    whitelist="$@"
    whitelist="${whitelist// /\|}"
    rm -f $(find . | grep -v "$whitelist") 2> /dev/null
    find . -type d -empty -delete
}

###############################################################################
# Installation Scripts
###

doStaticInstallation() {
    applicationName=$(promptDefault "The name of the application" "WebApp")
    description=$(promptDefault "A short description of the application" "")
    containerName=$(promptDefault "The name of the development container"\
                                  "test-container")
    networkName=$(promptDefault "The name of the docker network to connect to"\
                                "nginx-net")
    rootDirectory="/var/www/website.com"

    sed -i '' -e 's/CONTAINER_NAME/'$containerName'/' Makefile
    sed -i '' -e 's/NETWORK_NAME/'$networkName'/' Makefile
    sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' Makefile
    sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' development-site.conf
    sed -i '' -e 's/APPLICATION_NAME/'$applicationName'/' source/index.html

    if [[ ! -z $description ]]; then
        pattern="<!--DESCRIPTION-->"
        replacement="<meta name=\"description\" content=\"$description\" />"
        sed -i '' -e "s#$pattern#$replacement#" source/index.html
    fi

    whitelist=("Makefile" "development-site.conf" "source/index.html")
    deleteUnnecessaryFiles "${whitelist[@]}"
}

# applicationName=$(promptDefault "The name of the application" "WebApp")
# authorName=$(promptDefault "Your name (the author's name)" "Ethan D. Twardy")
# description=$(promptDefault "A short description of the application" "")
# containerName=$(promptDefault "The name of the development container"\
#                               "test-container")
# networkName=$(promptDefault "The name of the docker network to connect to"\
#                             "nginx-net")
# rootDirectory=$(promptDefault "The root directory of the website"\
#                               "/var/www/website.com")
# confFilename=$(promptDefault "The name of the Nginx conf file in deployment"\
#                              "site.conf")
# serverName=$(promptDefault "The domain name of the website"\
#                            "www.website.com")
# sslCertificate=$(promptDefault "The file path of the SSL Certificate chain"\
#               "/etc/chain.pem")
# sslCertificateKey=$(promptDefault "The file path of the SSL Certificate key"\
#                  "/etc/key.pem")

# sed -i '' -e 's/CONTAINER_NAME/'$containerName'/' Makefile
# sed -i '' -e 's/NETWORK_NAME/'$networkName'/' Makefile
# sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' Makefile

# sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' deploy.sh
# sed -i '' -e 's/CONF_FILENAME/'$confFilename'/' deploy.sh

# sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' development-site.conf

# sed -i '' -e 's/SERVER_NAME/'$serverName'/' site.conf
# sed -i '' -e 's#ROOT_DIRECTORY#'$rootDirectory'#' site.conf
# sed -i '' -e 's#SSL_CERTIFICATE_KEY#'$sslCertificateKey'#' site.conf
# sed -i '' -e 's#SSL_CERTIFICATE#'$sslCertificate'#' site.conf

# sed -i '' -e 's/NAME/'$applicationName'/' package.json
# sed -i '' -e 's/AUTHOR/'"$authorName"'/' package.json
# sed -i '' -e 's/DESCRIPTION/'"$description"'/' package.json

# npm install

###############################################################################
# Initialization Logic
###

INSTALLATION_TYPE=$1
printf '%s\n' "Please enter the following information."
case "$INSTALLATION_TYPE" in
    static)
        doStaticInstallation
        ;;
    static-node)
        doStaticNodeInstallation
        ;;
    django)
        doDjangoInstallation
        ;;
    extension)
        doExtensionInstallation
        ;;
    *)
        usage
        ;;
esac

mkdir log
git init
git add .
git commit -m 'Initialize from WebTemplate Repository'

###############################################################################
