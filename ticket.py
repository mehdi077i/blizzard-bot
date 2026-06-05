import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TICKET_CHANNEL_NAME = "📩・𝘛𝘪𝘤𝘬𝘦𝘵"

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

# دکمه‌ها
class TicketView(discord.ui.View):
    @discord.ui.button(label="📝 Ozviat", style=discord.ButtonStyle.primary)
    async def ozviat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "ozviat")

    @discord.ui.button(label="📞 Ertebat ba HG", style=discord.ButtonStyle.secondary)
    async def hg(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "hg")


async def create_ticket(interaction, ticket_type):
    guild = interaction.guild
    user = interaction.user

    channel_name = f"ticket-{user.name}-{ticket_type}"

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }

    channel = await guild.create_text_channel(
        name=channel_name,
        overwrites=overwrites
    )

    await channel.send(f"🎫 تیکت جدید برای {user.mention} ساخته شد!")
    await interaction.response.send_message(f"تیکت ساخته شد: {channel.mention}", ephemeral=True)


@bot.command()
async def ticket(ctx):
    channel = discord.utils.get(ctx.guild.text_channels, name=TICKET_CHANNEL_NAME)

    if not channel:
        await ctx.send("کانال تیکت پیدا نشد!")
        return

    embed = discord.Embed(
        title="❄️ Blizzard Ticket System",
        description="یکی از گزینه‌ها رو انتخاب کن:",
        color=0x00bfff
    )

    await channel.send(embed=embed, view=TicketView())

# توکن از env
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
