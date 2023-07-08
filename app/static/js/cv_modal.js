function openCVModal(cvPath) {
    var cvModal = document.getElementById('cvModal');
    var cvPdf = document.getElementById('cvPdf');

    cvPdf.setAttribute('src', cvPath);
    cvModal.style.display = 'block';
  }

  function closeCVModal() {
    var cvModal = document.getElementById('cvModal');
    cvModal.style.display = 'none';
  }