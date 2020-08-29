jQuery(document).ready(function ($) {

  function submit_file(popup_name) {
    content = $('[popup_name="' + popup_name + '"]' + ' > .popup_content');

    content.children().hide();
    content.append("<h1>Vérification du fichier en cours<h1>");
    content.append("<p>Veuillez patienter quelques instants.</p>")

    var fd = new FormData();
    fd.append('file', $('#file_input')[0].files[0]);
    var page;
    if(popup_name == "popup_train"){
      page = `/add_train`
    }else{
      page = `/processing`
    }
      
    fetch(page, {
      method: 'POST',
      body: fd,
      cache: 'no-cache',
    })
    //response from views.py
    .then(function (response) {
      if (response.status !== 200) {
        content.children().hide();
        content.append("<h1>Fichier incorrect</h1><p>Veuillez réessayer.</p>");
        if(popup_name == "popup_train"){
          setTimeout(function () { window.location = window.origin + '/data_train'; }, 2000);
        }else{
          setTimeout(function () { window.location = window.origin + '/results'; }, 2000);
        }            
        return;
      }
      response.json().then(function (data) {
        content.children().hide();
        content.append("<h1>Fichier ajouté<h1>");
        if(popup_name == "popup_train"){
          setTimeout(function () { window.location = window.origin + '/models'; }, 2000);
        }else{
          setTimeout(function () { window.location = window.origin + '/results'; }, 2000);
        }
      })
    })
    .catch((error) => {
      //Fixing the error for Chrome users
      content.children().hide();
      content.append("<h1>Fichier incorrect</h1><p>Veuillez réessayer.</p>");
      if(popup_name == "popup_train"){
        setTimeout(function () { window.location = window.origin + '/data_train'; }, 2000);
      }else{
        setTimeout(function () { window.location = window.origin + '/results'; }, 2000);
      }
      return;
    });
  };


  $('.burger, .overlay').click(function () {
    $('.burger').toggleClass('clicked');
    $('.overlay').toggleClass('show');
    $('nav').toggleClass('show');
    $('body').toggleClass('overflow');
  })


  //**Popup */
  //open
  var popup_name = ""
  $('[popup_open]').on('click', function () {
    popup_name = $(this).attr('popup_open');
    $('[popup_name="' + popup_name + '"]').fadeIn(300);
  });
  //close
  $('[popup_close]').on('click', function () {
    var popup_name = $(this).attr('popup_close');
    $('[popup_name="' + popup_name + '"]').fadeOut(300);
  });

  /////////////
  //// Submit a file : train and test files
  $('#submit_data').click(function () {
    submit_file(popup_name);
  });



  /////////////
  //// Select library
  var selection;
  var last_select;
  $('#libraries').change(function () {
    selection = $('#libraries').val()
    selection = $("#" + selection + "_options");
    selection.toggle();
    if(last_select){
      last_select.toggle();
    }
    last_select = selection;

  });
  



});
