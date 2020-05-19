###############################################################################
# NAME:		    Makefile
#
# AUTHOR:	    Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:	    The default rule for the website hosts this website using
#		    the nginx Docker base image on localhost:8080
#
# CREATED:	    04/20/2020
#
# LAST EDITED:	    05/19/2020
###

sourceDir=$(shell realpath .)/source
nginxConf=$(shell realpath .)/development-site.conf
containerName=CONTAINER_NAME
networkName=NETWORK_NAME
rootDirectory=ROOT_DIRECTORY

install:
	mkdir log

run:
	docker run -d --rm --name $(containerName) -p "8080:80" \
		--network $(networkName) \
		-v "$(sourceDir):/var/www/$(rootDirectory):ro" \
		-v "$(nginxConf):/etc/nginx/conf.d/default.conf:ro"\
		-v "`realpath .`/log:/var/log/nginx" \
		nginx:latest
	python3 LiveReloadServer/ContentChangeNotifier.py $(sourceDir) &
	uwsgi --master --log-master --http-socket=0.0.0.0:13001 \
		-w LiveReloadServer.LiveReloadServer:app &

###############################################################################
