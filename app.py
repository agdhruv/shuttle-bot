import os
import sys
import json
import string
import requests
from flask import Flask, request, send_from_directory, jsonify, render_template, abort

import shuttle
import menu
import directory

from db_operations.update_menu import update_menu_in_db
from db_operations.update_shuttle import update_schedule_in_db
from db_operations.connect import connect

app = Flask(__name__, static_url_path='/static')

# serve static file
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# save the menu that comes from the webpage
@app.route('/save_menu', methods = ['POST'])
def save_menu():
    data = request.get_json()

    password = os.environ["admin_password"] if os.environ.get("admin_password") else "whatever"
    
    if (data['password'] != password):
        return jsonify({'error':'Incorrect password'}), 403

    updated_document = update_menu_in_db(data)

    return jsonify(updated_document), 200


# route to show ui form to user to update menu data
@app.route('/update_menu/<meal>', methods = ['GET'])
def update_menu(meal):
    meals = ['breakfast', 'lunch', 'snacks', 'dinner']

    if meal not in meals:
        return abort(400)

    client = connect(os.environ["MONGODB_URI"] if os.environ.get("MONGODB_URI") else "mongodb://localhost:27017/ashoka-bot")
    db = client.get_default_database()

    meal_menu = db.menus.find_one({"meal": meal})

    client.close()

    return render_template('update_menu.html', meal_menu = meal_menu)


# save the menu that comes from the webpage
@app.route('/save_shuttle', methods = ['POST'])
def save_shuttle():
    data = request.get_json()

    password = os.environ["admin_password"] if os.environ.get("admin_password") else "whatever"
    
    if (data['password'] != password):
        return jsonify({'error':'Incorrect password'}), 403
        
    updated_schedule = update_schedule_in_db(data)

    return jsonify(data), 200


# route to show ui form to user to update shuttle schedule data
@app.route('/update_shuttle/<origin>', methods = ['GET'])
def update_shuttle(origin):
    origins = ['campus', 'metro']

    if origin not in origins:
        return abort(400)

    client = connect(os.environ["MONGODB_URI"] if os.environ.get("MONGODB_URI") else "mongodb://localhost:27017/ashoka-bot")
    db = client.get_default_database()

    shuttle_schedule = db.shuttle_schedules.find_one({"origin": origin})

    client.close()

    return render_template('update_shuttle.html', shuttle_schedule = shuttle_schedule)


# handle GET requests on root url
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    token = os.environ["VERIFY_TOKEN"]
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return render_template('index.html'), 200


# handle POST requests on root url
@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:

            webhook_event = entry["messaging"][0]

            if webhook_event.get("postback"): # someone used a postback button to send a message
                sender_id = webhook_event["sender"]["id"]
                recipient_id = webhook_event["recipient"]["id"]
                received_postback = webhook_event["postback"]
                payload = received_postback["payload"]

                # transfer control to function to get relevant data from functions defined in other files
                return_data = get_relevant_data(payload)

                # send the data back to the user once you get it back
                send_message(sender_id, return_data)

            elif webhook_event.get("message"):  # someone sent us a message
                sender_id = webhook_event["sender"]["id"]        # the facebook ID of the person sending you the message
                recipient_id = webhook_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                if "text" in webhook_event["message"]:
                    message_text = webhook_event["message"]["text"]  # the message's text
                else:
                    message_text = "Not text data"

                message_text = message_text.upper() # convert to uppercase to make things easier

                # transfer control to function to get relevant data from functions defined in other files
                return_data = get_relevant_data(message_text)

                # send the data back to the user once you get it back
                send_message(sender_id, return_data)

    return "ok", 200

# pass the text received and return the message to be sent back to the user
def get_relevant_data(message_text):
    shuttle_command_names = ["SHUTTLE HELP", "SHUTTLE CAMPUS", "SHUTTLE METRO"]
    menu_command_names = ["MENU BREAKFAST", "MENU LUNCH", "MENU SNACKS", "MENU DINNER"]
    directory_command_names = ["INFIRMARY", "MAINTENANCE", "HOUSEKEEPING"]


    # First check if the message sent is any of the 3 SHUTTLE commands
    if message_text in shuttle_command_names:
        return_message = shuttle.get_shuttle(message_text)

    # Then check if the message sent is any of the 3 MENU commands
    elif message_text in menu_command_names:
        return_message = menu.get_menu(message_text)

        # wow, that was new :O. Basically, if there are non-ASCII characters, skip them
        printable = set(string.printable)
        filter(lambda x: x in printable, return_message)

    # Then check if the message sent is any of the phone directory commands
    elif message_text in directory_command_names:
        return_message = directory.get_directory(message_text)
    
    # If it is neither of the valid commands
    else:
        # For the shitty Facebook review process
        return_message = "Invalid command. Use the menu at the bottom of this screen to get desired information."

    # Add this message at the end of every message being sent back hehe
    return_message += '\n\nIf you like this bot and have a GitHub account, I\'ll be grateful if you can star the repository here: https://github.com/agdhruv/shuttle-bot'

    return return_message
    

# function to send message to the user that contacted us
def send_message(recipient_id, message_text):

    log("Sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

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


# simple function for logging to stdout on heroku
def log(message):
    print str(message)
    sys.stdout.flush()


# start the server
if __name__ == '__main__':
    app.run(debug=True)



