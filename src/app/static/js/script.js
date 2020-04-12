
$(document).ready(function () {
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
