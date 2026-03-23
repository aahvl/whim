import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """ready"""
    await bot.tree.sync()
    print(f"online as {bot.user}")

async def main():
    """Main"""
    async with bot:
        for f in os.listdir("./commands"):
            if f.endswith(".py") and not f.startswith("__"):
                await bot.load_extension(f"commands.{f[:-3]}")
        await bot.start(TOKEN)

asyncio.run(main())