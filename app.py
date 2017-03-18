import os
import sys
import json

import requests
from flask import Flask, request, send_from_directory

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
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if message_text.upper()=="SHUTTLE HELP":
                        return_message = "Send \"SHUTTLE CAMPUS\" (without quotes) for timings of next 3 shuttles running from the Ashoka Campus to Jahangirpuri.\n\nSend \"SHUTTLE METRO\" (without quotes) for timings of next 3 shuttles running from Jahangirpuri to Ashoka Campus."
                        send_message(sender_id, return_message)
                    
                    # Configure to tell you schedule at Campus
                    elif message_text.upper()=="SHUTTLE CAMPUS":

                        # Get current time - time at which message has been received by this script
                        from datetime import datetime, timedelta
                        my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)
                        my_day = my_time.strftime('%A')

                        # Start generating return message:
                        return_message = "The request was received on " + my_time.strftime('%A, %H:%M') + ".\n\nThe next three shuttles will run from Ashoka to Jahangirpuri at:"

                        # Convert to integer
                        my_time = int(my_time.strftime('%H%M'))

                        # Make list with times of shuttles
                        if my_day=="Saturday" or my_day=="Sunday":
                            times_campus = [700,730,800,830,900,930,1000,1030,1100,1130,1200,1230,1300,1400,1500,1600,1700,1730,1800,1830,1900,2000,2100,2200,-1]
                        else:
                            times_campus = [630,700,730,800,820,845,900,930,1000,1100,1200,1300,1400,1500,1600,1630,1700,1720,1740,1800,1820,1840,1900,1930,2000,2030,2100,2200,-1]

                        # Use binary search to search for next 3 shuttles
                        low = 0
                        high = len(times_campus) - 1

                        toCheck = my_time

                        while low<high:
                            mid = (low + high)/2
                            if times_campus[mid]==toCheck:
                                low = mid
                                break
                            elif times_campus[mid]>toCheck:
                                high = mid
                            elif times_campus[mid]<toCheck:
                                low = mid + 1
                        ans_index = low

                        for i in range(low,low+3):
                            if times_campus[i] == -1:
                                return_message += "\nNo more shuttles today."
                                break
                            next_shuttle = str(times_campus[i])
                            next_shuttle = next_shuttle[:-2] + ":" + next_shuttle[-2:]
                            return_message += "\n" + next_shuttle

                        # Finally send the message
                        send_message(sender_id, return_message)

                    # Configure to tell you schedule at Jahangirpuri Metro Station
                    elif message_text.upper()=="SHUTTLE METRO":

                        # Get current time - time at which message has been received by this script
                        from datetime import datetime, timedelta
                        my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)
                        my_day = my_time.strftime('%A')

                        # Start generating return message:
                        return_message = "The request was received on " + my_time.strftime('%A, %H:%M') + ".\n\nThe next three shuttles will run from Jahangirpuri to Ashoka at:"

                        # Convert to integer
                        my_time = int(my_time.strftime('%H%M'))

                        # Make list with times of shuttles
                        if my_day=="Saturday" or my_day=="Sunday":
                            times_metro = [800,830,900,930,1000,1030,1100,1200,1300,1400,1500,1600,1700,1800,1830,1900,1930,2000,2030,2100,2130,2200,2230,2300,-1]
                        else:
                            times_metro = [730,800,830,900,920,940,1000,1030,1100,1200,1300,1400,1500,1600,1700,1720,1740,1800,1830,1900,1930,2000,2030,2100,2130,2200,2230,2300,-1]

                        # Use binary search to search for next 3 shuttles
                        low = 0
                        high = len(times_metro) - 1

                        toCheck = my_time

                        while low<high:
                            mid = (low + high)/2
                            if times_metro[mid]==toCheck:
                                low = mid
                                break
                            elif times_metro[mid]>toCheck:
                                high = mid
                            elif times_metro[mid]<toCheck:
                                low = mid + 1
                        ans_index = low

                        for i in range(low,low+3):
                            if times_metro[i] == -1:
                                return_message += "\nNo more shuttles today."
                                break
                            next_shuttle = str(times_metro[i])
                            next_shuttle = next_shuttle[:-2] + ":" + next_shuttle[-2:]
                            return_message += "\n" + next_shuttle

                        return_message += "\n\nGuard at Jahangirpuri: +91 8222930509"

                        # Finally send the message
                        send_message(sender_id, return_message)

                    else:
                        # For the shitty Facebook review process
                        return_message = "Invalid command. Use SHUTTLE HELP to know more commands."
                        send_message(sender_id, return_message)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

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