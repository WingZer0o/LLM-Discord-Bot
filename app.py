import os
from dotenv import load_dotenv
from bot import bot
from commands.hey_bot_command import HeyBotCommand
load_dotenv()


@bot.command(name='heybot', help='A command to prompt the LLM associated with the chatbot through a message')
async def hey_bot(ctx):
    await HeyBotCommand.handle_hey_bot_command(ctx)

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)