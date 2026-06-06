import discord
from discord.ext import commands
from discord.ui import View
from discord import app_commands
import os
from dotenv import load_dotenv
import json
import asyncio

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
CATEGORY_NAME = "✉️・Ticket"
SUPPORT_ROLE_ID = 1512090091391029409
WELCOME_CHANNEL_ID = 1345757711211434034
WELCOME_IMAGE = "https://media.discordapp.net/attachments/1360652773636575525/1512134315633283275/shayan.png"

TICKET_FILE = "ticket_counter.json"
WELCOME_LOG = set()  # جلوگیری از multiple welcome

# ================= HELPER FUNCTIONS =================
def load_ticket_counter():
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, "r") as f:
            data = json.load(f)
            return data.get("counter", 1)
    return 1

def save_ticket_counter(counter):
    with open(TICKET_FILE, "w") as f:
        json.dump({"counter": counter}, f)

ticket_counter = load_ticket_counter()

# ================= WELCOME SYSTEM =================
@bot.event
async def on_member_join(member):
    if not bot.is_ready():
        await bot.wait_until_ready()
    if member.id in WELCOME_LOG:
        return
    WELCOME_LOG.add(member.id)

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="❄️ Welcome to Blizzard ❄️",
            description=f"Welcome {member.mention} to the server!",
            color=0x3498db
        )
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.set_image(url=WELCOME_IMAGE)
        embed.set_footer(text="Enjoy your stay ❄️")
        await channel.send(embed=embed)

# ================= TICKET SYSTEM =================
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📝 عضویت", style=discord.ButtonStyle.blurple)
    async def ozviat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "عضویت")

    @discord.ui.button(label="📞 ارتباط با HG", style=discord.ButtonStyle.blurple)
    async def ertebat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "ارتباط با HG")

async def create_ticket(interaction, reason):
    global ticket_counter

    try:
        guild = interaction.guild

        # defer فوری
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        # گرفتن یا ساخت category
        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
        if not category:
            category = await guild.create_category(CATEGORY_NAME)

        role = guild.get_role(SUPPORT_ROLE_ID)
        if role is None:
            await interaction.followup.send("❌ رول ساپورت پیدا نشد!", ephemeral=True)
            return

        # جلوگیری از duplicate ticket
        existing = [ch for ch in category.channels if getattr(ch, "owner", None) == interaction.user]
        if existing:
            await interaction.followup.send(f"❌ شما قبلا تیکت ساختید: {existing[0].mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }

        channel_name = f"ticket-{ticket_counter}-{interaction.user.name}".lower()
        ticket_counter += 1
        save_ticket_counter(ticket_counter)

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        setattr(channel, "owner", interaction.user)

        embed = discord.Embed(
            title="🎫 Ticket Created",
            description=f"👤 User: {interaction.user.mention}\n📌 Reason: {reason}",
            color=0x3498db
        )
        embed.set_footer(text="Blizzard Support System")

        await channel.send(
            content=f"{interaction.user.mention} | {role.mention}",
            embed=embed,
            view=CloseTicketView()
        )

        await interaction.followup.send(
            f"🎫 تیکت ساخته شد: {channel.mention}",
            ephemeral=True
        )

    except Exception as e:
        print("Ticket error:", e)
        try:
            await interaction.followup.send("❌ خطا در ساخت تیکت!", ephemeral=True)
        except:
            pass

# ================= CLOSE TICKET =================
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 بستن تیکت", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(SUPPORT_ROLE_ID)
        if interaction.user != getattr(interaction.channel, 'owner', None) and role not in interaction.user.roles:
            await interaction.response.send_message("❌ اجازه نداری!", ephemeral=True)
            return

        await interaction.response.send_message("🔒 تیکت بسته شد", ephemeral=True)
        await interaction.channel.delete()

# ================= COMMANDS =================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="❄ Blizzard Ticket System ❄",
        description="یکی از گزینه‌ها رو انتخاب کن:",
        color=0x3498db
    )
    await ctx.send(embed=embed, view=TicketView())

# ================= SLASH COMMANDS =================
@bot.tree.command(name="rob", description="Send green embed")
@app_commands.describe(text="متن")
async def rob(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    embed = discord.Embed(title=text, color=0x2ecc71)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="lose", description="Send red embed")
@app_commands.describe(text="متن")
async def lose(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    embed = discord.Embed(title=text, color=0xe74c3c)
    await interaction.followup.send(embed=embed)

# ================= READY =================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is online!")

# ================= RUN =================
bot.run(TOKEN)
