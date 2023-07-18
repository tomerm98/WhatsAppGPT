document.getElementById('process-btn').addEventListener('click', () => {
  console.log("button clicked")
  const spinner = document.getElementById('spinner');
  const btn = document.getElementById('process-btn');

  btn.style.display = 'none';
  spinner.style.display = 'block';

  

  // Read the clipboard data
//   console.log(navigator.clipboard)
//   navigator.clipboard.readText()
//     .then((text) => {
//       console.log(`clipboard is: ${text}`)
//       // Open a new tab with a specific URL
//       chrome.tabs.create({ url: 'http://www.yourwebsite.com' }, function(tab) {
//         // We still need a content script to handle injecting the text into the page
//         console.log("Sending tab message")
//         chrome.tabs.sendMessage(tab.id, {processedText: processedText});
//       });
//
//       btn.style.display = 'block';
//       spinner.style.display = 'none';
//     });


});

const readClipboard = () =>{
  const placeholder = document.createElement("input");
  document.body.appendChild(placeholder);
  placeholder.focus();
  document.execCommand("paste");
  const clipboardText = placeholder.value;
  document.body.removeChild(placeholder);
  return clipboardText;
}
