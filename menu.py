def get_menu(message_text):

	from datetime import datetime, timedelta
	from db_operations.connect import connect
	import os
	
	meal_asked = message_text[5:]

	# Get current day to decide which day's menu needs to be sent
	my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)
	my_day = my_time.strftime('%A').lower()

	# Start generating return message:
	return_message = "The request was received on " + my_time.strftime('%A, %H:%M') + ".\nHere's the " + meal_asked + " menu for today.\n\n"

	# get the menu for the day from the database
	client = connect(os.environ["MONGODB_URI"] if os.environ.get("MONGODB_URI") else "mongodb://localhost:27017/ashoka-bot")
	db = client.get_default_database()

	meal_menu = db.menus.find_one({"meal": meal_asked.lower()})

	everyday_items = meal_menu['menu']['everyday']
	today_items = meal_menu['menu'][my_day]
	timings = meal_menu['timings']

	for item in everyday_items:
		return_message += item + '\n\n'

	for item in today_items:
		return_message += item + '\n'

	# insert meal timings from the db
	return_message += "\nMess timings for lunch are: {0}".format(timings)

	client.close()

	return return_message

# get_menu('MENU SNACKS')




	