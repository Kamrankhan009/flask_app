const messageElement = document.getElementById('chat-message');
const message = "The answer was within her reach. It was hidden in a box and now that box sat directly in front of her. She'd spent years searching for it and could hardly believe she'd finally managed to find it. She turned the key to unlock the box and then gently lifted the top. She held her breath in anticipation of finally knowing the answer she had spent so much of her time in search of. As the lid came off she could see that the box was empty.";

function displayMessage(messageElement, message) {
  let index = 0;
  let displayText = "";
  let cursorVisible = true;

  function updateDisplay() {
    displayText = message.substr(0, index);
    if (cursorVisible) {
      displayText += "<span class=\"square\"></span>";
    }

    messageElement.innerHTML = displayText;
  }

  function toggleCursor() {
    cursorVisible = !cursorVisible;
    updateDisplay();
  }

  setInterval(toggleCursor, 500); // Adjust blinking speed here (in milliseconds)

  function typeNextCharacter() {
    if (index < message.length) {
      index++;
      updateDisplay();
      setTimeout(typeNextCharacter, 100); // Adjust typing speed here (in milliseconds)
    }
  }

  setTimeout(() => {
    typeNextCharacter();
  }, 2000); // Wait for 2 seconds before typing the message
}

displayMessage(messageElement, message);
