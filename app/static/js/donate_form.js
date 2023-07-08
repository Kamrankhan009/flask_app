  // Create a Stripe instance
  var stripe = Stripe("YOUR_STRIPE_API_KEY");
 // Create a Stripe Elements instance
 var elements = stripe.elements();

 // Create a card Element and mount it to the form
 var card = elements.create('card');
 card.mount('#card-element');

 // Handle form submission
 var form = document.getElementById('payment-form');
 form.addEventListener('submit', function(event) {
   event.preventDefault();

   // Disable the submit button to prevent multiple submissions
   document.querySelector('.btn-primary').disabled = true;

   // Create a payment method using the card element
   stripe.createPaymentMethod({
     type: 'card',
     card: card,
     billing_details: {
       name: document.getElementById('name').value,
       email: document.getElementById('email').value
     }
   }).then(function(result) {
     if (result.error) {
       // Display any errors to the user
       var errorElement = document.getElementById('card-errors');
       errorElement.textContent = result.error.message;

       // Re-enable the submit button
       document.querySelector('.btn-primary').disabled = false;
     } else {
       // Send the payment method and user info to the server
       var formData = new FormData(form);
       formData.append('payment_method', result.paymentMethod.id);
       fetch("/process_payment", {
         method: "POST",
         body: formData
       }).then(function(response) {
         return response.json();
       }).then(function(data) {
         // Handle the response from the server
         console.log(data);
       });
     }
   });
 });