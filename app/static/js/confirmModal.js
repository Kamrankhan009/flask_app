// Open the modal
function openModal(email,declineOrAcept) {
    document.getElementById("modal").style.display = "block";
    var yesButton = document.querySelector(".btn-yes");
    var noButton = document.querySelector(".btn-no");

    yesButton.dataset.param1 = email;
    yesButton.dataset.declineOrAcept = declineOrAcept;
    yesButton.addEventListener("click", handleYesButtonClick, { once: true });
    noButton.addEventListener("click", handleNoButtonClick);
}

function handleYesButtonClick(event) {
    const email = event.target.dataset.param1;
    const declineOrAcept = event.target.dataset.declineOrAcept;
    sendEmail(email,declineOrAcept);
    clearCodeValue();
    
  }

  function handleNoButtonClick() {
    closeModal();

  }
  
  function getCodeValue() {
    var inputValue = document.getElementById("code").value;
    return inputValue;
  }
  function clearCodeValue() {
    document.getElementById("code").value = "";

  }

// Close the modal
function closeModal() {
    document.getElementById("modal").style.display = "none";
}


// Send email request
function sendEmail(email,declineOrAcept) {


    // AJAX request
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_email", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            console.log("Email sent successfully");
        }
    };
    xhr.send(JSON.stringify({ email: email, declineOrAcept:declineOrAcept}));
        // Close the modal after sending email
        closeModal();
}



function verifyCode() {  
  var pw = document.getElementById("code").value;
  var cpw = "1411"
  if (pw !== cpw){
      document.getElementById("codemessage").innerHTML = "**Code not Match!";
      showFlashErrorMessage("**Code not Match!")
      document.getElementById("btn-yes").disabled = true

  }
  else{
      document.getElementById("codemessage").innerHTML = "";
      document.getElementById("btn-yes").disabled = false

  }
}

