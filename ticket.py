import discord
from discord.ext import commands
from discord.ui import View, Button
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")  # توکن رو از env بخون

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# دکمه‌ها
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="ozviat", style=discord.ButtonStyle.green, custom_id="ozviat"))
        self.add_item(Button(label="ertebat ba hg", style=discord.ButtonStyle.blurple, custom_id="ertebat"))

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.top_role.name != "Tiket supporter":
            await interaction.response.send_message("شما اجازه بستن تیکت را ندارید!", ephemeral=True)
            return
        await interaction.channel.delete()

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def ticket(ctx):
    view = TicketView()
    await ctx.send("❄ Blizzard Ticket Dashboard ❄", view=view)

# ساخت تیکت جدید وقتی دکمه‌ها کلیک شدند
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    if interaction.data["custom_id"] in ["ozviat", "ertebat"]:
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        category = discord.utils.get(guild.categories, name="✉️・𝗧𝗶𝗰𝗸𝗲𝘁")
        if not category:
            category = await guild.create_category("✉️・𝗧𝗶𝗰𝗸𝗲𝘁")

        channel_name = f"ticket-{interaction.user.name}".lower()
        ticket_channel = await guild.create_text_channel(
            channel_name, category=category, overwrites=overwrites
        )
        await ticket_channel.send(
            f"{interaction.user.mention} تیکت شما ساخته شد! رول Tiket supporter می‌تواند پاسخ دهد."
        )
        await interaction.response.send_message(f"تیکت شما ساخته شد: {ticket_channel.mention}", ephemeral=True)

bot.run(TOKEN)
