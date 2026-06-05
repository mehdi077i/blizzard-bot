import discord
from discord.ext import commands
from discord.ui import View, Button
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CATEGORY_NAME = "✉️・𝗧𝗶𝗰𝗸𝗲𝘁"
SUPPORT_ROLE = "Tiket supporter"

# ---------------- Ticket System ----------------

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
    guild = interaction.guild

    # پیدا کردن یا ساخت کتگوری
    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
    if not category:
        category = await guild.create_category(CATEGORY_NAME)

    # رول ساپورت
    role = discord.utils.get(guild.roles, name=SUPPORT_ROLE)

    # دسترسی‌ها
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }
    if role:
        overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

    # ساخت چنل
    channel = await guild.create_text_channel(
        name=f"ticket-{interaction.user.name}",
        category=category,
        overwrites=overwrites
    )

    await channel.send(
        f"{interaction.user.mention} تیکت شما ساخته شد ✅ دلیل: **{reason}**",
        view=CloseTicketView()
    )

    await interaction.response.send_message(
        f"🎫 تیکت ساخته شد: {channel.mention}",
        ephemeral=True
    )


class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name=SUPPORT_ROLE)
        if role not in interaction.user.roles:
            await interaction.response.send_message("❌ شما اجازه بستن تیکت را ندارید!", ephemeral=True)
            return

        await interaction.response.send_message("🔒 تیکت بسته شد", ephemeral=True)
        await interaction.channel.delete()

# ---------------- Welcome System ----------------

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="💠・𝘞𝘦𝘭𝘤𝘰𝘮𝘦")
    if channel:
        embed = discord.Embed(
            title="❄️ Welcome to Blizzard ❄️",
            description=f"Glad to have you here, {member.mention}!",
            color=0x00bfff
        )
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.set_footer(text="Enjoy your stay ❄️")
        await channel.send(embed=embed)

# ---------------- Commands ----------------

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def ticket(ctx):
    await ctx.send("❄ Blizzard Ticket Dashboard ❄", view=TicketView())

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

bot.run(TOKEN)
