import discord
from discord.ext import commands
from discord.ui import View
from discord import app_commands
import os
from dotenv import load_dotenv
import json

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

# ================= COUNTER =================
def load_ticket_counter():
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, "r") as f:
            return json.load(f).get("counter", 1)
    return 1

def save_ticket_counter(counter):
    with open(TICKET_FILE, "w") as f:
        json.dump({"counter": counter}, f)

ticket_counter = load_ticket_counter()

# ================= WELCOME =================
@bot.event
async def on_member_join(member):
    await bot.wait_until_ready()

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="❄️ Welcome to Blizzard ❄️",
        description=f"Welcome {member.mention} to the server!",
        color=0x3498db
    )
    embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
    embed.set_image(url=WELCOME_IMAGE)
    embed.set_footer(text="Enjoy your stay ❄️")

    await channel.send(embed=embed)

# ================= TICKET VIEW =================
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📝 عضویت", style=discord.ButtonStyle.blurple)
    async def a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "عضویت")

    @discord.ui.button(label="📞 ارتباط با HG", style=discord.ButtonStyle.blurple)
    async def b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "ارتباط با HG")

# ================= CREATE TICKET =================
async def create_ticket(interaction, reason):
    global ticket_counter

    try:
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild

        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
        if not category:
            category = await guild.create_category(CATEGORY_NAME)

        role = guild.get_role(SUPPORT_ROLE_ID)
        if not role:
            await interaction.followup.send("❌ Support role not found", ephemeral=True)
            return

        # جلوگیری از تیکت تکراری
        for ch in category.channels:
            if ch.topic == str(interaction.user.id):
                await interaction.followup.send(f"❌ شما قبلاً تیکت دارید: {ch.mention}", ephemeral=True)
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{ticket_counter}",
            category=category,
            overwrites=overwrites,
            topic=str(interaction.user.id)  # 👈 مالک واقعی
        )

        ticket_counter += 1
        save_ticket_counter(ticket_counter)

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
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = interaction.guild.get_role(SUPPORT_ROLE_ID)
        owner_id = interaction.channel.topic

        if str(interaction.user.id) != owner_id and role not in interaction.user.roles:
            await interaction.response.send_message("❌ اجازه نداری!", ephemeral=True)
            return

        await interaction.response.send_message("🔒 تیکت بسته شد", ephemeral=True)
        await interaction.channel.delete()

# ================= COMMANDS =================
@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="❄ Blizzard Ticket System ❄",
        description="روی دکمه‌ها کلیک کن",
        color=0x3498db
    )
    await ctx.send(embed=embed, view=TicketView())

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# ================= READY =================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is online!")

# ================= RUN =================
bot.run(TOKEN)
