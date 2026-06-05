import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CATEGORY_NAME = "✉️・𝗧𝗶𝗰𝗸𝗲𝘁"
SUPPORT_ROLE_NAME = "Ticket supporter"


# ================== Ticket Dashboard ==================
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📝 Ozviat", style=discord.ButtonStyle.primary)
    async def ozviat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "Ozviat")

    @discord.ui.button(label="📞 Ertebat ba HG", style=discord.ButtonStyle.secondary)
    async def hg(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "Ertebat ba HG")

    async def create_ticket(self, interaction, reason):
        guild = interaction.guild

        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
        if not category:
            category = await guild.create_category(CATEGORY_NAME)

        support_role = discord.utils.get(guild.roles, name=SUPPORT_ROLE_NAME)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        await interaction.response.send_message(
            f"🎫 تیکت ساخته شد: {channel.mention}",
            ephemeral=True
        )

        await channel.send(
            f"سلام {interaction.user.mention} 👋\n"
            f"تیکت شما برای: **{reason}** ساخته شد.\n"
            f"پشتیبان‌ها پاسخ میدن به زودی."
        )

        await channel.send(view=CloseTicketView())


# ================== Close Ticket ==================
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        support_role = discord.utils.get(interaction.guild.roles, name=SUPPORT_ROLE_NAME)

        # فقط ساپورت یا صاحب تیکت بتونه ببنده
        if support_role not in interaction.user.roles and interaction.channel.name.startswith("ticket-"):

            # اجازه برای صاحب تیکت
            if interaction.channel.name.replace("ticket-", "") != interaction.user.name:
                return await interaction.response.send_message(
                    "❌ شما اجازه بستن این تیکت را ندارید.",
                    ephemeral=True
                )

        await interaction.response.send_message("🔒 تیکت بسته شد...", ephemeral=True)
        await interaction.channel.delete()


# ================== Ticket Command ==================
@bot.command()
async def ticket(ctx):
    await ctx.send("❄ Blizzard Ticket Dashboard ❄", view=TicketView())


# ================== Ready ==================
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


bot.run(TOKEN)
