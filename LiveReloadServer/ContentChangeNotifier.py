###############################################################################
# NAME:             ContentChangeNotifier.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      This python script watches the source directory for changes
#                   and notifies subscribers of changes to directory files.
#
# CREATED:          05/19/2020
#
# LAST EDITED:      05/19/2020
###

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from Network import Server, Client

class SubscriberServer(QtCore.QThread):
    def __init__(self, port):
        QtCore.QThread.__init__(self)
        self.port = port
        self.mutex = QtCore.QMutex()
        self.subscribers = []

    def __del__(self):
        self.wait()

    def run(self):
        address = ("127.0.0.1", self.port)
        with Server(self.onSubscribeReceipt, address) as server:
            server.start()

    def onSubscribeReceipt(self, message, address):
        self.mutex.lock()
        print('Received datagram')
        if message == "SUBSCRIBE":
            print('Subscribing new user')
            self.subscribers.append(address)
        self.mutex.unlock()
        return "OK"

    def notifySubscribers(self):
        """This method is run inside of a separate thread."""
        with Client() as client:
            self.mutex.lock()
            for subscriber in self.subscribers:
                client.send("UPDATE", subscriber, waitForResponse=False)
            self.mutex.unlock()

class ContentChangeNotifier(QtCore.QFileSystemWatcher):
    """A simple wrapper for PyQt5 Signals and Slots."""

    def __init__(self, handler, *args, **kwargs):
        super(ContentChangeNotifier, self).__init__(*args, **kwargs)
        self.handler = handler
        self.directoryChanged.connect(self.onDirectoryChanged)

    def onDirectoryChanged(self, path):
        print('onDirectoryChanged')
        self.handler()

###############################################################################
# Main
###

def main():
    app = QApplication(sys.argv)
    server = SubscriberServer(20001)
    server.start()
    notifier = ContentChangeNotifier(server.notifySubscribers, sys.argv[1:])
    app.exec_()

if __name__ == '__main__':
    main()

###############################################################################
