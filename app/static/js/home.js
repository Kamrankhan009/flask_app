const arabicMessageElement = document.getElementById('arabic-message');
const englishMessageElement = document.getElementById('english-message');

const arabicText = `مرحبًا بكم في موقع الويب الخاص بسيرفر <span style="color:yellow">"FORTPLAY"</span>، حيث يمكنكم شراء المنتجات الخاصة بالسيرفر هنا. يمكنكم أيضًا من خلال الموقع رؤية ترتيبكم في البطولة، وأيضًا معرفة أكثر 10 أشخاص جالسين في غرف السيرفر ومدة وجودهم فيها. نحن نوظف المحترفين لصالح المتجر، حيث يمكنهم الحصول على وظيفة معنا. يحتوي الموقع على صفحة لإرسال الدعم للسيرفر، ومن خلاله يمكنكم دعم السيرفر بمبلغ مادي، وسيكرمكم سيرفرنا على الديسكورد برتبة تليق بكم. <br><br>
<div style="text-align: center;">
  <span style="color: red; font-size: 40px;">
    <b>يرجى ملاحظة أن هذا السيرفر تم تصميمه لنشر السعادة بينكم.</b>
    </span>
  </div>`;

const englishText = `Welcome to the <span style="color:yellow">"FORTPLAY"</span> server website, here you can purchase server related products. Through the site, you can also see your ranking in the tournament, as well as checking the top 10 people with the most time in the server rooms and the duration of their presence in them. We also offer jobs at the website, as we hire professionals for the shop. You can also send support to our server through the support page in the website, and through it you can support the server with a sum of money, and our server will honor you on Discord with the supporter badge of you.

Additionally, we offer tournaments throughout the month with substantial prize pools to support professional players. Even if you are not a professional player in the game, there are events in which you can participate and win cash prizes.

We seek to create a suitable place for Fortnite players, where they can communicate with each other on the <span style="color:yellow">"FORTPLAY"</span> discord server and offer tournaments to encourage professional players, and we also offer events to make the server fun for everyone. We also provide business opportunities for those who seek opening a clan in our server, where they can get financial income.

<br><br>
<div style="text-align: center;">
  <span style="color: red; font-size: 40px;">
    <b>
      Please note that this server is created to spread happiness among players.
    </b>
  </span>
</div>`;

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
      setTimeout(typeNextCharacter, 2); // Adjust typing speed here (in milliseconds)
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
