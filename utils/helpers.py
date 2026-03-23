import discord
 
GREEN  = 0x2ECC71
RED    = 0xE74C3C
BLUE   = 0x3498DB
GOLD   = 0xF1C40F
PURPLE = 0x9B59B6
DARK   = 0x2C2F33

def make_embed(title, desc, color=BLUE, footer=None, author=None):
    e = discord.Embed(title=title, description=desc, color=color)
    if footer:
        e.set_footer(text=footer)
    if author:
        e.set_author(name=author.display_name, icon_url=author.display_avatar.url)
    return e

def win(title, desc, user=None):
    return make_embed(title, desc, GREEN, author=user)

def lose(title, desc, user=None):
    return make_embed(title, desc, RED, author=user)

def tie(title, desc, user=None):
    return make_embed(title, desc, GOLD, author=user)

def info(title, desc, user=None):
    return make_embed(title, desc, BLUE, author=user)
