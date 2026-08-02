import discord
from discord import app_commands
from discord.ext import commands
import os
import json
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ========== CONFIGURATION ==========
TOKEN = ""

WELCOME_CHANNEL_ID = 893706647535505429
AUTO_ROLE_ID = 888491577058680862
SUPPORT_ROLE_ID = 905165989463883867

ADMIN_STATOR_ROLE_IDS = [
    1142298941027782736,
    881211189219180555,
    903086167807889418
]

ALLOWED_ROB_ROLE_ID = 897069594404077578
ALLOWED_FINE_ROLE_ID = 1161411709353869382
ALLOWED_DONE_ROLE_ID = 897069594404077578

ALLOWED_ROB_CHANNEL_ID = 1127748882831519844
ALLOWED_FINE_CHANNEL_ID = 1012585350000025620

OZVIAT_CATEGORY_ID = 1127721864928694373
MAVARED_CATEGORY_ID = 1127722330207047721

NAVAR_RANG = 0x0a0a0a
GIF_URL = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTFmOTBxam9oN2NhdndmdjlqbXByY3IzYWl3NXFmNG5yN3QyaWM2NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SIB7qo2jm6bxpbGUqO/giphy.gif"
SWASTIK_EMOJI = "<:SwasTik:1115049626165329931>"

# Task Panel Config
ALLOWED_TASK_CHANNEL_ID = 1167934459170009298

# ========== رول‌های مجاز برای کامند !taskpanel ==========
ALLOWED_TASK_PANEL_ROLE_IDS = [
    1142298941027782736,
    881211189219180555,
    894797158627287040,
    903086167807889418
]

# ========== TASK PANEL STORAGE ==========
PANEL_TASK_FILE = "task_panel_data.json"

def save_task_panel(channel_id, message_id):
    data = {"channel_id": channel_id, "message_id": message_id}
    with open(PANEL_TASK_FILE, "w") as f:
        json.dump(data, f)

def load_task_panel():
    try:
        with open(PANEL_TASK_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def delete_task_panel():
    try:
        os.remove(PANEL_TASK_FILE)
    except:
        pass

# ========== TICKET PANEL STORAGE ==========
PANEL_FILE = "panel_data.json"

def save_panel(channel_id, message_id):
    data = {"channel_id": channel_id, "message_id": message_id}
    with open(PANEL_FILE, "w") as f:
        json.dump(data, f)

def load_panel():
    try:
        with open(PANEL_FILE, "r") as f:
            return json.load(f)
    except:
        return None

# ========== ADMIN CHECK FUNCTION ==========
def is_admin_stator(member):
    for role_id in ADMIN_STATOR_ROLE_IDS:
        role = member.guild.get_role(role_id)
        if role and role in member.roles:
            return True
    return False

# ========== CHECK FUNCTION FOR TASK PANEL ==========
def has_task_panel_access(member):
    for role_id in ALLOWED_TASK_PANEL_ROLE_IDS:
        role = member.guild.get_role(role_id)
        if role and role in member.roles:
            return True
    return False

# ========== TICKET CLASSES ==========
class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="𝗢𝘇𝘃𝗶𝗮𝗧", style=discord.ButtonStyle.success, row=0)
    async def ozviat_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await self.create_ticket(interaction, "𝗢𝘇𝘃𝗶𝗮𝗧", "ozviat_form")
    
    @discord.ui.button(label="𝗠𝗮𝘃𝗮𝗿𝗲𝗱 𝗱𝗶𝗴𝗮𝗿", style=discord.ButtonStyle.primary, row=0)
    async def mavared_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await self.create_ticket(interaction, "𝗠𝗮𝘃𝗮𝗿𝗲𝗱 𝗱𝗶𝗴𝗮𝗿", "mavared_simple")
    
    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str, template: str):
        try:
            guild = interaction.guild
            user = interaction.user
            
            # ========== همه کاربران میتونن تیکت باز کنن ==========
            
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel) and (
                    channel.name == f"Ozviat-{user.name}" or 
                    channel.name == f"Mavared-{user.name}"
                ):
                    await interaction.followup.send("❌ You already have an open ticket!", ephemeral=True)
                    return
            
            support_role = guild.get_role(SUPPORT_ROLE_ID)
            
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
            
            if support_role:
                overwrites[support_role] = discord.PermissionOverwrite(
                    view_channel=True, 
                    send_messages=True, 
                    read_message_history=True
                )
            
            if template == "ozviat_form":
                ozviat_category = guild.get_channel(OZVIAT_CATEGORY_ID)
                channel = await guild.create_text_channel(
                    name=f"Ozviat-{user.name}",
                    overwrites=overwrites,
                    category=ozviat_category,
                    topic=f"{ticket_type} | {user.name}"
                )
                
                # ========== متن تیکت عضویت با فونت معمولی ==========
                embed = discord.Embed(
                    description=f"""
**Salam <@!{user.id}> aziz, Lotfan Form Zir Ro Kamel Va Dar Hamin Channel Ersal Konid Va Montazer Pasokh Bashid**

- Mizan Time play khod Dar ruz ?
- Level Shoma Dar Server Sunset ?
- Dalile Vurud Be Team ?
- Sen Shoma ?

**Baraye bastan Ticket mitavanid az gozine zir Estefade Konid**
""",
                    color=NAVAR_RANG
                )
                embed.set_thumbnail(url=GIF_URL)
                close_view = CloseTicketView(user.id, user.name, ticket_type, support_role)
                await channel.send(embed=embed, view=close_view)
            
            elif template == "mavared_simple":
                mavared_category = guild.get_channel(MAVARED_CATEGORY_ID)
                channel = await guild.create_text_channel(
                    name=f"Mavared-{user.name}",
                    overwrites=overwrites,
                    category=mavared_category,
                    topic=f"{ticket_type} | {user.name}"
                )
                
                # ========== متن تیکت موارد دیگر با فونت معمولی ==========
                embed = discord.Embed(
                    description=f"""
**Salam <@!{user.id}> aziz**

**Age Soal Ya DarkhasTi Darid Hamin Ja Ersal Va Montazer Pasokh Bashid**
""",
                    color=NAVAR_RANG
                )
                embed.set_thumbnail(url=GIF_URL)
                close_view = CloseTicketView(user.id, user.name, ticket_type, support_role)
                await channel.send(embed=embed, view=close_view)
            
        except Exception as e:
            print(f"Error creating ticket: {e}")
            try:
                await interaction.followup.send("❌ An error occurred while creating the ticket!", ephemeral=True)
            except:
                pass


class CloseTicketView(discord.ui.View):
    def __init__(self, user_id, user_name, ticket_type, support_role):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.user_name = user_name
        self.ticket_type = ticket_type
        self.support_role = support_role
    
    @discord.ui.button(label="𝗖𝗹𝗼𝘀𝗲 𝗧𝗶𝗰𝗸𝗲𝗧", style=discord.ButtonStyle.danger, row=0)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.id != self.user_id and not interaction.user.guild_permissions.administrator:
                if self.support_role and self.support_role not in interaction.user.roles:
                    await interaction.response.send_message("❌ You don't have permission to close this ticket!", ephemeral=True)
                    return
            
            await interaction.response.send_message("🔒 Ticket is closing...")
            
            if not os.path.exists("ticket_logs"):
                os.makedirs("ticket_logs")
            
            filename = f"ticket_logs/{interaction.channel.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"TICKET: {interaction.channel.name}\nTYPE: {self.ticket_type}\nCREATOR: {self.user_name}\nCLOSED BY: {interaction.user.name}\nTIME: {datetime.now()}\n")
            
            await interaction.channel.delete()
            
        except Exception as e:
            print(f"Error closing ticket: {e}")


# ========== TICKET COMMANDS ==========
@bot.command(name="ticket")
async def ticket_panel(ctx):
    if not is_admin_stator(ctx.author):
        await ctx.send(
            "❌ You don't have permission to use this command!\nOnly users with Administrator roles can use the ticket panel.",
            delete_after=5
        )
        return
    
    embed = discord.Embed(
        title="<:X_:1373302115660730490> **Alliance ™** <:X_:1373302115660730490>",
        description="**Bara Baz Kardan Ticket Mored Nazar\nYeki az Gozine Haye Zir Ro Entekhab Konid**",
        color=NAVAR_RANG
    )
    embed.set_thumbnail(url=GIF_URL)
    
    view = TicketButtons()
    message = await ctx.send(embed=embed, view=view)
    
    save_panel(ctx.channel.id, message.id)
    await ctx.send("✅ Ticket panel created and saved!")


@bot.command(name="close")
async def force_close(ctx):
    if not ctx.channel.name.startswith(("Ozviat-", "Mavared-")):
        return
    await ctx.send("🔒 Ticket is closing...")
    await ctx.channel.delete()


@bot.command(name="reload_panel")
async def reload_panel(ctx):
    if not is_admin_stator(ctx.author):
        await ctx.send("❌ You don't have permission!", delete_after=5)
        return
    
    await ticket_panel(ctx)
    await ctx.send("✅ Ticket panel reloaded!", delete_after=5)


# ========== SLASH COMMAND: /rob ==========
@bot.tree.command(name="rob", description="Robbery System")
@app_commands.choices(
    name=[
        app_commands.Choice(name="𝗕𝗹𝗮𝗶𝗻", value="𝗕𝗹𝗮𝗶𝗻"),
        app_commands.Choice(name="𝗕𝗶𝗺𝗲", value="𝗕𝗶𝗺𝗲"),
        app_commands.Choice(name="𝗖𝗮𝗿𝗴𝗼", value="𝗖𝗮𝗿𝗴𝗼"),
        app_commands.Choice(name="𝗙𝗹𝗮𝗧", value="𝗙𝗹𝗮𝗧"),
        app_commands.Choice(name="𝗠𝗮𝗿𝗸𝗮𝘇𝗶", value="𝗠𝗮𝗿𝗸𝗮𝘇𝗶"),
        app_commands.Choice(name="𝗠𝗮𝘇𝗲", value="𝗠𝗮𝘇𝗲"),
        app_commands.Choice(name="𝗣𝗮𝗹𝗲𝘁𝗼", value="𝗣𝗮𝗹𝗲𝘁𝗼"),
        app_commands.Choice(name="𝗦𝗵𝗮𝗵𝗿", value="𝗦𝗵𝗮𝗵𝗿"),
        app_commands.Choice(name="𝗦𝗵𝗮𝗺𝘀", value="𝗦𝗵𝗮𝗺𝘀"),
        app_commands.Choice(name="𝗔𝗶𝗿", value="𝗔𝗶𝗿")
    ],
    status=[
        app_commands.Choice(name="𝗪𝗶𝗻", value="Win"),
        app_commands.Choice(name="𝗟𝗼𝘀𝗲", value="Lose")
    ]
)
async def rob(interaction: discord.Interaction, name: app_commands.Choice[str], status: app_commands.Choice[str]):
    if interaction.channel_id != ALLOWED_ROB_CHANNEL_ID:
        embed = discord.Embed(
            description="❌ This command can only be used in the designated robbery channel!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    has_access = False
    ALLOWED_ROB_ROLE_IDS = [
        1142298941027782736,
        881211189219180555,
        903086167807889418,
        897069594404077578
    ]
    
    for role_id in ALLOWED_ROB_ROLE_IDS:
        role = interaction.guild.get_role(role_id)
        if role and role in interaction.user.roles:
            has_access = True
            break
    
    if not has_access:
        embed = discord.Embed(
            description="❌ You don't have permission to use this command!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    await interaction.response.send_message("✅ Processing...", ephemeral=True)
    
    if status.value == "Win":
        color = discord.Color.green()
        status_display = "𝗪𝗶𝗻"
    else:
        color = discord.Color.red()
        status_display = "𝗟𝗼𝘀𝗲"
    
    embed = discord.Embed(
        title=f"𝗥𝗼𝗯𝗯𝗲𝗿𝘆 {SWASTIK_EMOJI}",
        description=f"{name.value} / {status_display}",
        color=color
    )
    
    await interaction.channel.send(embed=embed)
    await interaction.delete_original_response()


# ========== SLASH COMMAND: /say ==========
@bot.tree.command(name="say", description="Send message through bot")
async def say(interaction: discord.Interaction, message: str):
    if not is_admin_stator(interaction.user):
        embed = discord.Embed(
            description="❌ You don't have permission to use this command!\nOnly users with Administrator roles can use this command.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        description=message,
        color=NAVAR_RANG
    )
    
    await interaction.channel.send(embed=embed)
    await interaction.response.defer()
    await interaction.delete_original_response()


# ========== SLASH COMMAND: /fine ==========
@bot.tree.command(name="fine", description="Command for fine")
@app_commands.describe(
    member="User name or ID",
    amount="Fine amount"
)
async def fine(interaction: discord.Interaction, member: str, amount: str):
    if interaction.channel_id != ALLOWED_FINE_CHANNEL_ID:
        embed = discord.Embed(
            description="❌ This command can only be used in the designated fine channel!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    has_access = False
    ALLOWED_FINE_ROLE_IDS = [
        1142298941027782736,
        881211189219180555,
        903086167807889418,
        1161411709353869382
    ]
    
    for role_id in ALLOWED_FINE_ROLE_IDS:
        role = interaction.guild.get_role(role_id)
        if role and role in interaction.user.roles:
            has_access = True
            break
    
    if not has_access:
        embed = discord.Embed(
            description="❌ You don't have permission to use this command!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    user_mention = member
    if member.isdigit():
        user_mention = f"<@{member}>"
    
    message = f"""{user_mention} 𝗔𝘇𝗶𝘇 𝗦𝗵𝗼𝗺𝗮 𝗠𝗮𝗯𝗹𝗮𝗴𝗵 {amount} 𝗝𝗮𝗿𝗶𝗺𝗲 𝗦𝗵𝗼𝗱𝗶𝗱

𝗛𝗮𝗧𝗺𝗮𝗻 𝗕𝗮𝗿𝗮𝘆𝗲 𝗣𝗮𝗿𝗱𝗮𝗸𝗵𝗧 𝗝𝗮𝗿𝗶𝗺𝗲 𝗕𝗮 𝗦𝗵𝗮𝗸𝗵𝘀 𝗖𝗮𝗿𝗟𝗼𝗴𝗲𝗿 𝗗𝗮𝗿 𝗘𝗿𝗧𝗲𝗯𝗮𝗧 𝗕𝗮𝘀𝗵𝗶𝗱 !"""
    
    embed = discord.Embed(
        description=message,
        color=discord.Color.blue()
    )
    
    await interaction.channel.send(embed=embed)
    await interaction.response.defer()
    await interaction.delete_original_response()


# ========== TASK PANEL CLASSES ==========
class TaskSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="[200] Khurde Aluminium - [50] Khurde Ahan",
                value="task_done"
            )
        ]
        super().__init__(
            placeholder="Gozine mored nazar ro entekhab konid...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        # ========== همه کاربران میتونن گزینه رو انتخاب کنن ==========
        
        # ========== ارسال پیام ثبت تسک ==========
        embed = discord.Embed(
            description=f"{interaction.user.mention} **Task khodesh Ro anjam Dad**",
            color=NAVAR_RANG
        )
        
        embed.add_field(
            name="",
            value="**[200] Khurde Aluminium - [50] Khurde Ahan**",
            inline=False
        )
        
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ Your task has been registered!", ephemeral=True)


class TaskPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TaskSelect())


# ========== COMMAND: !taskpanel ==========
@bot.command(name="taskpanel")
async def taskpanel_command(ctx):
    # Check channel
    if ctx.channel.id != ALLOWED_TASK_CHANNEL_ID:
        embed = discord.Embed(
            description="❌ This command can only be used in the designated task channel!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    # Check user roles
    if not has_task_panel_access(ctx.author):
        embed = discord.Embed(
            description="❌ You don't have permission to use this command!\nOnly users with the required roles can create the task panel.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    # Create dashboard-style panel
    embed = discord.Embed(
        title="**Alliance Team Weekly Tasks**",
        description=(
            "Dar SuraTi ke Task Ro anjam Dadid\n"
            "Gozine Zir MarbuT Be Task ro EnTekhab Konid"
        ),
        color=NAVAR_RANG
    )
    
    view = TaskPanelView()
    message = await ctx.send(embed=embed, view=view)
    
    # Save panel data for future reference
    save_task_panel(ctx.channel.id, message.id)
    await ctx.send("✅ Task panel created and saved!", delete_after=3)


# ========== WELCOME EVENT ==========
@bot.event
async def on_member_join(member):
    if not member.bot:
        role = member.guild.get_role(AUTO_ROLE_ID)
        if role:
            try:
                await member.add_roles(role)
                print(f"✅ Role {role.name} added to {member.name}")
            except Exception as e:
                print(f"❌ Error adding role to {member.name}: {e}")
        else:
            print(f"❌ Role with ID {AUTO_ROLE_ID} not found!")
    
    if not member.bot:
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        
        if channel is None:
            print(f"❌ Welcome channel with ID {WELCOME_CHANNEL_ID} not found!")
            return
        
        # ========== متن ولکام با فونت معمولی ==========
        embed = discord.Embed(
            description=f"""**Hey {member.mention}, Welcome To Alliance ᵀᴹ**


Thank you For joining us.""",
            color=NAVAR_RANG
        )
        
        embed.set_thumbnail(url=GIF_URL)
        await channel.send(embed=embed)


# ========== ON READY EVENT ==========
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot {bot.user} is ready!")
    await bot.change_presence(activity=discord.Game("・"), status=discord.Status.online)
    
    print("ℹ️ Bot is online. Use !taskpanel to create task panel.")
    print("ℹ️ Use !ticket to create ticket panel.")
    print("✅ Bot is ready!")


if __name__ == "__main__":
    bot.run(TOKEN)
