import discord
from discord.ext import commands
import config
import datetime
import aiohttp
from database import init_db

init_db()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def is_valid_address(address: str) -> bool:
    # Basic Ethereum address validation
    return address.startswith('0x') and len(address) == 42

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name}')

@bot.command(name='help')
async def help_command(ctx):
    help_embed = discord.Embed(
        title="Bot Commands",
        description="Available commands:",
        color=discord.Color.blue()
    )
    help_embed.add_field(
        name="!check <token_address>",
        value="Analyze a token for price, liquidity, and security",
        inline=False
    )
    await ctx.send(embed=help_embed)

@bot.command(name='check')
async def check_token(ctx, token_address: str):
    if not is_valid_address(token_address):
        await ctx.send("Invalid token address! Address should start with '0x' and be 42 characters long.")
        return

    # Create a loading embed
    loading_embed = discord.Embed(
        title="🔍 Analyzing Token",
        description="Please wait while I gather information...",
        color=discord.Color.blue()
    )
    message = await ctx.send(embed=loading_embed)
    
    try:
        # DexScreener API call
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config.DEX_SCREENER_API}{token_address}") as response:
                dex_data = await response.json()

        # RugCheck API call
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config.RUGCHECK_API}scan/{token_address}") as response:
                rug_data = await response.json()

        # Create result embed
        result_embed = discord.Embed(
            title="Token Analysis Results",
            description=f"Analysis for token: `{token_address}`",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )

        # Add DexScreener data
        if 'pairs' in dex_data and dex_data['pairs']:
            pair = dex_data['pairs'][0]
            result_embed.add_field(
                name="💰 Price",
                value=f"${float(pair.get('priceUsd', 0)):.8f}",
                inline=True
            )
            result_embed.add_field(
                name="💧 Liquidity",
                value=f"${float(pair.get('liquidity', {}).get('usd', 0)):,.2f}",
                inline=True
            )
            result_embed.add_field(
                name="📊 24h Volume",
                value=f"${float(pair.get('volume', {}).get('h24', 0)):,.2f}",
                inline=True
            )

        # Add RugCheck data
        if rug_data:
            result_embed.add_field(
                name="🛡️ Security Score",
                value=f"{rug_data.get('score', 'N/A')}/100",
                inline=True
            )
            result_embed.add_field(
                name="⚠️ Risk Level",
                value=rug_data.get('risk', 'Unknown'),
                inline=True
            )

        result_embed.set_footer(text="Data from DexScreener & RugCheck")
        
        # Update the message with results
        await message.edit(embed=result_embed)

    except Exception as e:
        # Error embed
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while analyzing the token: {str(e)}",
            color=discord.Color.red()
        )
        await message.edit(embed=error_embed)

@check_token.error
async def check_token_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a token address! Usage: `!check <token_address>`")

bot.run(config.DISCORD_BOT_TOKEN)
