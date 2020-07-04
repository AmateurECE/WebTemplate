///////////////////////////////////////////////////////////////////////////////
// NAME:            debug.js
//
// AUTHOR:          Ethan D. Twardy <edtwardy@mtu.edu>
//
// DESCRIPTION:     This script implements a live reloading fetch mechanism.
//
// CREATED:         05/19/2020
//
// LAST EDITED:     05/19/2020
////

"use strict";

class DebugRefresher {
    queryURL = "";

    constructor(queryURL) {
        this.queryURL = queryURL;
    }

    fire() {
        fetch(this.queryURL)
            .then((value, reason) => {
                if (!value.ok) {
                    reject(value.status);
                }
                window.location.reload(true);
                this.fire();
            })
            .catch(() => {
                console.error("Debug server is not running.");
            });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    var liveReloader = new DebugRefresher('/xhr');
    liveReloader.fire();
});

///////////////////////////////////////////////////////////////////////////////
