document.addEventListener('DOMContentLoaded', function() {
  const stripePublicKey = 'pk_test_51NP8SlAG1w1CkJgYirjkuUL8lP2f0iPg0KVLKWFq4L0piz1cWo9FPppSiMFthKC6PJqjwfGdE3vUWtLd79a2Hkiz00rUtkYZBC';
  const stripe = Stripe(stripePublicKey);
  const elements = stripe.elements();
  const cardElement = elements.create('card');

  cardElement.mount('#card-number');

  document.getElementById('payment-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const paymentAmount = document.getElementById('amount').value;

    fetch('/process_payment_cart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'payment-amount=' + encodeURIComponent(paymentAmount)
    })
    .then(response => response.text())
    .then(clientSecret => {
      // Use the client secret to complete the payment using Stripe.js
      stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: cardElement,
        }
      })
      .then(result => {
        // Handle the payment result
        if (result.error) {
          console.error(result.error.message);
        } else {
           window.location.href="http://localhost:5000/success"
        }
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });

  function showSuccessMessage() {
    const successMessage = document.createElement('div');
    successMessage.textContent = 'Payment succeeded!';
    successMessage.classList.add('success-message');
    document.body.appendChild(successMessage);
  }
});
