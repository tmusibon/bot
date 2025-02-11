import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Set up intents explicitly
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# Create bot instance with specific intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is connected!')
    print(f'Bot name: {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('-------------------')

@bot.command()
async def test(ctx):
    await ctx.send('Bot is working! 👍')

# Get token from .env
token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(token)
