document.addEventListener('DOMContentLoaded', function() {
  const stripePublicKey = 'pk_test_51NP8SlAG1w1CkJgYirjkuUL8lP2f0iPg0KVLKWFq4L0piz1cWo9FPppSiMFthKC6PJqjwfGdE3vUWtLd79a2Hkiz00rUtkYZBC';
  const stripe = Stripe(stripePublicKey);
  const elements = stripe.elements();
  const style = {
    base: {
      fontSize: '20px',
      // color: '#32325d',
      padding: '20px',
      border: '1px solid black' // Add custom padding
    }
  };
  const cardElement = elements.create('card', {style: style});

  cardElement.mount('#card-number');

  document.getElementById('payment-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const paymentAmount = document.getElementById('amount').value;
    const address = document.getElementById('address').value;
    const zip = document.getElementById('zip').value;
    const city = document.getElementById('city').value;
    const state = document.getElementById('state').value;


    const requestBody = new URLSearchParams();
      requestBody.append('payment-amount', paymentAmount);
      requestBody.append('address', address);
      requestBody.append('zip', zip);
      requestBody.append('city', city);
      requestBody.append('state', state);

    fetch('/process_payment_cart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: requestBody.toString()
    })
    .then(response => response.text())
    .then(clientSecret => {
      // Use the client secret to complete the payment using Stripe.js
      stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: cardElement,
          billing_details: {
            address: {
              line1: address,
              postal_code: zip,
              city: city,
              country:"AE" // Replace with the appropriate country code
            }
          }
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
