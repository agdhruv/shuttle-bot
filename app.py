import os
import sys
import json
import string
import requests
from flask import Flask, request, send_from_directory

import shuttle
import menu
import directory

app = Flask(__name__)


@app.route('/<path:path>')
def send_txt(path):
    return send_from_directory('', path)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    token = os.environ["VERIFY_TOKEN"]
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return 'Hello World', 200

@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]  # the message's text
                    else:
                        message_text = "Not identified"

                    message_text = message_text.upper() # convert to uppercase to make things easier

                    shuttle_command_names = ["SHUTTLE HELP","SHUTTLE CAMPUS","SHUTTLE METRO"]
                    menu_command_names = ["MENU BREAKFAST","MENU LUNCH","MENU SNACKS","MENU DINNER"]
                    directory_command_names = ["INFIRMARY", "MAINTENANCE", "HOUSEKEEPING"]

                    # First check if the message sent is any of the 3 SHUTTLE commands
                    if message_text in shuttle_command_names:
                        return_message = shuttle.get_shuttle(message_text)
                        return_message += '\n\nIf you like this bot and have a GitHub account, I\'ll be grateful if you can star the repository here: https://github.com/agdhruv/shuttle-bot'
                        send_message(sender_id, return_message)
                    
                    # Then check if the message sent is any of the 3 MENU commands
                    elif message_text in menu_command_names:

                        # return_message = menu.get_menu(message_text)

                        # wow, that was new :O. Basically, if there are non-ASCII characters, skip them
                        printable = set(string.printable)
                        filter(lambda x: x in printable, return_message)

                        # Finally send the message
                        return_message += '\n\nIf you like this bot and have a GitHub account, I\'ll be grateful if you can star the repository here: https://github.com/agdhruv/shuttle-bot'
                        send_message(sender_id, "The bot is currently under maintenance.")
                        # send_message(sender_id, return_message)

                    # Then check if the message sent is any of the directory commands
                    elif message_text in directory_command_names:
                        return_message = directory.get_directory(message_text)
                        return_message += '\n\nIf you like this bot and have a GitHub account, I\'ll be grateful if you can star the repository here: https://github.com/agdhruv/shuttle-bot'
                        send_message(sender_id, return_message)

                    # If it is neither of the valid commands
                    else:
                        # For the shitty Facebook review process
                        return_message = "Invalid command.\n\n1. SHUTTLE HELP to know more SHUTTLE commands.\n2. MENU BREAKFAST (LUNCH, SNACKS, DINNER) for mess menu.\n3. INFIRMARY, MAINTENANCE, HOUSEKEEPING for contact details."
                        return_message += '\n\nIf you like this bot and have a GitHub account, I\'ll be grateful if you can star the repository here: https://github.com/agdhruv/shuttle-bot'
                        send_message(sender_id, return_message)

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)