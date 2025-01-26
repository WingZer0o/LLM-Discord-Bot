import discord
from discord.ext import commands
from commands.hey_bot_command import HeyBotCommand

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)