const arabicMessageElement = document.getElementById('arabic-message');
const englishMessageElement = document.getElementById('english-message');

const arabicText = arabic_text;


const englishText = english_text;

const message = arabicText + "<br><br>" + englishText;

function displayMessage(messageElement, message, callback) {
  let index = 0;
  let displayText = "";
  let cursorVisible = true;
  let blinkingInterval;

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

  blinkingInterval = setInterval(toggleCursor, 500); // Adjust blinking speed here (in milliseconds)

  function typeNextCharacter() {
    if (index < message.length) {
      index++;
      updateDisplay();
      setTimeout(typeNextCharacter, speed); // Adjust typing speed here (in milliseconds)
    } else {
      clearInterval(blinkingInterval); // Stop the cursor blinking
      callback(); // Call the callback function when typing finishes
    }
  }

  setTimeout(() => {
    typeNextCharacter();
  }, 2000); // Wait for 2 seconds before typing the message
}

// Display the Arabic text first and then display the English text after it finishes
displayMessage(arabicMessageElement, arabicText, () => {
  displayMessage(englishMessageElement, englishText, () => {
    // Both messages have finished typing
    console.log("Finished typing both messages.");
  });
});
