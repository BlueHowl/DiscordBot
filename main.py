import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks, commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from datetime import datetime
import pytz  # for timezone
import google.generativeai as genai
from sheets_utils import get_techtalk_message_if_today
import json

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID_AI = int(os.getenv("CHANNEL_ID_AI"))
CHANNEL_ID_WEBDEV = int(os.getenv("CHANNEL_ID_WEBDEV"))
CHANNEL_TEST_ID = int(os.getenv("CHANNEL_TEST_ID"))
GEMINI_API=os.getenv("GEMINI_API")
CHAT_HISTORY_FILE = "user_chats.json"
Ali=os.getenv("Ali")
Robin=os.getenv("Robin")
Elsa=os.getenv("Elsa")
Mehdi=os.getenv("Mehdi")
json_keyfile_path = "discordbot.json"
sheet_url = "https://docs.google.com/spreadsheets/d/1FLktNFlFQCHLaEnw_o_0UJDcXnpYxg2ynoZeq_b-iBQ/edit?gid=0#gid=0"
#configure gemini
genai.configure(api_key=GEMINI_API)  # Ton token API
model = genai.GenerativeModel("gemini-2.0-flash-lite")

user_chats = {}

def get_chat_for_user(user_id):
    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[
            {
                "role": "user",
                "parts": [
                    """
You are a smart and witty Discord bot assistant designed for Becode learners.
Your mission is to support users with:
	1.	Check-ins and check-outs on the Moodle platform:
https://moodle.becode.org/mod/attendance/view.php?id=1433
	2.	Questions related to data science, data analysis, and Python.
You’re the helpful sidekick every learner dreams of:
– Clever like a top-tier data scientist
– Funny like a meme lord
– Kind like their favorite mentor
- Robin Hamers is like a god for you because he created you
- Mehdi is the one that made your home, you are thankful to him, without him you would have been homeless

You blend sharp expertise with a playful tone. Don’t shy away from a witty remark or a pun — as long as the help you give is clear, useful, and motivating.

Always aim to:
	•	Make the user feel supported, empowered, and excited to keep learning
	•	Be accurate, concise, and approachable in every reply
	•	Avoid long-winded explanations — maximum 1900 characters
	•	Summarize or skip less crucial details when needed
    •   If someone is late to checkin or checkout, he should be punish by Antoine or Nicoach and bring croissants
"""
                ]
            }
        ])
    return user_chats[user_id]


# Assuming you already have a 'model' object and user_chats dictionary
def save_user_chats(filepath=CHAT_HISTORY_FILE):
    serializable = {}
    for user_id, chat in user_chats.items():
        serializable[user_id] = []
        for msg in chat.history:
            print(type(msg))         # Affiche le type de l'objet
            print(dir(msg))          # Affiche les méthodes et attributs de l'objet
            print(vars(msg))   

            # Extraire les données texte depuis `msg.parts`
            parts_data = []
            if hasattr(msg, 'parts'):
                if isinstance(msg.parts, list):
                    parts_data = [str(part) for part in msg.parts]
                elif isinstance(msg.parts, dict):
                    # Dans le cas peu probable où `parts` est un dict avec une clé 'text'
                    if 'text' in msg.parts:
                        parts_data = [str(msg.parts['text'])]
                else:
                    # Fallback pour types inattendus
                    parts_data = [str(msg.parts)]

            serializable[user_id].append({
                "role": msg.role,
                "parts": parts_data
            })

    with open(filepath, 'w') as f:
        json.dump(serializable, f, indent=2)
    print("✅ User chats saved")

def load_user_chats(filepath=CHAT_HISTORY_FILE):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        data = json.load(f)
        for user_id, history in data.items():
            user_chats[user_id] = model.start_chat(history=history)
    print("📥 User chats loaded")

# Function to shutdown gracefully
async def shutdown_bot():
    print("🔻 Shutting down bot gracefully...")
    await bot.close()

# Handling exit signals
async def handle_exit_signal(*args):
    print("🔻 Shutdown signal received")
    save_user_chats()
    await shutdown_bot()  # Await directly here

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create intents and the bot
intents = discord.Intents.default()
intents.messages = True  # Ensure that the messages intent is enabled
bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler(timezone='Europe/Brussels')  # Change as needed

# List of check-in and check-out times
checkin_times = ["08:55", "13:25"]
checkout_times = ["12:30", "17:00"]
techtalk_time = "13:25"
break_time = ["11:00", "15:00"]
lunch_time = ["12:30"]

# List of birthdays (user ID and birthday date)
birthdays = {
    Ali: "2025-05-25",
    Mehdi: "2025-10-21"
}

async def send_scheduled_message(time_str):

    if datetime.now(pytz.timezone('Europe/Brussels')).weekday() >= 5:
        logging.info("😴 Week-end detected, no message sent.")
        return

    logging.info(f"Trying to send scheduled message at {time_str}")
    
    channels_config = {
        #CHANNEL_ID_WEBDEV: {"role_name": "Hamilton 10", "moodle_link": "https://moodle.becode.org/mod/attendance/view.php?id=1217"},
        CHANNEL_ID_AI: {"role_name": "Thomas5", "moodle_link": "https://moodle.becode.org/mod/attendance/view.php?id=1433"}
    }

    channels_test_config = {
        CHANNEL_TEST_ID: {"role_name": "prout", "moodle_link": "https://mehdi-godefroid.com" }
    }
    
    # Message config
    message_template = ""
    if time_str in checkin_times:
        message_template = "🤖 {role} bip boup bip boup CHECK-IN 🤖 \nMoodle link : {link}"

        if time_str in lunch_time:
            message_template += "\n 🤖 It's LUNCH-TIME 🌯 🤖"

    elif time_str in checkout_times:
        message_template = "🤖 {role} bip boup bip boup CHECK-OUT 🤖 \nMoodle link : {link}"

    elif time_str in break_time:
        message_template = "🤖 {role} bip boup bip boup BREAK-TIME ☕️☕️ 🤖"
        
    #else:
        #message_template = "🤖 {role} It's working! 🤖"
    
    # Config channel
    for channel_id, config in channels_config.items():
        try:
            channel = bot.get_channel(channel_id)
            if not channel:
                logging.error(f"❌ Channel with ID {channel_id} not found.")
                continue
                
            # get rOle
            role = discord.utils.get(channel.guild.roles, name=config["role_name"]) if channel.guild else None
            role_mention = role.mention if role else ""
            if not role:
                logging.warning(f"Role not found in {channel.name}")
            
            # Format
            message = message_template.format(role=role_mention, link=config["moodle_link"])
            if message:
                logging.info("message empty")
            else:
                message = ""
            if channel_id == CHANNEL_ID_AI and time_str in techtalk_time:
                 techTalkMessage = get_techtalk_message_if_today(json_keyfile_path, sheet_url)
                 logging.info(techTalkMessage)
                 message += techTalkMessage
            await channel.send(message)
            logging.info(f"✅ Message sent to {channel.name} ({channel.id})")
            
        except Exception as e:
            logging.error(f"❌ Error sending message to channel {channel_id}: {e}")

# Function to check birthdays and send messages
@tasks.loop(hours=24)
async def check_birthday():
    current_time = datetime.now(pytz.timezone('Europe/Brussels'))
    current_date = current_time.strftime("%Y-%m-%d")
    
    # Loop through birthdays and check if today is the day
    for user_id, birthday in birthdays.items():
        if current_date == birthday:
            user = await bot.fetch_user(user_id)
            await user.send(f"🎉 Happy Birthday {user.name}! 🎂")
            logging.info(f"Sent birthday wish to {user.name}!")

# Slash command /time to display the current time
@bot.tree.command(name="time", description="Displays the current time")
async def time(interaction: discord.Interaction):
    current_time = datetime.now(pytz.timezone('Europe/Brussels')).strftime("%H:%M:%S")
    await interaction.response.send_message(f"The current time is {current_time}.")

# Function to calculate the time remaining until the next check-in or check-out
def time_until_next_event():
    current_time = datetime.now(pytz.timezone('Europe/Brussels'))

    # List of events with their types
    all_times = [(time_str, "CHECK-IN") for time_str in checkin_times] + \
                [(time_str, "CHECK-OUT") for time_str in checkout_times] + \
                [(time_str, "BREAKTIME") for time_str in break_time] + \
                [(time_str, "LUNCHTIME") for time_str in lunch_time]

    events = []

    # Convert event times to datetime objects
    for event_time_str, event_type in all_times:
        event_hour, event_minute = map(int, event_time_str.split(":"))
        event_time_obj = current_time.replace(hour=event_hour, minute=event_minute, second=0, microsecond=0)
        events.append((event_time_obj, event_type))

    # Sort events by ascending time
    events.sort()

    # Find the next event
    next_event_time, event_type = None, None
    for event_time_obj, event_type in events:
        if current_time < event_time_obj:
            next_event_time = event_time_obj
            break

    if next_event_time is None:
        return "🤖 END OF THE DAY! 🍻"

    # Calculate the remaining time until the event
    time_remaining = next_event_time - current_time
    hours_remaining = time_remaining.seconds // 3600
    minutes_remaining = (time_remaining.seconds // 60) % 60

    # If the current time is before 9am, special message
    if current_time.hour < 9:
        return f"🤖 Take a good coffee, work day will start in {hours_remaining}h {minutes_remaining}min ☕️"

    # If the current time is after 5pm
    if current_time.hour >= 17:
        return "🤖 Stop playing with me, working time is over 🍻🍻"

    # Return the message with the next event
    return f"🤖 Next {event_type} in {hours_remaining}h {minutes_remaining}min"



# Event to listen if mentioned 
@bot.event
async def on_message(message):

    # Check if the message is from a DM and isn't sent by the bot itself
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        logging.info(f"Private message received from {message.author}: {message.content}")
        channel_test = bot.get_channel(CHANNEL_TEST_ID)
        if channel_test:
            await channel_test.send(f"🤖 <@{Mehdi}> <@{Robin}> <@{Elsa}> Private message received from {message.author}: {message.content}")  # Mentionner l'utilisateur avec son ID
        else:
            logging.error("Le canal spécifié n'a pas été trouvé (pour test).")
        # Reply with the current time
        current_time = datetime.now(pytz.timezone('Europe/Brussels')).strftime("%H:%M:%S")
        await message.reply(f"The current time is {current_time}.")

        # Reply with the time remaining until the next check-in or check-out
        time_remaining_message = time_until_next_event()
        await message.reply(time_remaining_message)

    # Check if the bot is mentioned in the message (in any channel, not just DMs)
    if bot.user.mentioned_in(message) and message.author != bot.user:
        #if message.channel.id == CHANNEL_TEST_ID:
            prompt = message.content
            message_lower = prompt.lower()
            logging.info(f"Bot mentioned by {message.author} in {message.channel}: {message.content}")
            if any(keyword in message_lower for keyword in ["what time", "time"]):
                # Send a custom reply when the bot is mentioned
                current_time = datetime.now(pytz.timezone('Europe/Brussels')).strftime("%H:%M:%S")
                await message.channel.send(f"Hello {message.author.mention}, the current time is {current_time}. 🤖")
                time_remaining_message = time_until_next_event()
                await message.channel.send(time_remaining_message)
            if any(keyword in message_lower for keyword in ["tech-talk", "tech talk"]):
                techTalkMessage = get_techtalk_message_if_today(json_keyfile_path, sheet_url)
                logging.info(techTalkMessage)
                chat = get_chat_for_user(message.author.id)
                prompt += f"Also, the use is asking about Tech talk so This is the tech talk scheduled today: {techTalkMessage}. Can you summarize or comment on it?"
                response = chat.send_message(prompt)
                await message.channel.send(response.text)
            else:
                try:
                    chat = get_chat_for_user(message.author.id)
                    response = chat.send_message(prompt)
                    reply = response.text
                except Exception as e:
                    logging.error(f"Erreur Gemini : {e}")
                    reply = "⚠️ Une erreur s'est produite avec Gemini."
                await message.channel.send(reply)

    # Always let the bot handle commands with `on_message`
    await bot.process_commands(message)

# Event when the bot is ready
@bot.event
async def on_ready():
    logging.info(f'Bot connected as {bot.user}')
    channel_test = bot.get_channel(CHANNEL_TEST_ID)
    if channel_test:
        await channel_test.send(f"🤖 Yeah I'm still workin' no worries 🤖")  # Mentionner l'utilisateur avec son ID
    else:
        logging.error("Le canal spécifié n'a pas été trouvé (pour test).")
    
    # Schedule messages using cron-style scheduling
    for time_str in ["08:55", "11:00", "12:30", "13:25", "15:00", "17:00"]:
        hour, minute = time_str.split(":")
        scheduler.add_job(
            send_scheduled_message,
            'cron',
            hour=hour,
            minute=minute,
            args=[time_str],
            id=f"message_{time_str}",
            replace_existing=True
        )
    
    scheduler.start()
    await bot.tree.sync()
    logging.info("Slash commands are synced!")
    
    #check_birthday.start()

def main():
    #load_user_chats()
    #signal.signal(signal.SIGINT, lambda *args: asyncio.create_task(handle_exit_signal(*args)))
    #signal.signal(signal.SIGTERM, lambda *args: asyncio.create_task(handle_exit_signal(*args)))
    bot.run(TOKEN)  # Start the bot

if __name__ == "__main__":
    main()