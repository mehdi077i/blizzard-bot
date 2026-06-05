import discord
from discord.ext import commands
from discord.ui import View
from discord import app_commands
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

ticket_counter = 1

# ================= Ticket System =================

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

    role = discord.utils.get(guild.roles, name=SUPPORT_ROLE)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }

    if role:
        overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

    channel_name = f"ticket-{ticket_counter}-{interaction.user.name}".lower()
    ticket_counter += 1

    channel = await guild.create_text_channel(
        name=channel_name,
        category=category,
        overwrites=overwrites
    )

    await channel.send(
        f"{interaction.user.mention} تیکت شما ساخته شد ✅ دلیل: **{reason}**",
        view=CloseTicketView(interaction.user.id)
    )

    await interaction.response.send_message(
        f"🎫 تیکت ساخته شد: {channel.mention}",
        ephemeral=True
    )


class CloseTicketView(View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = discord.utils.get(interaction.guild.roles, name=SUPPORT_ROLE)

        is_owner = interaction.user.id == self.owner_id
        is_support = role in interaction.user.roles if role else False

        if not (is_owner or is_support):
            return await interaction.response.send_message(
                "❌ فقط صاحب تیکت یا ساپورت می‌تونه ببنده!",
                ephemeral=True
            )

        await interaction.response.send_message("🔒 تیکت بسته شد", ephemeral=True)
        await interaction.channel.delete()

# ================= Welcome =================

@bot.event
async def on_member_join(member):

    channel = discord.utils.get(
        member.guild.text_channels,
        name="💠・𝘞𝘦𝘭𝘤𝘰𝘮𝘦"
    )

    if channel:
        embed = discord.Embed(
            title="❄️ Welcome to Blizzard ❄️",
            description=f"Glad to have you here, {member.mention}!",
            color=0x00bfff
        )

        embed.set_author(
            name=member.display_name,
            icon_url=member.display_avatar.url
        )

        embed.set_footer(text="Enjoy your stay ❄️")

        await channel.send(embed=embed)

# ================= Commands =================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def ticket(ctx):
    await ctx.send(
        "❄ Blizzard Ticket Dashboard ❄",
        view=TicketView()
    )

# ================= Slash Command /rob =================

@bot.tree.command(name="rob", description="Send any text")
@app_commands.describe(text="متنی که میخوای ارسال بشه")
async def rob(interaction: discord.Interaction, text: str):

    await interaction.response.send_message(text)

# ================= Ready =================

@bot.event
async def on_ready():

    await bot.tree.sync()

    print(f"{bot.user} is online!")

bot.run(TOKEN)
