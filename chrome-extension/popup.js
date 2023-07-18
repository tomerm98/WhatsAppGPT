document.getElementById('process-btn').addEventListener('click', () => {
  console.log("button clicked")
  let spinner = document.getElementById('spinner');
  let btn = document.getElementById('process-btn');

  btn.style.display = 'none';
  spinner.style.display = 'block';

  // Read the clipboard data
  navigator.clipboard.readText()
    .then((text) => {
      console.log(`clipboard is: ${text}`)
      processText(text).then((processedText) => {
        console.log("Text has been processed")
        // Open a new tab with a specific URL
        chrome.tabs.create({ url: 'http://www.yourwebsite.com' }, function(tab) {
          // We still need a content script to handle injecting the text into the page
          console.log("Sending tab message")
          chrome.tabs.sendMessage(tab.id, {processedText: processedText});
        });

        btn.style.display = 'block';
        spinner.style.display = 'none';
      });
    });
});

// Process text from clipboard
async function processText(text) {
  return text;
}
