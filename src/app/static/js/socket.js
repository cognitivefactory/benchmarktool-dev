jQuery(document).ready(function ($) {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function () {

        var form = $('form').on('submit', function (e) {
            e.preventDefault()
            socket.emit('start_training', {
                name: $('#name').val(),
            })
        })
    })
    socket.on('training', function (msg) {
        content = $('[popup-name="popup-start"] > .popup-content');
        content.children().hide();

        if(msg!=1){
            content.append("<h1>Jeu de données d'entraînement vide</h1>")
            content.append("<p>Veuillez sélection un jeu de données d'entraînement</p>");
            setTimeout(function () { window.location = window.origin + '/data_train'; }, 2000);
        }else{
            content.append("<h1>Démarrage de l'entraînement<h1>");
            setTimeout(function () { window.location = window.origin + '/models'; }, 2000);
        }
    })

});