import discord
from discord.ext import commands
from discord.ui import View
from discord import app_commands
import os
from dotenv import load_dotenv

# ================= LOAD TOKEN =================
load_dotenv()
TOKEN = os.getenv("TOKEN")

# ================= INTENTS =================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= SETTINGS =================
CATEGORY_NAME = "✉️・𝗧𝗶𝗰𝗸𝗲𝘁"
SUPPORT_ROLE = "Ticket suporter"  # اصلاح شد، مطابق با اسم رول در سرور

WELCOME_CHANNEL_NAME = "💠・𝘞𝘦𝘭𝘤𝘰𝘮𝘦"
WELCOME_IMAGE = "https://media.discordapp.net/attachments/1360652773636575525/1512134315633283275/shayan.png?ex=6a24f692&is=6a23a512&hm=0fbf5cfa574e80ac812de795720a15e37deb1c4d6f83ded08e286c0df46def4f&=&format=webp&quality=lossless&width=1240&height=698"

ticket_counter = 1

# ================= WELCOME SYSTEM =================
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL_NAME)
    if channel:
        embed = discord.Embed(
            title="❄️ Welcome to Blizzard ❄️",
            description=f"Welcome {member.mention} to the server!",
            color=0x00bfff  # آبی برای ولکام
        )
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.set_image(url=WELCOME_IMAGE)
        embed.set_footer(text="Enjoy your stay ❄️")
        await channel.send(embed=embed)

# ================= TICKET SYSTEM =================
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📝 Ozviat", style=discord.ButtonStyle.green)
    async def ozviat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Ozviat")

    @discord.ui.button(label="📞 Ertebat ba HG", style=discord.ButtonStyle.blurple)
    async def ertebat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Ertebat ba HG")

async def create_ticket(interaction, reason):
    global ticket_counter
    guild = interaction.guild

    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
    if not category:
        category = await guild.create_category(CATEGORY_NAME)

    role = discord.utils.get(guild.roles, name=SUPPORT_ROLE)  # رول اصلاح شد

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }
    if role:
        overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

    channel_name = f"ticket-{ticket_counter}-{interaction.user.name}".lower()
    ticket_counter += 1

    channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)

    embed = discord.Embed(
        title="🎫 Ticket Created",
        description=f"👤 User: {interaction.user.mention}\n📌 Reason: {reason}",
        color=0x00ff00
    )
    await channel.send(embed=embed, view=CloseTicketView())
    await interaction.response.send_message(f"🎫 تیکت ساخته شد: {channel.mention}", ephemeral=True)

class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 تیکت بسته شد", ephemeral=True)
        await interaction.channel.delete()

# ================= NORMAL COMMANDS =================
@bot.command()
async def ping(ctx):
    embed = discord.Embed(description="🏓 Pong!", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command()
async def ticket(ctx):
    embed = discord.Embed(title="❄ Blizzard Ticket System ❄", description="یکی از گزینه‌ها رو انتخاب کن:", color=0x00ff00)
    await ctx.send(embed=embed, view=TicketView())

# ================= /ROB COMMAND =================
@bot.tree.command(name="rob", description="Send green embed")
@app_commands.describe(text="متنی که میخوای داخل Embed باشه")
async def rob(interaction: discord.Interaction, text: str):
    embed = discord.Embed(
        title=text,
        color=0x00ff00
    )
    await interaction.response.send_message(embed=embed)

# ================= /LOSE COMMAND =================
@bot.tree.command(name="lose", description="Send red embed")
@app_commands.describe(text="متنی که میخوای داخل Embed باشه")
async def lose(interaction: discord.Interaction, text: str):
    embed = discord.Embed(
        title=text,
        color=0xff0000
    )
    await interaction.response.send_message(embed=embed)

# ================= READY =================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is online!")

# ================= RUN BOT =================
bot.run(TOKEN)
