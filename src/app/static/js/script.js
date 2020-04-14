
$(document).ready(function () {
  //**Add a file */
  $('#submit-data').click(function () {
    var fd = new FormData();
    fd.append('file', $('#file-input')[0].files[0]);
    
    fetch(`/analyse`, {
      method: 'POST',
      body: fd,
      cache: 'no-cache',
    })
    //response from views.py
    .then(function(response){
      if(response.status !== 200){
        return;
      }
      response.json().then(function(data){
        alert("Ficher ajouté");
        console.log(data);
        window.location = window.origin + '/models'
      })
    })
    .catch((error) => {
      console.error('Error:', error);
      return;
    });
  });

  //**Menu */
  $('.burger, .overlay').click(function () {
    $('.burger').toggleClass('clicked');
    $('.overlay').toggleClass('show');
    $('nav').toggleClass('show');
    $('body').toggleClass('overflow');
  })

  //**Popup */
  $(function popup() {
    // Open Popup
    $('[popup-open]').on('click', function () {
      var popup_name = $(this).attr('popup-open');
      $('[popup-name="' + popup_name + '"]').fadeIn(300);
    });

    // Close Popup
    $('[popup-close]').on('click', function () {
      var popup_name = $(this).attr('popup-close');
      $('[popup-name="' + popup_name + '"]').fadeOut(300);
    });

    // Close Popup When Click Outside
    $('.popup').on('click', function () {
      var popup_name = $(this).find('[popup-close]').attr('popup-close');
      $('[popup-name="' + popup_name + '"]').fadeOut(300);
    }).children().click(function () {
      return false;
    });

  });
});
