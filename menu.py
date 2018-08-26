# def get_menu(message_text):

# 	from datetime import datetime, timedelta
	
# 	meal_asked = message_text[5:]

# 	# Get current day to decide which day's menu needs to be sent
# 	my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)
# 	my_day = my_time.strftime('%A')

# 	# Start generating return message:
# 	return_message = "The request was received on " + my_time.strftime('%A, %H:%M') + ".\nHere's the " + meal_asked + " menu for today.\n"

# 	# Get day number -> 1 for Monday, 7 for Sunday
# 	days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
# 	for my_day_number in range(len(days)):
# 	    if my_day == days[my_day_number]:
# 	        break
# 	my_day_number += 1 # to account for 0 indexed list

# 	# Do it meal by meal - simple

# 	if meal_asked == "BREAKFAST":
# 		returned_menu = "\nBreakfast timings are 08:00 to 10:30.\n"

# 		# For breakfast, keep checking till there is a line with an empty string as the first element
# 		with open('menu.csv') as file:
# 		    for line in file:
# 		        values_in_line = line.split(",")
# 		        if (not values_in_line[0].strip()) and (not values_in_line[1].strip()):
# 		            break
# 		        else:
# 		            returned_menu += "\n" + values_in_line[0].strip() + ": " + values_in_line[my_day_number].strip().strip("\"").strip()


# 	elif meal_asked == "LUNCH":
# 		returned_menu = "\nLunch timings are 12:15 to 14:30.\n"
# 		number_of_breaks = 0

# 		# For lunch, start check after number_of_breaks is 1 and end when it is 2
# 		with open('menu.csv') as file:
# 		    for line in file:
# 		        values_in_line = line.split(",")
# 		        if (not values_in_line[0].strip()) and (not values_in_line[1].strip()):
# 		            number_of_breaks += 1
# 		        elif number_of_breaks == 1:
# 		            type_of_dish = values_in_line[0].strip()
# 		            dish = values_in_line[my_day_number].strip().strip("\"").strip()
# 		            if not dish:
# 		                dish = "Nothing"
# 		            else:
# 		                pass
# 		            returned_menu += "\n" + type_of_dish + ": " + dish


# 	elif meal_asked == "SNACKS":
# 		returned_menu = "\nSnacks timings are 16:45 to 18:15.\n"
# 		number_of_breaks = 0

# 		# For snacks, start check after number_of_breaks is 2 and end when it is 3
# 		with open('menu.csv') as file:
# 		    for line in file:
# 		        values_in_line = line.split(",")
# 		        if (not values_in_line[0].strip()) and (not values_in_line[1].strip()):
# 		            number_of_breaks += 1
# 		        elif number_of_breaks == 2:
# 		            type_of_dish = values_in_line[0].strip()
# 		            dish = values_in_line[my_day_number].strip().strip("\"").strip()
# 		            if not dish:
# 		                dish = "Nothing"
# 		            else:
# 		                pass
# 		            returned_menu += "\n" + type_of_dish + ": " + dish

# 	elif meal_asked == "DINNER":
# 		returned_menu = "\nDinner timings are 19:30 to 22:15.\n"
# 		number_of_breaks = 0

# 		# For dinner, start check after number_of_breaks is 3 and end when it is 4
# 		with open('menu.csv') as file:
# 		    for line in file:
# 		        values_in_line = line.split(",")
# 		        if (not values_in_line[0].strip()) and (not values_in_line[1].strip()):
# 		            number_of_breaks += 1
# 		        elif number_of_breaks == 3:
# 		            type_of_dish = values_in_line[0].strip()
# 		            dish = values_in_line[my_day_number].strip().strip("\"").strip()
# 		            if not dish:
# 		            	if (type_of_dish == 'SWEET'):
# 		                	dish = "Excuse me? This is not your home."
# 		                else:
# 		                	dish = "Nothing"
# 		            else:
# 		                pass
# 		            returned_menu += "\n" + type_of_dish + ": " + dish

# 	# ignore non-ascii characters
# 	returned_menu = returned_menu.decode("ascii", errors="ignore").encode()

# 	return_message += returned_menu

# 	# Return the message to callee
# 	return return_message


def get_menu(message_text):

	from datetime import datetime, timedelta
	from pymongo import MongoClient
	import os
	
	meal_asked = message_text[5:]

	# Get current day to decide which day's menu needs to be sent
	my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)
	my_day = my_time.strftime('%A').lower()

	# Start generating return message:
	return_message = "The request was received on " + my_time.strftime('%A, %H:%M') + ".\nHere's the " + meal_asked + " menu for today.\n\n"

	# get the menu for the day from the database
	client = MongoClient(os.environ["MONGODB_URI"] if os.environ.get("MONGODB_URI") else "mongodb://localhost:27017/ashoka-bot")
	db = client.get_default_database()

	meal_menu = db.menus.find_one({"meal": meal_asked.lower()})

	everyday_items = meal_menu['menu']['everyday']
	today_items = meal_menu['menu'][my_day]
	timings = meal_menu['timings']

	for item in everyday_items:
		return_message += item + '\n'

	for item in today_items:
		return_message += item + '\n'

	# insert meal timings from the db
	return_message += "\nMess timings for lunch are: {0}".format(timings)
	
	client.close()

	return return_message

get_menu('MENU LUNCH')



















	