

import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Temporary memory storage for custom rules
current_rules = (
    "1. Follow instructions issued by airBaltic Staff and ATC.\n"
    "2. Maintain respect toward all passengers and flight crew.\n"
    "3. Keep conversations relevant to the channel topic.\n"
    "4. Follow proper taxi and flight protocols during operations.\n"
    "5. Do not advertise external virtual airlines without permission."
)

@bot.event
async def on_ready():
    print(f"🟢 airBaltic Utilities is online as {bot.user.name}!")
    await bot.change_presence(activity=discord.Game(name="PTFS | flying airBaltic"))

# 1. Dynamic Rules Command
@bot.command()
async def rules(ctx):
    embed = discord.Embed(
        title="📜 AIRBALTIC OFFICIAL SERVER RULES",
        description="Welcome to airBaltic! Please follow our official airline guidelines:",
        color=0xCDDA32 # airBaltic primary yellow-green
    )
    embed.add_field(name="Current Server Guidelines:", value=current_rules, inline=False)
    embed.set_footer(text="Thank you for cooperating! Safe flying out there in PTFS.")
    await ctx.send(embed=embed)

# 2. CEO Rule Changer Command
@bot.command()
async def setrules(ctx, *, new_text: str):
    global current_rules
    # Checks if the person running it is an Administrator (like the CEO)
    if ctx.author.guild_permissions.administrator:
        current_rules = new_text
        await ctx.send("✅ **CEO Update Complete:** The official rules have been updated instantly!")
    else:
        await ctx.send("❌ You do not have permission to change the company rules.")

# Secure background token fetcher
bot.run(os.environ.get("DISCORD_TOKEN"))
