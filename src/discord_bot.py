from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
from langchain.llms import Ollama
from .api.client import APIClient
from .utils.analysis import analyze_pair, format_price, format_large_number

load_dotenv()

class DiscordTradingBot:
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        
        self.bot = commands.Bot(command_prefix='!', intents=self.intents)
        self.api_client = APIClient()
        self.llm = Ollama(model="llama2")
        
        # Register commands
        self.setup_commands()

    def setup_commands(self):
        @self.bot.event
        async def on_ready():
            print(f'{self.bot.user} is ready and online!')

        @self.bot.command()
        async def scan(ctx, pair_address: str):
            await self.scan_token(ctx, pair_address)

        @self.bot.command()
        async def ask(ctx, *, question):
            try:
                response = self.llm(question)
                await ctx.send(response)
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")

    async def scan_token(self, ctx, pair_address):
        await ctx.send(f"🔍 Scanning pair {pair_address}...")
        
        try:
            pair_data = await self.api_client.get_pair_data(pair_address)
            if not pair_data or 'pairs' not in pair_data or not pair_data['pairs']:
                await ctx.send("❌ Error: Pair not found or invalid address")
                return

            holders_data = await self.api_client.get_security_data(pair_address)
            analysis = analyze_pair(pair_data, holders_data or {'holders': []})
            
            if 'error' in analysis:
                await ctx.send(f"❌ Error analyzing pair: {analysis['error']}")
                return

            response = self.format_analysis_response(analysis, pair_address)
            await ctx.send(response)

        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    def format_analysis_response(self, analysis, pair_address):
        return f"""
🔍 Security Analysis for {pair_address}

🚨 Security Level: {analysis['security'].security_level.value}

💰 Token Metrics:
Price: {format_price(analysis['price'])}
Liquidity: ${format_large_number(analysis['liquidity'])}
24h Volume: ${format_large_number(analysis['volume_24h'])}

📊 Risk Metrics:
Buy Tax: {analysis['buy_tax']*100:.1f}%
Sell Tax: {analysis['sell_tax']*100:.1f}%
Top Holders: {analysis['holder_concentration']*100:.1f}%

⚠️ Warnings:
{chr(10).join(analysis['warnings']) if analysis['warnings'] else 'No major warnings'}

🚦 Trading Status: {'✅ SAFE TO TRADE' if analysis['is_tradeable'] else '❌ DO NOT TRADE'}

⚠️ DISCLAIMER: This is not financial advice. Always DYOR!
"""

    async def start(self):
        await self.api_client.init_session()
        await self.bot.start(os.getenv('DISCORD_BOT_TOKEN'))

    async def shutdown(self):
        await self.api_client.close()
        await self.bot.close()
