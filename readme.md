# Shuttle Messegner Bot + Menu Messenger Bot

This is a simple Facebook Messenger bot that I built on a Thursday night.

Credit for the code to configure the Bot goes to: https://github.com/hartleybrody/fb-messenger-bot. I also used a blog entry by the same author to help me with the configuration. Kudos to @hartleybrody.

I initially cloned the above repository to get everything up and running, and then amended it to give the desired information.

## How does it work?

For the shuttle schedule, it uses `binary search` to decide what is the next biggest integer after the integer representing the current time in the `list` that contains the shuttle timings.

For the Menu, it uses file handling with a `.csv` file that holds the menu for each week. The menu for each week will have to be updated manually.

It uses the time at which the message was **received** by the system, and not the time at which the message was sent by the user.

## Commands Allowed

	1. SHUTTLE HELP - Shows the list of commands that you can use for the shuttle service. It includes:
	 - SHUTTLE CAMPUS - Shows timings of next 3 shuttles from Campus to Jahangirpuri.
	 - SHUTTLE METRO - Shows timings of next 3 shuttles from Jahangirpuri to Ashoka.
	2. MENU BREAKFAST
	3. MENU LUNCH
	4. MENU SNACKS
	5. MENU DINNER