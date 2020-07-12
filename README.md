# Website Template

This template repository contains some useful tools for website development.
It will be expanded as I further develop my workflow. Usage of this repository
is further explained below.

## Initializing the Template

This repository is composed of a number of _components_, which can be installed
individually or in tandem to create the basis for a useful template of web
development. Templates are enabled in `template-config.ini`, which is read when
installing the components by running `install.py`. The user can obtain a list
of installable components and descriptions of them by running:

```
python3 install.py -h
```

Use the provided `template-config.ini` as a starting point. Sections in this
file name configurations that can be selected, allowing the user to install
a standard combination of components. For example, the `static` configuration
installs a development container and a template for an `index.html` file, and
can be installed using the following command:

```
python3 install.py static
```

Note that `install.py` deletes itself as part of the installation process, so
can only be called once.

## Component Prerequisites

Components assume a number of prerequisite conditions which must be met for
correct operation. Obviously, the `install.py` script depends on having a valid
python3.5+ distribution. All components depend on having the `git` command-line
client and `sed` installed. Other prerequisites are named below:

1. development-container: Must have Docker installed, with the command-line
client, a docker network set up to allow forwarding traffic from localhost to
the guest container (mine is called `nginx-net`), and the Nginx base image.
Must have `make` installed.
2. static-base: None.
3. node-packages: Must have `npm` installed.
4. extension: None.
5. deploy-static: See functionality of this component below. Must have `ssh`
installed on local and remote machine, and `git`, `wget`, `sed` and Nginx
installed on the remote machine. The install script assumes the remote machine
is running some flavor of Linux. Cygwin may be supported by default, but this
is not tested.
6. middleman: Must have a working ruby distribution and the middleman bundle
installed.

## Using the deploy-static Component

This component allows the user to deploy website changes by pushing refs to a
remote repository. The name of the remote can be selected at install time, so
the user may also maintain another remote repository.

The install script assumes the remote machine is running some flavor of Linux.
Cygwin may be supported by default, but this is not tested.

The user may take advantage of this component by following these steps:
1. Install the component by using the install script and following the prompts.
2. Edit the `post-update.hook` and `deployment-site.conf` files. The default
Nginx conf file may not be suitable. For example, all of my sites are deployed
as locations within my domain, so I would rewrite this file to contain:
```
location /myapp/ {
    alias /home/edtwardy/Git/Serve/MyApp/;
    index index.html
}
```
3. Commit and push these changes. The hook will require no further
configuration.
4. Log into the server using your credentials, and manually install the Nginx
configuration. For example, I install it to
/etc/nginx/conf.d/location.d/myapp.conf.
5. Reload Nginx.

## Using the Live Reloading Server

The `Makefile` is already configured to use the server. Run `make run` to start
it up. This will also start up a Docker container to serve the website via
Nginx. In order to enable live reloading for an HTML file, add the following to
the bottom of the `body` in your file:

```
<script src="static/js/debug.js"></script>
```

Navigate to the webpage in your browser and concurrently open the HTML file in
your favorite text editor. Begin working on the page source, and whenever you
save the file, the browser window should be automatically refreshed to display
your newest changes. Pretty neat!

*Note*: The `development-container` component must also be installed, or the
live reloading server will not function.

## Using the Middleman component

The Middleman component should not be used with other components, except
the `deploy-static` component. It may be possible to install the
`django-app` component alongside, but that is currently untested.

// TODO: Test installation of django-app alongside middleman
