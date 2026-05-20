import random
import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import win, lose, tie

FACES = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dice", description="Roll dice against the bot, highest total wins")
    @app_commands.describe(count="how many dice to roll each (1 to 3)")
    async def dice(self, interaction: discord.Interaction, count: app_commands.Range[int, 1, 3] = 2):
        player_rolls = [random.randint(1, 6) for _ in range(count)]
        bot_rolls    = [random.randint(1, 6) for _ in range(count)]

        pt = sum(player_rolls)
        bt = sum(bot_rolls)

        p_faces = "  ".join(FACES[r - 1] for r in player_rolls)
        b_faces = "  ".join(FACES[r - 1] for r in bot_rolls)
 
        desc = (
            f"> 👤  You    {p_faces}    **{pt}**\n"
            f"> 🤖  Bot    {b_faces}    **{bt}**\n"
        )

        if pt > bt:
            e = win(f"🎲  You rolled higher!  ({pt} vs {bt})", desc)
        elif pt < bt:
            e = lose(f"🎲  Bot rolled higher  ({bt} vs {pt})", desc)
        else:
            e = tie(f"🎲  Dead tie  ({pt} vs {bt})", desc)

        e.set_author(name=interaction.user.display_name)
        e.set_footer(text="Whim")
        await interaction.response.send_message(embed=e)

async def setup(bot):
    await bot.add_cog(Dice(bot))