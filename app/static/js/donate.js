

function getDonateURL(minAmount) {
      var donateLink = document.getElementById('donate-link');
      donateLink.href = `/donate_form?min_amount=${minAmount}`;
      donateLink.style.display = 'block';

}
  
  function regularDonate() {
    document.getElementById("min-amount").innerText = "5";
    document.getElementById("max-amount").innerText = "145";
    var minAmount = document.getElementById('min-amount').innerText;
    var donateLink = document.getElementById('donate-link');

    donateLink.href = "{{ url_for('donate_form', min_amount=" + minAmount + ") }}";
    donateLink.style.backgroundColor = '#ffc107';
    donateLink.style.display = 'block';
    getDonateURL(minAmount);
  }

  function strongDonate() {
    document.getElementById("min-amount").innerText = "150";
    document.getElementById("max-amount").innerText = "∞";

    var minAmount = document.getElementById('min-amount').innerText;
    var donateLink = document.getElementById('donate-link');

    donateLink.href = "{{ url_for('donate_form', min_amount=" + minAmount + ") }}";
    donateLink.style.backgroundColor = '#dc3545';
    donateLink.style.display = 'block';
    getDonateURL(minAmount);
  }