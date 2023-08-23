function getPayFormURL(amount) {
    var payLink = document.getElementById('pay-btn');
    payLink.href = `/payment_address?amount=${amount}`;    
}


function getPayFormURL2(amount) {
    var payLink = document.getElementById('pay-btn2');
    payLink.href = `/payment_address?amount=${amount}`;    
}


