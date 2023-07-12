
const decrementButton = document.getElementById('decrement');
const incrementButton = document.getElementById('increment');
const counterInput = document.getElementById('counter');
const priceElement = document.getElementById('product-price');
const originalPrice = parseFloat(priceElement.textContent);

decrementButton.addEventListener('click', function() {
  const currentValue = parseInt(counterInput.value);
  if (currentValue > 1) {
    counterInput.value = currentValue - 1;
   s
  }
});

incrementButton.addEventListener('click', function() {
  const currentValue = parseInt(counterInput.value);
  counterInput.value = currentValue + 1;
 
});

counterInput.addEventListener('change', function() {

});

function updatePrice() {
  const quantity = parseInt(counterInput.value);
  const totalPrice = originalPrice * quantity;
  priceElement.textContent = totalPrice.toFixed(2);
}




$(document).ready(function() {
  $('.add-to-cart').click(function() {
    var button = $(this);
    var itemId = button.data('item-id');
    var quantity = parseInt($('#counter').val());

    if (!button.hasClass('disabled')) {
      button.addClass('disabled').attr('disabled', 'disabled');

      $.ajax({
        type: 'POST',
        url: '/add_to_cart/' + itemId,
        data: { quantity: quantity }, // Pass the quantity as data
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




