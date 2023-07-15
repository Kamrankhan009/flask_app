const messageElement = document.getElementById('chat-message');
// const arabicText = `مرحبًا بكم في موقع الويب الخاص بسيرفر "FORTPLAY"، حيث يمكنكم شراء المنتجات الخاصة بالسيرفر هنا. يمكنكم أيضًا من خلال الموقع رؤية ترتيبكم في البطولة، وأيضًا معرفة أكثر 10 أشخاص جالسين في غرف السيرفر ومدة وجودهم فيها. نحن نوظف المحترفين لصالح المتجر، حيث يمكنهم الحصول على وظيفة معنا. يحتوي الموقع على صفحة لإرسال الدعم للسيرفر، ومن خلاله يمكنكم دعم السيرفر بمبلغ مادي، وسيكرمكم سيرفرنا على الديسكورد برتبة تليق بكم. <span style="color: #936EC4;">يرجى ملاحظة أن هذا السيرفر تم تصميمه لنشر السعادة بينكم.</span>`;

const arabicText = `مرحبًا بكم في موقع الويب الخاص بسيرفر "<span style="color: #FFD700;">FORTPLAY</span>"، حيث يمكنكم شراء المنتجات الخاصة بالسيرفر هنا. يمكنكم أيضًا من خلال الموقع رؤية ترتيبكم في البطولة، وأيضًا معرفة أكثر 10 أشخاص جالسين في غرف السيرفر ومدة وجودهم فيها. نحن نوظف المحترفين لصالح المتجر، حيث يمكنهم الحصول على وظيفة معنا. يحتوي الموقع على صفحة لإرسال الدعم للسيرفر، ومن خلاله يمكنكم دعم السيرفر بمبلغ مادي، وسيكرمكم سيرفرنا على الديسكورد برتبة تليق بكم. <br><span style="color: #936EC4;">يرجى ملاحظة أن هذا السيرفر تم تصميمه لنشر السعادة بينكم.</span>`;

const englishText = `Welcome to the "<span style="color: #FFD700;">FORTPLAY</span>" server website, here you can purchase server related products. Through the site, you can also see your ranking in the tournament, as well as checking the top 10 people with the most time in the server rooms and the duration of their presence in them. We also offer jobs at the website, as we hire professionals for the shop. You can also send support to our server through the support page in the website, and through it you can support the server with a sum of money, and our server will honor you on Discord with the supporter badge of you.

Additionally, we offer tournaments throughout the month with substantial prize pools to support professional players. Even if you are not a professional player in the game, there are events in which you can participate and win cash prizes.

We seek to create a suitable place for Fortnite players, where they can communicate with each other on the "<span style="color: #FFD700;">FORTPLAY</span>" discord server and offer tournaments to encourage professional players, and we also offer events to make the server fun for everyone. We also provide business opportunities for those who seek opening a clan in our server, where they can get financial income.

Please note that this server is created to spread happiness among players.`;


// const englishText ="";

const message = arabicText + "<br><br>" + englishText;
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
