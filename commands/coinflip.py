import random
import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import win, lose

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Flip a coin and guess the outcome")
    @app_commands.describe(choice="heads or tails")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Heads", value="heads"),
        app_commands.Choice(name="Tails", value="tails"),
    ])
    async def coinflip(self, interaction: discord.Interaction, choice: str):
        result = random.choice(["heads", "tails"])
        won = choice == result

        icons = {"heads": "🟡", "tails": "⚫"}
        pick_icon = icons[choice]
        result_icon = icons[result]

        if won:
            e = win(
                "Correct!",
                f"> {pick_icon}  You picked **{choice.capitalize()}**\n"
                f"> {result_icon}  Landed on **{result.capitalize()}**\n\n"
                f"✅  Nice call!",
            )
        else:
            e = lose(
                "Wrong!",
                f"> {pick_icon}  You picked **{choice.capitalize()}**\n"
                f"> {result_icon}  Landed on **{result.capitalize()}**\n\n"
                f"❌  Better luck next time!",
            )

        e.set_author(name=interaction.user.display_name)
        e.set_footer(text="Whim")
        await interaction.response.send_message(embed=e)

async def setup(bot):
    await bot.add_cog(Coinflip(bot))

