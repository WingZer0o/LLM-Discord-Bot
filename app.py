import os
from dotenv import load_dotenv
from bot import bot
from commands.hey_bot_command import HeyBotCommand
from commands.parse_docs_command import ParseDocsCommand
from database.database import get_engine, Base
from sqlalchemy.orm import sessionmaker

from database.tables.chat_message import ChatMessage
load_dotenv()


@bot.command(name='heybot', help='A command to prompt the LLM associated with the chatbot through a message')
async def hey_bot(ctx):
    await HeyBotCommand.handle_hey_bot_command(ctx)

@bot.command(name='docs', help='A command that parses our documentation and stores the results in a vector data')
async def parse_docs(ctx):
    await ParseDocsCommand.parse_docs(ctx)

TOKEN = os.getenv('TOKEN')

engine = get_engine(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_DB"))
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)

bot.run(TOKEN)