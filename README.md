# Website Template

This template repository contains some useful tools for website development.
It will be expanded as I further develop my workflow. Usage of this repository
is further explained below, however, upon cloning/downloading, it is important
to initialize the template:

```
./initialize.sh
```

Follow the prompts, filling in the requisite information. This script populates
important files with information needed to set up the workflow.

## Using the Live Reloading Server

The `Makefile` is already configured to use the server. Run `make` to start it
up. This will also start up a Docker container to serve the website via Nginx.
In order to enable live reloading for an HTML file, add the following to the
bottom of the `body` in your file:

```
<script src="source/js/debug.js"></script>
```

Navigate to the webpage in your browser and concurrently open the HTML file in
your favorite text editor. Begin working on the page source, and whenever you
save the file, the browser window should be automatically refreshed to display
your newest changes. Pretty neat!
