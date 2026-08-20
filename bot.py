
import discord
from discord.ext import commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Pre-loaded with your official 10 server guidelines
current_rules = (
    "1. While in our Server, follow Roblox's TOS and Discord TOS.\n"
    "2. Be respectful to anybody in the server no matter what.\n"
    "3. You are allowed to swear in the server as long it isnt a slur and directed to anybody.\n"
    "4. Discrimination of any kind is not allowed at all.\n"
    "5. NSFW, Sexting, or anything inappropriate is not allowed.\n"
    "6. refrain from spamming, attention seeking in VC, if this happens spammers will be timed out for 5 mins and VC attention seekers will be timed out for 10.\n"
    "7. This server is English only, as it is hard for our moderators to moderate in other languages.\n"
    "8. Only use channels for designated purposes.\n"
    "9. Do not Troll during flights, In VC's or In chats at all.\n"
    "10. Moderation will be harsh, do not argue with employees at all for any purpose."
)
current_footer = "Thank you for cooperating! Safe flying out there in PTFS."

# Global Live Flight Information Storage
flight_data = {
    "number": "BT-001",
    "status": "SCHEDULED",
    "date": "August 24th",
    "gate": "Gate 1 (Main Terminal)",
    "destination": "Riga International Airport (PTFS)"
}

# Live Passenger Database Tracking
club_miles = {}

@bot.event
async def on_ready():
    print(f"🟢 airBaltic Utilities is online as {bot.user.name}!")
    await bot.change_presence(activity=discord.Game(name="PTFS | type !commands"))

# 📥 AUTOMATED WELCOME, MULTI-ROLE & AUTO-NAME SYSTEM
@bot.event
async def on_member_join(member):
    pax_role = discord.utils.get(member.guild.roles, name="Passenger")
    eco_role = discord.utils.get(member.guild.roles, name="ECO | Economy Class")
    
    if pax_role:
        try: await member.add_roles(pax_role)
        except Exception: pass
            
    if eco_role:
        try: await member.add_roles(eco_role)
        except Exception: pass

    try:
        new_nickname = f"PAX | {member.global_name or member.name}"
        if len(new_nickname) > 32: 
            new_nickname = new_nickname[:29] + "..."
        await member.edit(nick=new_nickname)
    except Exception: pass

    welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if welcome_channel:
        welcome_text = (
            f"🇱🇻  **Welcome to airBaltic, {member.mention}!**\n"
            f"`🟢` **`think green, fly green`**\n\n"
            f"> Welcome aboard! Review guidelines in `!rules` and use `!commands` to explore our premium systems."
        )
        await welcome_channel.send(welcome_text)

# Handles role permissions errors smoothly 
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole) or isinstance(error, commands.CheckFailure):
        await ctx.send("❌ **Access Denied:** This command is strictly locked to the **CEO** and **CTO** positions.")
        return
    raise error

# 1. System Commands Index Directory Index
@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title="✈️ AIRBALTIC ADVANCED SYSTEM UTILITIES",
        description="Premium automated customer service and logistics interface directory.",
        color=0xCDDA32
    )
    embed.add_field(
        name="🎮 Public Passenger Tools",
        value=(
            "• `!commands` - Open this automated user service index panel.\n"
            "• `!rules` - View our 10 official server operational codes.\n"
            "• `!fleet` - Inspect our active aircraft profile configurations.\n"
            "• `!flight` - Check current live flight details and routes.\n"
            "• `!checkin` - Check in for a flight and print an electronic boarding pass.\n"
            "• `!club` - View your airBaltic Club frequent flyer stats and tier standings."
        ),
        inline=False
    )
    embed.add_field(
        name="💼 Executive Operations (LOCKED TO CEO/CTO)",
        value=(
            "• `!status <NEW_STATUS>` - Update the operational flight status board.\n"
            "• `!firstcall` - Broadcast the initial boarding call announcement.\n"
            "• `!rows` - Broadcast boarding notice restricted to back seat rows.\n"
            "• `!finalcall` - Broadcast the urgent final boarding call alert card.\n"
            "• `!logflight <@user>` - Record completed commercial flight miles for a pilot.\n"
            "• `!givemiles <@user> <amount>` - Bulk award points to an account ledger.\n"
            "• `!clear <amount>` - Sweep out chat lines up to 100 entries.\n"
            "• `!createflight <No. / Status / Date / Gate / Dest>` - Log a route path map setup.\n"
            "• `!setrules <text>` / `!setfooter <text>` - Update master rule strings on-the-fly."
        ),
        inline=False
    )
    await ctx.send(embed=embed)

# 📢 BOARDING CALL 1: First Call Notice (LOCKED TO CEO/CTO)
@bot.command()
@commands.has_any_role("CEO", "CTO")
async def firstcall(ctx):
    embed = discord.Embed(
        title="🛫 airBaltic ANNOUNCEMENT: FIRST BOARDING CALL",
        description=f"Good day passengers, airBaltic flight **{flight_data['number']}** to **{flight_data['destination']}** is now ready for boarding.",
        color=0xCDDA32
    )
    embed.add_field(name="📍 Location:", value=f"Please proceed immediately to **{flight_data['gate']}**.", inline=False)
    embed.add_field(name="📋 Directives:", value="Please have your electronic boarding passes ready for validation by ground crew via `!checkin`.", inline=False)
    embed.set_footer(text="Thank you for flying green with airBaltic.")
    await ctx.send("@everyone", embed=embed)

# 📢 BOARDING CALL 2: Seat Row Restriction Notice (LOCKED TO CEO/CTO)
@bot.command()
@commands.has_any_role("CEO", "CTO")
async def rows(ctx):
    embed = discord.Embed(
        title="✈️ airBaltic ANNOUNCEMENT: BOARDING BY SEAT ROWS",
        description=f"Attention passengers on flight **{flight_data['number']}** with destination **{flight_data['destination']}**.",
        color=0xCDDA32
    )
    embed.add_field(name="💺 Active Boarding Zone:", value="We are now welcoming passengers holding boarding passes for **Rows 15 through 30** to board the aircraft.", inline=False)
    embed.add_field(name="📋 Directives:", value="All other passengers, please remain seated in the gate terminal area until your row zone is announced.", inline=False)
    embed.set_footer(text="We appreciate your cooperation during boarding.")
    await ctx.send(embed=embed)

# 📢 BOARDING CALL 3: Final Call Notice (LOCKED TO CEO/CTO)
@bot.command()
@commands.has_any_role("CEO", "CTO")
async def finalcall(ctx):
    embed = discord.Embed(
        title="🚨 airBaltic ANNOUNCEMENT: FINAL BOARDING CALL",
        description=f"This is the final boarding announcement for remaining passengers booked on airBaltic flight **{flight_data['number']}** bound for **{flight_data['destination']}**.",
        color=0xFF3333
    )
    embed.add_field(name="⚠️ Immediate Action Required:", value=f"The aircraft doors are preparing to close. All remaining passengers must clear security and report to **{flight_data['gate']}** immediately.", inline=False)
    embed.set_footer(text="Final boarding alert • Flight operations closing.")
    await ctx.send("@everyone", embed=embed)

# 📊 FLIGHT STATUS BOARD MANAGEMENT SYSTEM (LOCKED TO CEO/CTO)
@bot.command()
@commands.has_any_role("CEO", "CTO")
async def status(ctx, *, new_status: str):
    global flight_data
    flight_data["status"] = new_status.upper()
    
    status_emoji = "🟢" if "board" in new_status.lower() or "active" in new_status.lower() else "🟡"
    if "cancel" in new_status.lower() or "delay" in new_status.lower():
        status_emoji = "🔴"
        
    embed = discord.Embed(
        title="📊 airBaltic REAL-TIME OPERATIONS STATUS",
        description="The live schedule and operational state of our mainline flight route has been updated.",
        color=0xCDDA32
    )
    embed.add_field(name="Flight Identifier:", value=f"`{flight_data['number']}`", inline=True)
    embed.add_field(name="Current Flight State:", value=f"{status_emoji} **{flight_data['status']}**", inline=True)
    embed.add_field(name="Route Vectors:", value=f"🛫 Riga (RIX) ➡️ 🛬 `{flight_data['destination']}`", inline=False)
    embed.set_footer(text="Type !flight to view the full detailed travel itinerary block.")
    await ctx.send(embed=embed)

# 2. Ticket Check-In Boarding Pass Generator
@bot.command()
async def checkin(ctx):
    seat_letters = ["A", "B", "C", "D", "F"]
    seat_num = f"{random.randint(1, 28)}{random.choice(seat_letters)}"
    seq_num = f"0{random.randint(10, 99)}"
    
    embed = discord.Embed(
        title="🎟️ ELECTRONIC BOARDING PASS • VALIDATED",
        description="Your virtual ticket has been confirmed in the airBaltic manifest database.",
        color=0xCDDA32
    )
    embed.add_field(name="Passenger Name:", value=f"`{ctx.author.display_name}`", inline=True)
    embed.add_field(name="Flight Assignment:", value=f"`{flight_data['number']}`", inline=True)
    embed.add_field(name="Assigned Seat:", value=f"💺 `{seat_num}`", inline=True)
    embed.add_field(name="Gate Assignment:", value=f"🚪 `{flight_data['gate']}`", inline=False)
    embed.add_field(name="Route Vector:", value=f"🛫 RIX ➡️ 🛬 `{flight_data['destination']}`", inline=False)
    embed.set_footer(text=f"Sequence No: {seq_num} • Please arrive at the terminal prior to departure.")
    await ctx.send(embed=embed)

# 3. Loyalty Club Tracking with Your Exact Milestone Tiers
@bot.command()
async def club(ctx):
    user_id = str(ctx.author.id)
    miles = club_miles.get(user_id, 0)
    
    if miles >= 35000: tier = "💎 Business Class Club"
