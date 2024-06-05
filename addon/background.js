let iskocniOtvoren = false;

async function awaitIskocni() {
  if (iskocniOtvoren) {
    return;
  }
  iskocniOtvoren = true;

  async function iskocniPrompt(iskocniId, defaultResponse) {
    await messenger.windows.get(iskocniId);

    return new Promise(resolve => {
      let response = defaultResponse;
      function windowRemoveListener(closedId) {
        if (iskocniId == closedId) {
          messenger.windows.onRemoved.removeListener(windowRemoveListener);
          messenger.runtime.onMessage.removeListener(messageListener);
          resolve(response);
        }
      }
      function messageListener(request, sender, sendResponse) {
        if (sender.tab.windowId != iskocniId || !request) {
          return;
        }
        if (request.iskocniResponse) {
          response = request.iskocniResponse;
        }
      }
      messenger.runtime.onMessage.addListener(messageListener);
      messenger.windows.onRemoved.addListener(windowRemoveListener);
    });
  }

  let window = await messenger.windows.create({
    url: "iskocni.html",
    type: "popup",
    height: 280,
    width: 390,
    allowScriptsToClose: true,
  });

  let rv = await iskocniPrompt(window.id, "cancel");
  console.log(rv);
  iskocniOtvoren = false;
}

browser.messageDisplay.onMessageDisplayed.addListener((tab, message) => {
  if (message && message.flagged) {
    browser.messages.update(message.id, { junk: true }).then(() => {
      console.log(`Poruksa s ID: ${message.id} je dodana u smece.`);
      awaitIskocni();
    }).catch(error => {
      console.error("Greska dodavanja u smece:", error);
    });
  }
});