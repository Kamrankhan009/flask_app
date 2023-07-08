$(document).ready(function() {
    $('.list-item').hover(function() {
      $('.list-item').not(this).css('filter', 'brightness(50%)');
        

    }, function() {
      $('.list-item').css('filter', 'brightness(100%)');
    });
    
  });
  
  $(document).ready(function() {
    $('.list-item').hover(
      function() {
        $('.username').css('color', 'black');
        $('.duration').css('color', 'rgb(4, 28, 48)');
      },
      function() {
        $('.username').css('color', 'rgb(4, 28, 48)');
        $('.duration').css('color', 'rgb(4, 28, 48)');

      }
    );
  });