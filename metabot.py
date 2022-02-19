# !/usr/bin/python3.8
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix=">",
    intents=intents
)

bot.help_command = None

cogfiles = [
    "cogs.events",
    "cogs.commands"
]

for cogfile in cogfiles:
    try:
        bot.load_extension(cogfile)
    except Exception as e:
        print(e)


bot.run(os.getenv('TOKEN'))