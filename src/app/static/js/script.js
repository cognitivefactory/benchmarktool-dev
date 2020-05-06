jQuery(document).ready(function ($) {
  //**Menu */
  $('.burger, .overlay').click(function () {
    $('.burger').toggleClass('clicked');
    $('.overlay').toggleClass('show');
    $('nav').toggleClass('show');
    $('body').toggleClass('overflow');
  })


  //**Popup */
  //open
  $('[popup-open]').on('click', function () {
    var popup_name = $(this).attr('popup-open');
    $('[popup-name="' + popup_name + '"]').fadeIn(300);
  });
  //close
  $('[popup-close]').on('click', function () {
    var popup_name = $(this).attr('popup-close');
    $('[popup-name="' + popup_name + '"]').fadeOut(300);
  });

  /////////////
  //// data_train.html

  //**Add a file */
  $('#submit-data').click(function () {
    content = $('[popup-name="popup-train"] > .popup-content');
    content.children().hide();
    content.append("<h1>Vérification du fichier en cours<h1>");
    content.append("<p>Veuillez patienter quelques instants.</p>")

    var fd = new FormData();
    fd.append('file', $('#file-input')[0].files[0]);

    fetch(`/add_train`, {
      method: 'POST',
      body: fd,
      cache: 'no-cache',
    })
      //response from views.py
      .then(function (response) {
        if (response.status !== 200) {
          alert("Incorrect file");
          return;
        }
        response.json().then(function (data) {
          content.children().hide();
          content.append("<h1>Fichier ajouté<h1>");
          setTimeout(function () { window.location = window.origin + '/models'; }, 2000);
        })
      })
      .catch((error) => {
        console.error('Error:', error);
        return;
      });
  });


  /////////////
  //// models.html

  $('#submit-start').click(function () {
    content = $('[popup-name="popup-start"] > .popup-content');
    content.children().hide();

    var entry = {
      name: $("#name").val()
    }
    fetch(`/start_training`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(entry)
    })
      //response from views.py
      .then(function (response) {
        if(response.status == 100) {
          content.append("<h1>Erreur<h1>");
          setTimeout(function () { window.location = window.origin + '/models'; }, 2000);
          return;
        }
        response.json().then(function (data) {
          if(data["state"] == 0){
            content.append("<h1>Jeu de données d'entraînement vide</h1>")
            content.append("<p>Veuillez sélection un jeu de données d'entraînement</p>");
            setTimeout(function () { window.location = window.origin + '/data_train'; }, 2000);
          }
          else{
            content.append("<h1>Démarrage de l'entraînement<h1>");
            setTimeout(function () { window.location = window.origin + '/models'; }, 2000);
          }
        })
      })
      .catch((error) => {
        console.error('Error:', error);
        return;
      });
  });

});
