# PhishingTool

Thunderbird add-on detects phishing in mail messages that are sent with Postfix

## Parts

* detect.txt - .txt file where phishing links are located that we want to compare with mail
* pokazujeNaSkriptu.desktop - file located on desktop that is behaving like an app. Pointing to skriptaiThunderbird.sh
* skriptaPostfix.py - script that compares all mail content of a user with phishing links (detect.txt) and flags them
* skriptaiThunderbird.sh - script that start skriptaPostfix.py and thunderbird after
* addon - folder containing the addon for thunderbird with all necessary files


## Add-on

* manifest.json - the main configuration file in which properties such as name, description, unique identifier (id) are defined and defines how the extension will be attached to Thunderbird.
* background.js - listens to displayed messages in Thunderbird. When a flagged message is detected, the script marks the message as junk and opens a popup window that is created using the popup.html and popup.css files to provide additional notice to the user
* popup.css - contains design for popup.html
* popup.html - small html window that will be displayed when flagged message is detected
