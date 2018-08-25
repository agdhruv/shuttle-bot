def get_directory(message_text):

	from datetime import datetime, timedelta

	# Get current time - time at which message has been received by this script
	my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)

	# Start generating return message
	return_message = "The request was received on " + my_time.strftime('%A, %H:%M') + ".\n\n" + message_text + " contact details:\n"


	# Configure to reply to INFIRMARY command
	if message_text=="INFIRMARY":
		return_message += "+91 8199977073\n01302300550\n\nBoth these numbers are active 24/7."
    
	# Configure to reply to MAINTENANCE command
	elif message_text=="MAINTENANCE":
		return_message += "+91 8199977074\n01302300429\n\nBoth these numbers are active 24/7."

	# Configure to reply to HOUSEKEEPING command
	elif message_text=="HOUSEKEEPING":
		return_message += "+91 86859222791 (Active 24/7)\n01302300203 (9:30am to 6:00pm)"


	# Return the message to callee
	return return_message


# print get_directory("HOUSEKEEPING")