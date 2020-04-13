
$(document).ready(function () {

  $('#submit-data').click(function () {
    var fd = new FormData();
    fd.append('file', $('#file-input')[0].files[0]);
    
    fetch(`/analyse`, {
      method: 'POST',
      body: fd,
      cache: 'no-cache',
    })
    .then(function(response){
      if(response.status !== 200){
        return;
      }
      response.json().then(function(data){
        alert("le fichier a été ajouté \n");
        console.log(data);
      })
    })
    .catch((error) => {
      console.error('Error:', error);
      return;
    });
  });

  
  // // POST
  // fetch('/analyse', {

  //   // Specify the method
  //   method: 'POST',

  //   // A JSON payload
  //   body: JSON.stringify({
  //     "greeting": "Hello from the browser!"
  //   })
  // }).then(function (response) { // At this point, Flask has printed our JSON
  //   return response.text();
  // }).then(function (text) {

  //   alert('POST response: ');

  //   // Should be 'OK' if everything was successful
  //   alert(text);
  // });






  // //**Ajax envoi fichier json */
  // // Select your input type file and store it in a variable
  // const input =$('#fileinput');

  // // This will upload the file after having read it
  // const upload = (file) => {
  //   fetch('/analyse', { // Your POST endpoint
  //     method: 'POST',
  //     body: file // This is your file object
  //   }).then(function (response) { // At this point, Flask has printed our JSON
  //     console.log("ok");
  //     return response.text();
  //   }).then(function (text) {
  //     console.log('POST response: ');
  //     // Should be 'OK' if everything was successful
  //     console.log(text);
  //   });
  // };

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
