from telegram.ext import Application, CommandHandler
from .api.client import APIClient
from .analysis import analyze_pair, format_price, format_large_number

class TradingBot:
    def __init__(self, token):
        self.token = token
        self.api_client = APIClient()

    async def start(self, update, context):
        await update.message.reply_text(
            "🤖 Welcome to the Trading Bot!\n"
            "Use /scan <address> to analyze a token."
        )

    async def scan_token(self, update, context):
        if not context.args:
            await update.message.reply_text("Please provide a token pair address")
            return

        pair_address = context.args[0]
        await update.message.reply_text(f"🔍 Scanning pair {pair_address}...")
        
        try:
            pair_data = await self.api_client.get_pair_data(pair_address)
            if not pair_data or 'pairs' not in pair_data or not pair_data['pairs']:
                await update.message.reply_text("❌ Error: Pair not found or invalid address")
                return

            holders_data = await self.api_client.get_security_data(pair_address)
            analysis = analyze_pair(pair_data, holders_data or {'holders': []})
            
            if 'error' in analysis:
                await update.message.reply_text(f"❌ Error analyzing pair: {analysis['error']}")
                return

            response = self.format_analysis_response(analysis, pair_address)
            await update.message.reply_text(response)

        except Exception as e:
            await update.message.reply_text(f"❌ An error occurred: {str(e)}")

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

    async def init(self):
        self.application = Application.builder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("scan", self.scan_token))
        await self.api_client.init_session()

    async def run(self):
        await self.init()
        await self.application.run_polling()

    async def shutdown(self):
        await self.api_client.close()
