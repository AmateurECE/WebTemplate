###############################################################################
# NAME:             LiveReloadServer.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      This debug server returns an XHR when a file changes, which
#                   causes the browser (by the javascript) to refresh the page.
#
# CREATED:          05/17/2020
#
# LAST EDITED:      05/19/2020
###

from flask import Flask, Response
from .Network import Client

class LiveReloadServer(Flask):
    """Returns an XHR when the content changes, triggering browser reload."""

    def __init__(self, notifierPort, name):
        super(LiveReloadServer, self).__init__(name)
        self.notifierAddress = ("127.0.0.1", notifierPort)
        self.client = Client()
        response = self.client.send("SUBSCRIBE", self.notifierAddress)
        if response != "OK":
            raise RuntimeError(("ContentNotifier Server is not running at"
                                " address {}").format(self.notifierAddress))

    def run(self, host=None, port=None, debug=None, load_dotenv=True,
            **options):
        super(LiveReloadServer, self).run(host, port, debug, load_dotenv,
                                          **options)

    def xhrHandler(self):
        """Handle the incoming Ajax request."""
        # This method is called from the flask server thread.
        # Essentially, we block until the fileChangeHandler releases the mutex
        print('Received Ajax Request. Blocking...')
        message, address = self.client.recvfrom()
        print('Pushing changes...')
        return Response({}, status=200, mimetype="application/json")

###############################################################################
# Main
###

app = LiveReloadServer(20001, __name__)

@app.route('/xhr')
def theXhrReceiver():
    return app.xhrHandler()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=13001)

###############################################################################
