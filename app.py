import os
from dotenv import load_dotenv
from bot import bot
from discord.ext import commands
from commands.hey_bot_command import HeyBotCommand
from commands.parse_docs_command import ParseDocsCommand
from database.database import get_engine, Base

load_dotenv()


@bot.command(name='heybot', help='A command to prompt the LLM associated with the chatbot through a message')
async def hey_bot(ctx):
    await HeyBotCommand.handle_hey_bot_command(ctx)

@bot.command(name='docs', help='A command that parses our documentation and stores the results in a vector data')
@commands.has_permissions(administrator=True)
async def parse_docs(ctx):
    await ParseDocsCommand.parse_docs(ctx)

TOKEN = os.getenv('TOKEN')

bot.run(TOKEN)