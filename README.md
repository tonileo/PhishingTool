# PhishingTool

Thunderbird add-on detects phishing in mail messages that are sent with Postfix

## Parts

detect.txt - .txt file where phishing links are located that we want to compare with mail
pokazujeNaSkriptu.desktop - file located on desktop that is behaving like an app. Pointing to skriptaiThunderbird.sh
skriptaPostfix.py - script that compares all mail content of a user with phishing links (detect.txt) and flags them
skriptaiThunderbird.sh - script that start skriptaPostfix.py and thunderbird after
