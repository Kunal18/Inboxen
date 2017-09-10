/*!
 * Copyright (c) 2017 Jessica Tallon & Matt Molyneaux
 * Licensed under AGPLv3 (https://github.com/Inboxen/Inboxen/blob/master/LICENSE)
 */

(function($){
    'use strict';

    var copySupported, copyEnalbed;
    copySupported = document.queryCommandSupported("copy");
    copyEnabled = document.queryCommandEnabled("copy");

    if !(copySupported && copyEnabled) {
        console.log("Copying not supported.");
        return;
    }

    $(".inbox-name > a").forEach(function() {
        // something?
    });

})(jQuery);
