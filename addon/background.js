let popupOpen = false;

async function awaitPopup() {
  if (popupOpen) {
    return;
  }
  popupOpen = true;

  async function popupPrompt(popupId, defaultResponse) {
    try {
      await messenger.windows.get(popupId);
    } catch (e) {
      return defaultResponse;
    }
    return new Promise(resolve => {
      let response = defaultResponse;
      function windowRemoveListener(closedId) {
        if (popupId == closedId) {
          messenger.windows.onRemoved.removeListener(windowRemoveListener);
          messenger.runtime.onMessage.removeListener(messageListener);
          resolve(response);
        }
      }
      function messageListener(request, sender, sendResponse) {
        if (sender.tab.windowId != popupId || !request) {
          return;
        }
        if (request.popupResponse) {
          response = request.popupResponse;
        }
      }
      messenger.runtime.onMessage.addListener(messageListener);
      messenger.windows.onRemoved.addListener(windowRemoveListener);
    });
  }

  let window = await messenger.windows.create({
    url: "popup.html",
    type: "popup",
    height: 280,
    width: 390,
    allowScriptsToClose: true,
  });

  let rv = await popupPrompt(window.id, "cancel");
  console.log(rv);
  popupOpen = false;
}

browser.messageDisplay.onMessageDisplayed.addListener((tab, message) => {
  if (message && message.flagged) {
    browser.messages.update(message.id, { junk: true }).then(() => {
      console.log(`Message with ID: ${message.id} marked as junk.`);
      awaitPopup();
    }).catch(error => {
      console.error("Failed to mark message as junk:", error);
    });
  }
});