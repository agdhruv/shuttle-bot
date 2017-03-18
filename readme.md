# Shuttle Messegner Bot

This is a simple Facebook Messenger bot that I built on a Thursday night for my University Shuttle Service.

Credit for the code to configure the Bot goes to: https://github.com/hartleybrody/fb-messenger-bot. I also used a blog entry by the same author to help me with the configuration. Kudos to @hartleybrody.

I initially cloned the above repository to get everything up and running, and then amended it to give the desired information.

## How does it work?

It uses `binary search` to decide what is the next biggest integer after the integer reresenting the current time in the `list` that contains the shuttle timings.

It uses the time at which the message was **received** by the system, and not the time at which the message was sent by the user.