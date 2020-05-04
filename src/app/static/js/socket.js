jQuery(document).ready(function ($) {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    
    /*
    socket.on('connect', function () {
        socket.emit('my event', {
            data: 'User Connected'
        })
        
    });

    socket.on('my response', function (msg) {
        console.log(msg)
    });
    */

});