from datetime import datetime, timedelta

def shuttle(message_text):

	# Configure to reply to shuttle help command
	if message_text=="SHUTTLE HELP":
        return_message = "Send \"SHUTTLE CAMPUS\" (without quotes) for timings of next 3 shuttles running from the Ashoka Campus to Jahangirpuri.\n\nSend \"SHUTTLE METRO\" (without quotes) for timings of next 3 shuttles running from Jahangirpuri to Ashoka Campus."
    
    # Configure to tell you schedule at Campus
    elif message_text=="SHUTTLE CAMPUS":

        # Get current time - time at which message has been received by this script
        my_time = datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=30)
        my_day = my_time.strftime('%A')

        # Start generating return message:
        return_message = "The request was received on " + my_time.strftime('%A, %H:%M') + ".\n\nThe next three shuttles will run from Ashoka to Jahangirpuri at:"

        # Convert to integer
        my_time = int(my_time.strftime('%H%M'))

        # Make list with times of shuttles
        if my_day=="Saturday" or my_day=="Sunday":
            times_campus = [700,800,830,900,930,1000,1030,1100,1130,1200,1230,1300,1330,1400,1430,1500,1530,1600,1700,1730,1800,1830,1900,1930,2000,2100,2200,-1]
        elif my_day=="Friday":
            times_campus = [630,645,700,715,730,800,830,900,930,1000,1100,1200,1300,1400,1430,1500,1530,1600,1630,1700,1720,1740,1800,1820,1840,1900,2000,2100,2200,-1]
        else:
            times_campus = [630,645,700,715,730,800,830,900,930,1000,1100,1200,1300,1400,1500,1600,1630,1700,1720,1740,1800,1830,1900,1930,2000,2100,2200,-1]

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
            times_metro = [800,900,930,1000,1030,1100,1200,1230,1300,1330,1400,1430,1500,1530,1600,1700,1800,1830,1900,1930,2000,2030,2100,2130,2200,2245,2300,-1]
        elif my_day=="Friday":
            times_metro = [730,800,820,840,900,920,940,1000,1030,1100,1200,1300,1400,1500,1530,1600,1630,1700,1730,1800,1830,1900,1930,2000,2030,2100,2130,2200,2245,2300,-1]
        else:
            times_metro = [730,800,820,840,900,920,940,1000,1030,1100,1200,1300,1400,1500,1600,1700,1800,1830,1900,1930,2000,2030,2100,2130,2200,2245,2300,-1]

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