import discord
from discord.ext import commands
import os  # برای خوندن توکن از محیط

# Intent ها
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# ساخت بات
bot = commands.Bot(command_prefix="!", intents=intents)

# روشن شدن بات
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

# ولکام
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
        embed.set_image(
            url="https://media.discordapp.net/attachments/1360652773636575525/1512134315633283275/shayan.png"
        )
        embed.set_footer(
            text="Enjoy your stay in Blizzard ❄️"
        )
        await channel.send(embed=embed)

# دستور پینگ
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

# آخر فایل: فقط یک خط امن
TOKEN = os.getenv("TOKEN")  # <- اینجا هیچ توکنی ننویس
bot.run(TOKEN)
