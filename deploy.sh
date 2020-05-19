###############################################################################
# NAME:             deploy.sh
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Deploys the website.
#
# CREATED:          05/10/2020
#
# LAST EDITED:      05/19/2020
###

if [[ $UID -ne 0 ]]; then
    printf '%s\n' "This script must be run as root."
    exit
fi

rsync -r source/ /var/www/ROOT_DIRECTORY
rsync site.conf /etc/nginx/conf.d/CONF_FILENAME
nginx -s reload

###############################################################################
