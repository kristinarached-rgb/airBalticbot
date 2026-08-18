import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🟢 airBaltic Utilities is online as {bot.user.name}!")
    await bot.change_presence(activity=discord.Game(name="PTFS | flying airBaltic"))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def boarding(ctx):
    embed = discord.Embed(title="✈️ AIRBALTIC FLIGHT ANNOUNCEMENT ✈️", color=0xCDDA32)
    embed.add_field(name="Flight:", value="`BT-001 (INAUGURAL FLIGHT)`", inline=True)
    embed.add_field(name="Status:", value="🟢 **NOW BOARDING**", inline=True)
    embed.add_field(name="Departure Date:", value="`August 24th`", inline=False)
    embed.add_field(name="Gate:", value="`Gate 1 (Main Terminal)`", inline=False)
    embed.add_field(name="Destination:", value="`Riga International Airport (PTFS)`", inline=False)
    embed.set_footer(text="Join us for our very first flight! Please have your tickets ready at the gate.")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def rules(ctx):
    embed = discord.Embed(title="📜 AIRBALTIC OFFICIAL SERVER RULES", color=0xCDDA32)
    embed.add_field(name="1. Directives & Aviation Realism", value="Follow instructions issued by Staff and Active ATC Controllers.", inline=False)
    embed.add_field(name="2. Behavioral Standards", value="Maintain respect toward all passengers and flight crew.", inline=False)
    embed.set_footer(text="Thank you for cooperating! Safe flying.")
    await ctx.send(embed=embed)
    await ctx.message.delete()

import os
bot.run(os.environ.get("DISCORD_TOKEN"))

