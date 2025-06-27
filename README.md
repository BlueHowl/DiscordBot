# Becode Discord Bot

## Overview

The **Becode Discord Bot** is designed to assist learners at Becode with a variety of tasks, including:
- Automated check-ins and check-outs on the Moodle platform.
- Providing support with questions related to data science, data analysis, and Python.
- Sending birthday wishes to users.
- Displaying the current time and reminding users of upcoming events like check-ins and breaks.

The bot is powered by **Google Gemini** for intelligent responses and also utilizes **Discord.py** for the bot framework. It also integrates the **APScheduler** library for scheduling messages.

## Features

- **Automated Messages**:
  - Check-in and check-out reminders.
  - Break-time and lunch-time reminders.
  - Daily birthday wishes.
  
- **User Assistance**:
  - Responds to data science, data analysis, and Python-related queries.
  - Provides time information and upcoming event reminders.
  
- **Moodle Integration**:
  - Direct links to Moodle check-in/check-out pages for Becode learners.
  
- **Customizable Roles and Channels**:
  - Supports multiple channels (AI, WebDev) for personalized reminders.

- **Gemini Integration**:
  - Smart and witty responses powered by **Google Gemini**.
  
## Prerequisites

Before running the bot, ensure you have the following dependencies:

- **Python 3.x** (preferably Python 3.8+)
- **Discord.py**: To interact with the Discord API.
- **APScheduler**: To schedule timed events like check-ins, breaks, etc.
- **dotenv**: To load environment variables from `.env` files.
- **Google Gemini API**: For intelligent responses.

### Install dependencies

You can install the necessary dependencies using `pip install -r requirements.txt`

### Build project

You can build the project using docker by building the dockerfile using `docker build -t discord-bot .`

To run your newly built container you can use (e.g : `docker run -d --name discord-bot-container discord-bot  `)

## Commands
	•	/time: Displays the current time.
	•	The bot will respond to messages that mention it, answering questions about time and providing other helpful information related to learning at Becode.

  • `/happy-birthdays` - Check for birthdays today

  • `/next-birthdays` - Check for birthdays in the next 7 days

## Customizations

You can modify the following parameters in the bot:
- Check-in, Check-out, Break, and Lunch Times: Modify the checkin_times, checkout_times, break_time, and lunch_time variables to change the schedule.
- Birthday Reminders: Add or modify users in the birthdays dictionary to send birthday wishes to specific users.

### Logging

Logging is enabled to track the bot’s activity and any errors that occur. Logs are output to the console.

### Troubleshooting

If you encounter any issues, check the following:
- Ensure that your environment variables are correctly set in the .env file.
- Check that your bot has the necessary permissions in your Discord server to send messages and manage roles.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
