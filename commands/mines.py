import random
import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import win, lose, info, make_embed, BLUE

active_games = {}

GRID = 20

def new_game(bombs):
    cells = [{"revealed": False, "bomb": False} for _ in range(GRID)]
    pool = list(range(GRID))
    random.shuffle(pool)
    for i in pool[:bombs]:
        cells[i]["bomb"] = True
    return {"cells": cells, "bombs": bombs, "found": 0, "over": False, "alive": True}

def game_embed(game, user):
    found = game["found"]
    safe_left = GRID - game["bombs"] - found
    mult = round(1.0 + found * 0.5, 1)

    if not game["over"]:
        desc = (
            f"> 💣  Bombs hiding    **{game['bombs']}**\n"
            f"> 💎  Found so far    **{found}**\n"
            f"> 🔲  Safe tiles left  **{safe_left}**\n"
            f"> 📈  Cash out mult    **{mult}x**\n\n"
            f"*click tiles to reveal diamonds, avoid the bombs*"
        )
        e = make_embed("💣 Mines", desc, BLUE)
    elif game["alive"]:
        desc = (
            f"> 💎  Diamonds found    **{found}**\n"
            f"> 📈  Multiplier         **{mult}x**\n\n"
            f"✅  Cashed out safely"
        )
        e = win("💠 Cashed Out!", desc)
    else:
        desc = (
            f"> 💣  You hit a bomb!\n"
            f"> 💎  Had found    **{found}** diamond(s) before going boom\n\n"
            f"❌  Game over"
        )
        e = lose("💥 Game Over", desc)

    e.set_author(name=user.display_name)
    e.set_footer(text="Whim")
    return e

class MinesView(discord.ui.View):
    def __init__(self, user_id, game):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.game = game
        self.rebuild()

    def rebuild(self, reveal_bombs=False):
        self.clear_items()
        for idx in range(GRID):
            cell = self.game["cells"][idx]
            row  = idx // 5
 
            if cell["revealed"] and not cell["bomb"]:
                emoji, style, disabled = "💎", discord.ButtonStyle.success, True
            elif cell["revealed"] and cell["bomb"]:
                emoji, style, disabled = "💣", discord.ButtonStyle.danger, True
            elif reveal_bombs and cell["bomb"]:
                emoji, style, disabled = "💣", discord.ButtonStyle.danger, True
            elif self.game["over"]:
                emoji, style, disabled = "🟫", discord.ButtonStyle.secondary, True
            else:
                emoji, style, disabled = "💎", discord.ButtonStyle.primary, False
 
            btn          = discord.ui.Button(emoji=emoji, style=style, custom_id=f"m{idx}", disabled=disabled, row=row)
            btn.callback = self.make_cb(idx)
            self.add_item(btn)

        if not self.game["over"]:
            cashout_btn = discord.ui.Button(label="💰  Cash Out", style=discord.ButtonStyle.success, row=4, custom_id="cashout")
            cashout_btn.callback = self._cashout_callback
            self.add_item(cashout_btn)
        
    def make_cb(self, idx):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                return await interaction.response.send_message("It is not your game.", ephemeral=True)
                
            g = self.game
            if g["over"] or g["cells"][idx]["revealed"]:
                return await interaction.response.defer()

            g["cells"][idx]["revealed"] = True

            if g["cells"][idx]["bomb"]:
                g["over"] = True
                g["alive"] = False
                self.rebuild(reveal_bombs=True)
                active_games.pop(self.user_id, None)
            else:
                g["found"] += 1
                safe_left = sum(1 for c in g["cells"] if not c["bomb"] and not c["revealed"])
                if safe_left == 0:
                    g["over"] = True
                    g["alive"] = True
                    active_games.pop(self.user_id, None)
                    self.rebuild()

            await interaction.response.edit_message(embed=game_embed(g, interaction.user), view=self)
        return cb

    async def _cashout_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("not your game", ephemeral=True)
        g = self.game
        if g["found"] == 0:
            return await interaction.response.send_message(
                embed=info("Nothing to cash out", "Find at least one 💎 first"), ephemeral=True)
        g["over"]  = True
        g["alive"] = True
        active_games.pop(self.user_id, None)
        self.rebuild()
        await interaction.response.edit_message(embed=game_embed(g, interaction.user), view=self)
 
 
class Mines(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @app_commands.command(name="mines", description="Uncover diamonds, avoid bombs, cash out anytime")
    @app_commands.describe(bombs="how many bombs to hide (1 to 15, default 5)")
    async def mines(self, interaction: discord.Interaction, bombs: app_commands.Range[int, 1, 15] = 5):
        if interaction.user.id in active_games:
            return await interaction.response.send_message(
                embed=info("Already playing", "Finish your current mines game first"), ephemeral=True)

        game = new_game(bombs)
        active_games[interaction.user.id] = game
        view = MinesView(interaction.user.id, game)
        await interaction.response.send_message(embed=game_embed(game, interaction.user), view=view)

async def setup(bot):
    await bot.add_cog(Mines(bot))