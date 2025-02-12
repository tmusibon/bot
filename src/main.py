import discord
from discord.ext import commands
from database import init_db, add_trade, update_trade, get_active_trades
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Bot initialization
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help') 

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    init_db()

@bot.command(name='analyze')
async def analyze(ctx, token_address: str):
    try:
        # Here you would add your analysis logic
        # This is a placeholder response
        embed = discord.Embed(
            title="Token Analysis",
            description=f"Analysis for token: {token_address}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Price", value="$0.00", inline=True)
        embed.add_field(name="24h Change", value="0%", inline=True)
        embed.add_field(name="Volume", value="$0", inline=True)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error analyzing token: {str(e)}")

@bot.command(name='trade')
async def trade(ctx, token_address: str, entry_price: float):
    try:
        add_trade(token_address, entry_price)
        embed = discord.Embed(
            title="New Trade Added",
            description=f"Successfully opened trade for {token_address}",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Entry Price", value=f"${entry_price}", inline=True)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error adding trade: {str(e)}")

@bot.command(name='close')
async def close_trade(ctx, trade_id: int, exit_price: float):
    try:
        update_trade(trade_id, exit_price)
        embed = discord.Embed(
            title="Trade Closed",
            description=f"Successfully closed trade #{trade_id}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Exit Price", value=f"${exit_price}", inline=True)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error closing trade: {str(e)}")

@bot.command(name='trades')
async def list_trades(ctx):
    try:
        trades = get_active_trades()
        if not trades:
            await ctx.send("No active trades found.")
            return

        embed = discord.Embed(
            title="Active Trades",
            description="Current open positions",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        for trade in trades:
            trade_id, token_address, entry_price, entry_time = trade[0:4]
            embed.add_field(
                name=f"Trade #{trade_id}",
                value=f"Token: {token_address}\nEntry: ${entry_price}\nTime: {entry_time}",
                inline=False
            )

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error listing trades: {str(e)}")

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="Trading Bot Commands",
        description="List of available commands",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    commands = {
        "!analyze <token_address>": "Analyze a token",
        "!trade <token_address> <entry_price>": "Open a new trade",
        "!close <trade_id> <exit_price>": "Close an existing trade",
        "!trades": "List all active trades",
        "!help": "Show this help message"
    }
    
    for command, description in commands.items():
        embed.add_field(name=command, value=description, inline=False)
    
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send("Invalid argument provided. Please check the command syntax.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
