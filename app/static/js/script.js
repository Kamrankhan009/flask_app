function updateCartCount() {
  $.ajax({
    type: 'GET',
    url: '/cart_count',
    success: function(response) {
      $('.cart-count').text(response.count);
    },
    error: function(error) {
      console.log('Error retrieving cart count');
    }
  });
}

$(document).ready(function() {
  // Toggle dropdown content on click
  $('.dropdown-btn').click(function() {
      $(this).next('.dropdown-content').toggle();
  });

  // Close dropdown when clicking outside
  $(document).click(function(event) {
      if (!$(event.target).closest('.dropdown').length) {
          $('.dropdown-content').hide();
      }
  });
});



$(document).ready(function() {
  $('.add-to-cart').click(function() {
    var button = $(this);
    var itemId = button.data('item-id');

    if (!button.hasClass('disabled')) {
      button.addClass('disabled').attr('disabled', 'disabled');

      $.ajax({
        type: 'POST',
        url: '/add_to_cart/' + itemId,
        data: { quantity: 1 }, // Pass the quantity as data
        dataType: 'json',
        success: function(response) {
          updateCartCount();
        },
        error: function(error) {
          alert('Error adding item to cart');
        },
        complete: function() {
          button.removeClass('disabled').removeAttr('disabled');
        }
      });
    }
  });
});





// Set the timeout to remove flash messages after 3 seconds
setTimeout(function() {
  var flashMessages = document.getElementById("flash-messages");
  if (flashMessages) {
    flashMessages.innerHTML = "";
  }
}, 3000);


function showFlashErrorMessage(message) {
  var flashMessageElement = document.getElementById('flash-message');
  flashMessageElement.textContent = message;
  flashMessageElement.style.display = 'block';
  flashMessageElement.classList.add('error');
  // Hide the flash message after 3 seconds
  setTimeout(function() {
    flashMessageElement.style.display = 'none';
  }, 3000);
}
function showFlashSuccessMessage(message) {
  var flashMessageElement = document.getElementById('flash-message');
  flashMessageElement.textContent = message;
  flashMessageElement.style.display = 'block';
  flashMessageElement.classList.add('success');
  // Hide the flash message after 3 seconds
  setTimeout(function() {
    flashMessageElement.style.display = 'none';
  }, 3000);
}