import os
import sys
import json
import string
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
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]  # the message's text
                    else:
                        message_text = "Not identified"

                    message_text = message_text.upper() # convert to uppercase to make things easier

                    shuttle_command_names = ["SHUTTLE HELP","SHUTTLE CAMPUS","SHUTTLE METRO"]
                    menu_command_names = ["MENU BREAKFAST","MENU LUNCH","MENU SNACKS","MENU DINNER"]

                    ######## THIS POINT ONWARDS FOR THE SHUTTLE PART OF THE APPLICATION ########

                    # First check if the message sent is any of the 3 SHUTTLE commands
                    if message_text in shuttle_command_names:

                        if message_text=="SHUTTLE HELP":
                            return_message = "Send \"SHUTTLE CAMPUS\" (without quotes) for timings of next 3 shuttles running from the Ashoka Campus to Jahangirpuri.\n\nSend \"SHUTTLE METRO\" (without quotes) for timings of next 3 shuttles running from Jahangirpuri to Ashoka Campus."
                            send_message(sender_id, return_message)
                        
                        # Configure to tell you schedule at Campus
                        elif message_text=="SHUTTLE CAMPUS":

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
                                times_campus = [700,730,800,830,900,920,940,1000,1020,1040,1100,1120,1140,1200,1220,1240,1300,1400,1500,1600,1700,1730,1800,1830,1900,1930,2000,2100,2200,-1]
                            elif my_day=="Friday":
                                times_campus = [630,700,720,740,800,820,840,900,930,1000,1100,1200,1300,1400,1430,1500,1530,1600,1630,1700,1720,1740,1800,1820,1840,1900,1930,2000,2100,2200,-1]
                            else:
                                times_campus = [630,700,720,740,800,820,840,900,930,1000,1100,1200,1300,1400,1500,1600,1630,1700,1720,1740,1800,1820,1840,1900,1930,2000,2100,2200,-1]

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
                        elif message_text=="SHUTTLE METRO":

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
                                times_metro = [800,830,900,930,1000,1020,1040,1100,1120,1140,1200,1300,1400,1500,1600,1630,1700,1730,1800,1830,1900,1930,2000,2030,2100,2130,2200,2245,2300,-1]
                            elif my_day=="Friday":
                                times_metro = [730,800,820,840,900,920,940,1000,1030,1100,1200,1300,1400,1500,1530,1600,1630,1700,1730,1800,1830,1900,1930,2000,2030,2100,2130,2200,2245,2300,-1]
                            else:
                                times_metro = [730,800,820,840,900,920,940,1000,1030,1100,1200,1300,1400,1500,1600,1700,1730,1800,1830,1900,1930,2000,2030,2100,2130,2200,2245,2300,-1]

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
            
                    ######## THIS POINT ONWARDS FOR THE MENU PART OF THE APPLICATION ########
                    
                    # First check if the menu of any meal has been asked
                    elif message_text in menu_command_names:
                        meal_asked = message_text[5:]

                        # Get current day to decide which day's menu needs to be sent
                        from datetime import datetime, timedelta
                        my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)
                        my_day = my_time.strftime('%A')

                        # Start generating return message:
                        return_message = "The request was received on " + my_time.strftime('%A, %H:%M') + ".\nHere's the " + meal_asked + " menu for today.\n"

                        # Get day number -> 1 for Monday, 7 for Sunday
                        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
                        for my_day_number in range(len(days)):
                            if my_day == days[my_day_number]:
                                break
                        my_day_number += 1

                        # Do it meal by meal - simple

                        if meal_asked == "BREAKFAST":
                            returned_menu = "\nBreakfast timings are 07:30 to 10:15.\n"
                            # For breakfast, keep checking till there is a line with an empty string as the first element
                            with open('menu.csv') as file:
                                for line in file:
                                    values_in_line = line.split(",")
                                    if (not values_in_line[0].strip()) and (not values_in_line[1].strip()):
                                        break
                                    else:
                                        returned_menu += "\n" + values_in_line[0].strip() + ": " + values_in_line[my_day_number].strip().strip("\"").strip()

                        elif meal_asked == "LUNCH":
                            returned_menu = "\nLunch timings are 12:15 to 14:30.\n"
                            number_of_breaks = 0
                            # For lunch, start check after number_of_breaks is 1 and end when it is 2
                            with open('menu.csv') as file:
                                for line in file:
                                    values_in_line = line.split(",")
                                    if (not values_in_line[0].strip()) and (not values_in_line[1].strip()):
                                        number_of_breaks += 1
                                    elif number_of_breaks == 1:
                                        type_of_dish = values_in_line[0].strip()
                                        dish = values_in_line[my_day_number].strip().strip("\"").strip()
                                        if not dish:
                                            dish = "Nothing"
                                        else:
                                            pass
                                        returned_menu += "\n" + type_of_dish + ": " + dish

                        elif meal_asked == "SNACKS":
                            returned_menu = "\nSnacks timings are 16:45 to 18:15.\n"
                            number_of_breaks = 0
                            # For snacks, start check after number_of_breaks is 2 and end when it is 3
                            with open('menu.csv') as file:
                                for line in file:
                                    values_in_line = line.split(",")
                                    if (not values_in_line[0].strip()) and (not values_in_line[1].strip()):
                                        number_of_breaks += 1
                                    elif number_of_breaks == 2:
                                        type_of_dish = values_in_line[0].strip()
                                        dish = values_in_line[my_day_number].strip().strip("\"").strip()
                                        if not dish:
                                            dish = "Nothing"
                                        else:
                                            pass
                                        returned_menu += "\n" + type_of_dish + ": " + dish

                        elif meal_asked == "DINNER":
                            returned_menu = "\nDinner timings are 19:30 to 22:15.\n"
                            number_of_breaks = 0
                            # For dinner, start check after number_of_breaks is 3 and end when it is 4
                            with open('menu.csv') as file:
                                for line in file:
                                    values_in_line = line.split(",")
                                    if (not values_in_line[0].strip()) and (not values_in_line[1].strip()):
                                        number_of_breaks += 1
                                    elif number_of_breaks == 3:
                                        type_of_dish = values_in_line[0].strip()
                                        dish = values_in_line[my_day_number].strip().strip("\"").strip()
                                        if not dish:
                                            dish = "Nothing"
                                        else:
                                            pass
                                        returned_menu += "\n" + type_of_dish + ": " + dish

                        return_message += string.printable(str(returned_menu))

                        # Finally send the message
                        send_message(sender_id, return_message)

                    else:
                        # For the shitty Facebook review process
                        return_message = "Invalid command. Use SHUTTLE HELP to know more SHUTTLE commands.\nUse MENU LUNCH to know the mess menu for the day. Similarly, you can use commands for breakfast, snacks and lunch too."
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