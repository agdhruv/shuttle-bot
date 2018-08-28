def get_shuttle(message_text):
	
	from datetime import datetime, timedelta
	from db_operations.connect import connect
	import os

	origin_asked = message_text[8:]
	schedule_day = ''

	weekdays = ['monday', 'tuesday', 'wednesday', 'thursday']
	holidays = ['saturday', 'sunday']

	# Get current time - time at which message has been received by this script
	my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)
	my_day = my_time.strftime('%A').lower()

	if my_day in weekdays:
		schedule_day = 'weekday'
	elif my_day in holidays:
		schedule_day = 'holiday'
	else:
		schedule_day = 'friday'

	# get schedule from db
	client = connect(os.environ["MONGODB_URI"] if os.environ.get("MONGODB_URI") else "mongodb://localhost:27017/ashoka-bot")
	db = client.get_default_database()

	shuttle_schedule = db.shuttle_schedules.find_one({"origin": origin_asked.lower()})

	route = shuttle_schedule['route']
	today_timings = shuttle_schedule['schedule'][schedule_day]
	phone = shuttle_schedule['phone']

	# Start generating return message
	return_message = "The request was received on {0}.\n\nToday, shuttles will run from {1} at:\n{2}".format(my_time.strftime('%A, %H:%M'), route, today_timings)

	if phone != '':
		return_message += "\n\nGuard at {0}: {1}".format(origin_asked, phone)

	print return_message

	# Return the message to callee
	return return_message


get_shuttle('SHUTTLE METRO')




