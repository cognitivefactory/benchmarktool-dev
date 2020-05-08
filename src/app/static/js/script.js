
jQuery(document).ready(function ($) {

  $('.burger, .overlay').click(function () {
    $('.burger').toggleClass('clicked');
    $('.overlay').toggleClass('show');
    $('nav').toggleClass('show');
    $('body').toggleClass('overflow');
  })


  //**Popup */
  //open
  $('[popup_open]').on('click', function () {
    var popup_name = $(this).attr('popup_open');
    $('[popup_name="' + popup_name + '"]').fadeIn(300);
  });
  //close
  $('[popup_close]').on('click', function () {
    var popup_name = $(this).attr('popup_close');
    $('[popup_name="' + popup_name + '"]').fadeOut(300);
  });

  /////////////
  //// data_train.html

  //**Add a file */
  $('#submit_data').click(function () {
    content = $('[popup_name="popup_train"] > .popup_content');
    content.children().hide();
    content.append("<h1>Vérification du fichier en cours<h1>");
    content.append("<p>Veuillez patienter quelques instants.</p>")

    var fd = new FormData();
    fd.append('file', $('#file_input')[0].files[0]);

    fetch(`/add_train`, {
      method: 'POST',
      body: fd,
      cache: 'no-cache',
    })
      //response from views.py
      .then(function (response) {
        if (response.status !== 200) {
          content.children().hide();
          content.append("<h1>Fichier incorrect</h1><p>Veuillez réessayer.</p>");
          setTimeout(function () { window.location = window.origin + '/data_train'; }, 2000);
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
});
