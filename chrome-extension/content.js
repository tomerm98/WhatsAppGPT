chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  // Wait until the page is fully loaded
  window.onload = function() {
    // Find the textbox and paste the processed text into it
      console.log("TESTINNGGGG CONTENT JSS ***************")
    let textbox = document.querySelector('input[type="text"]'); // Update this selector based on the actual textbox
    if (textbox) {
      textbox.value = request.processedText;
    }
  }
});
