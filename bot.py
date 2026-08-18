
import discord
from discord.ext import commands
import os
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Live memory storage for your rules, footer, and active flight details
current_rules = (
    "1. Follow instructions issued by airBaltic Staff and ATC.\n"
    "2. Maintain respect toward all passengers and flight crew.\n"
    "3. Keep conversations relevant to the channel topic.\n"
    "4. Follow proper taxi and flight protocols during operations.\n"
    "5. Do not advertise external virtual airlines without permission."
)
current_footer = "Thank you for cooperating! Safe flying out there in PTFS."

# Default flight data stored in live memory
flight_data = {
    "number": "BT-001",
    "status": "SCHEDULED",
    "date": "August 24th",
    "gate": "Gate 1 (Main Terminal)",
    "destination": "Riga International Airport (PTFS)"
}

@bot.event
async def on_ready():
    print(f"🟢 airBaltic Utilities is online as {bot.user.name}!")
    await bot.change_presence(activity=discord.Game(name="PTFS | flying airBaltic"))

# 📥 AUTOMATED WELCOME SYSTEM
@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if welcome_channel:
        welcome_text = (
            f"🇱🇻  **Welcome to airBaltic, {member.mention}!**\n"
            f"`🟢` **`think green, fly green`**\n\n"
            f"> We are thrilled to have you step aboard the Baltics' premier virtual airline!\n\n"
            f"🔹 **Step 1:** Review our official operating guidelines in `!rules`.\n"
            f"🔹 **Step 2:** Check out our current flight status with `!flight`.\n"
            f"🔹 **Step 3:** Stay tuned for our massive **August 24th Inaugural Flight** event!\n\n"
            f"> **Prepare for departure and enjoy your travel experience with airBaltic! 🍏**"
        )
        await welcome_channel.send(welcome_text)

# 1. New Dynamic Flight Tracking Command
@bot.command()
async def flight(ctx):
    embed = discord.Embed(
        title="✈️ AIRBALTIC OFFICIAL FLIGHT ANNOUNCEMENT ✈️",
        color=0xCDDA32 # airBaltic primary yellow-green
    )
    
    # Check if this is the inaugural august flight to calculate a real-time countdown day tracker
    countdown_str = ""
    if "august 24" in flight_data["date"].lower():
        current_year = datetime.now().year
        try:
            target_date = datetime(current_year, 8, 24)
            days_left = (target_date - datetime.now()).days
            if days_left > 0:
                countdown_str = f"\n⏳ **Countdown:** Only `{days_left} days` until departure!"
            elif days_left == 0:
                countdown_str = f"\n🚨 **Status Update:** The flight is happening TODAY!"
        except Exception:
            pass

    status_emoji = "🟢" if "boarding" in flight_data["status"].lower() or "active" in flight_data["status"].lower() else "🟡"
    
    embed.add_field(name="Flight Number:", value=f"`{flight_data['number']}`", inline=True)
    embed.add_field(name="Operations Status:", value=f"{status_emoji} **{flight_data['status'].upper()}**", inline=True)
    embed.add_field(name="Scheduled Date:", value=f"`{flight_data['date']}`{countdown_str}", inline=False)
    embed.add_field(name="Airport Gate:", value=f"`{flight_data['gate']}`", inline=False)
    embed.add_field(name="Route Destination:", value=f"`{flight_data['destination']}`", inline=False)
    embed.set_footer(text="Please ensure your flight tickets are ready prior to reaching the gate. Thank you for flying airBaltic!")
    await ctx.send(embed=embed)

# 2. CEO Custom Flight Creator Command (Split items using a slash '/')
@bot.command()
async def createflight(ctx, *, details: str):
    global flight_data
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ You do not have permission to log flight operations.")
        return
        
    try:
        # Example format: BT-102 / BOARDING / August 24th / Gate 3 / London Heathrow
        parts = [p.strip() for p in details.split("/")]
        if len(parts) < 5:
            await ctx.send("❌ **Format Error!** Use: `!createflight FlightNumber / Status / Date / Gate / Destination`")
            return
            
        flight_data["number"] = parts[0]
        flight_data["status"] = parts[1]
        flight_data["date"] = parts[2]
        flight_data["gate"] = parts[3]
        flight_data["destination"] = parts[4]
        
        await ctx.send("✅ **CEO Operations Logged:** Custom flight itinerary generated successfully! Type `!flight` to view.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred formatting the logs: {str(e)}")

# 3. Rules Command
@bot.command()
async def rules(ctx):
    embed = discord.Embed(
        title="📜 AIRBALTIC OFFICIAL SERVER RULES",
        description="Welcome to airBaltic! Please follow our official airline guidelines:",
        color=0xCDDA32
    )
    embed.add_field(name="Current Server Guidelines:", value=current_rules, inline=False)
    embed.set_footer(text=current_footer)
    await ctx.send(embed=embed)

# 4. Rule Changer Command
@bot.command()
async def setrules(ctx, *, new_text: str):
    global current_rules
    if ctx.author.guild_permissions.administrator:
        current_rules = new_text
        await ctx.send("✅ **CEO Update Complete:** Rules updated!")
    else:
        await ctx.send("❌ Access Denied.")

# 5. Recruitment Board Command
@bot.command()
async def hiring(ctx):
    ad_text = (
        "🇱🇻  **airBaltic**\n"
        "`🟢` **`think green, fly green`**\n\n"
        "> airBaltic is the primary airline of the Baltics, operating an elite, all-Airbus A220-300 fleet. We connect virtual aviators to a wide grid of destinations, delivering a sleek experience from standard economy to our prestigious cabin crew teams.\n\n"
        "🔹 **Now Hiring Premium Crew:** Elevate your career by managing our elite Business Class cabins.\n"
        "🔹 **Aviation Realism:** Train under advanced flight protocols, structural routes, and live ATC.\n\n"
        "📸 https://imgur.com"
    )
    await ctx.send(ad_text)

bot.run(os.environ.get("DISCORD_TOKEN"))
