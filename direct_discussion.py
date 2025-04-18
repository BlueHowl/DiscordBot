import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks, commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from datetime import datetime, timedelta
import pytz  # for timezone

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID_AI"))

# Configurer les logs
logging.basicConfig(level=logging.INFO)

# Créer l'intent et le bot
intents = discord.Intents.default()
intents.messages = True  # Assure-toi que l'intent messages est activé
bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler(timezone='Europe/Brussels')  # Change as needed

# Liste des horaires de check-in et check-out
checkin_times = ["09:00", "13:30"]
checkout_times = ["12:30", "17:00"]
break_time = ["11:00", "15:00", "15:15"]
lunch_time = ["12:30"]

@bot.event
async def on_ready():
    # Lorsque le bot est prêt et connecté, envoie un message dans un canal spécifique
    channel = bot.get_channel(CHANNEL_ID)  # Remplace CHANNEL_ID par l'ID du canal où tu veux envoyer le message
    guild = channel.guild if channel else None
    role = discord.utils.get(guild.roles, name="Hamilton 10") if guild else None
    if role:
        role_mention = role.mention
    else:
        logging.warning(f"Role not found in {channel.name}")
        role_mention = ""

    if channel:
        await channel.send(f"🤖 {role_mention} Hello I'm CheckinBot Don't Forget to checkin, sorry for being today 🤖")  # Mentionner l'utilisateur avec son ID
    else:
        logging.error("Le canal spécifié n'a pas été trouvé.")

    logging.info(f'Bot connecté en tant que {bot.user}')

# Run the bot
bot.run(TOKEN)