function getPayFormURL(amount) {
    var payLink = document.getElementById('pay-btn');
    payLink.href = `/cart_payment_form?amount=${amount}`;    
}

