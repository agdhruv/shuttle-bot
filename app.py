import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    token = "hello_my_name_is_dhruv_agarwal"
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


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

                    if message_text=="SOMETHING":

                        # Get current time - time at which message has been received by this script
                        from datetime import datetime, timedelta
                        my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)

                        # Start generating return message:
                        return_message = "The request was received at " + my_time.strftime('%H:%M') + "\n"

                        # Convert to integer
                        my_time = int(my_time.strftime('%H%M'))

                        # Make list with times of shuttles
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

                        send_message(sender_id, return_message)
                    else:
                        send_message(sender_id, "Don't know what you are talking about.")

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
        "access_token": 'EAAELrXkFF6MBAAibk461aGn1kvbwCjrVwPp4uwZAb6JoJQhBSwfPAZBqRdI9fjqJ1ueHwc7TRtR9CPcm8zUl3ZAwOZAJ6zG4XGIZA22qgwBq21K0JyvoHpSVxikJggUmZB4hlLKjwOTR0nAZBvraMsrDfZBbN8d8kcPZBOzu0eZBPIZBAZDZD'
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
