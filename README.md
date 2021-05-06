# Project Scope
Construtora SAM's main method of communication is through a Telegram groupchat. At the beginning and end of each shift, workers send various photos of their trucks that show things like license plate number, mileage, equipment, and problems that they might run into. Additionally, when the truck needs to be refueled, they must follow a certain procedure that involves taking photos of the mileage, the amount of gas in the tank, the cost of refueling, as well as the gas station attendant. This process leads to an inconsistent amount of photos sent to the group chat every week and can create a lot of clutter.

The purpose of this bot is to organize the company's refueling procedure by having each driver manually input various information about the truck before and after refueling. The input is then updated to a Google sheet that their manager can then look at and record at the end of the day/week.

# Getting Started
First you will need:
- a Google sheet formatted as shown in *example_sheet.png*
- your own Telegram Bot with a unique token ([tutorial](https://core.telegram.org/bots#3-how-do-i-create-a-bot))

The [python-telegram-bot library](https://github.com/python-telegram-bot/python-telegram-bot) makes it super easy to get started with your own bot. Their page shows you how to install the necessary package and even includes a bunch of examples that you can learn from and gain a deeper understanding of how Telegram bots work. I personally used [conversationbot.py](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py) as a model. **Please note that I stored my bot's API token under the *API_KEY* variable in constants.py, so you should replace that with your own token.**

This [Python tutorial (Your own Bookkeeping Telegram Bot)](https://chatbotslife.com/your-own-bookkeeping-telegram-bot-with-python-561507fc6a02) helped a lot in getting started with the Google Cloud Platform. It has a link to a step-by-step Youtube [tutorial from Tech With Tim](https://www.youtube.com/watch?v=cnPlKLEGR7E) that explains the process perfectly. **Note: You should replace creds.json with your own credentials.**

Once everything is set up you're ready to test it out!

# Available Commands
- */driver* - Change the name of a vehicle's driver.
- */plate* - Change the license plate of a vehicle.
- */refuel* - Begin the refueling procedure.
- */help* - Display the above information.

When each command is called, it starts a "conversation" that first asks the user to pick their vehicle using an inline keyboard. Then, it prompts the user to enter whatever information they wanted to update about the vehicle. When the conversation is over, the Google sheet is updated with the corresponding inputs. The */refuel* command involves more steps:
1. Enter mileage before refueling
2. Enter mileage after refueling
3. Enter the quantity of fuel (in liters)
4. Enter the cost of refueling

**Note: The bot assumes that the company only owns four vehicles, but that's probably not the case. Therefore, you should edit the inline keyboard AND the Google sheet to include the number of vehicles they actually own. You could also ask to see what system they use to keep track of their vehicles (maybe they go by license plate/driver/etc).**

# Switching Between Languages
Since the company is based in Recife, Brazil they'll want the bot to speak to them in Portugese. To tackle this issue, I created separate string variables in **constants.py** to represent what the bot is saying to the user. These variables are used as parameters when *update.message.reply_text()* is called and correspond to the specific command/step used in conversation.

To switch between English and Portugese, simply comment out the block labeled "english version" or "portugese version" and uncomment the block with your preferred language. There are probably better ways to do this, so feel free to change it.

Note: I only used Google Translate to find the Portugese versions and I'm really sorry if some of the sayings are incorrect. Feel free to change that as well!

# Suggestions
This bot definitely has room for improvement given the time span in which it was created. Some of my suggestions are listed below.
- Switching between languages only changes how the bot speaks to the user, not the commands themselves (/refuel, /driver, /plate, /help). Finding a better method of switching languages could possibly include a way for the command names to change as well.
- Add more commands to improve the functionality of the bot. This way it's not limited to just the refueling procedure. You could also keep track of specific workers, teams, equipment, etc. I know there's also a specific procedure for when workers go on break, so incorporating that into the bot is also a possibility.
- Currently workers send their locations to the group chat. python-telegram-bot has a way to save a user's location if you wanted to incorporate that.
- Right now anyone who uses the bot is able to change information about any of the vehicles, so it's not very secure. Telegram Passports can probably help with that, but I haven't looked into it.
- Require numerical values only (for some commands). For example, in the photos provided the user was able to enter the mileages as "ncd" and "chdj."
- Other error handlers
