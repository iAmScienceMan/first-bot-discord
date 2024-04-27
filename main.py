import discord
from discord.ext import commands
import random
import datetime
import asyncio

# dotenv start
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
# dotenv end

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# 8ball answers
ball_answers = [
    "Yes",
    "No",
    "Maybe",
    "Try again later",
    "Definitely",
    "Absolutely not"
]

# On Ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()

# answer to any "kys" as "nah i'd do my own thing"
@bot.event
async def on_kys(message):
    if message.author == bot.user:
        return

    if "kys" in message.content.lower():
        await message.channel.send("nah i'd do my own thing")

    await bot.process_commands(message)

# Old way to check for permissions
'''
async def has_permissions(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    else:
        await ctx.send("You don't have permission to use this command.")
        return False
'''

# Ping command
@bot.hybrid_command()
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")

# Help command
bot.remove_command('help')
@bot.hybrid_command(name='help', description='Displays all available commands with their descriptions.')
async def help(ctx):
    embed = discord.Embed(
        title='Available Commands',
        description='List of all available commands with their descriptions:',
        color=discord.Color.blue()
    )

    for command in bot.commands:
        if not command.hidden:
            embed.add_field(name=f'/{command.name}', value=command.description or 'No description provided.', inline=False)
            embed.set_footer(text='powered by iamscienceman')

    await ctx.send(embed=embed)

# Echo command
@bot.hybrid_command(name='echo',description="If bot's online, it'll answer with what you've said.")
async def echo(ctx,msg):
    await ctx.send(msg)

# Poll command
@bot.hybrid_command(name='poll',description="Creates a poll that user can vote on.")  
async def poll(ctx, question, option1, option2, option3: str = "", option4: str = "", option5: str = "", option6: str = "", option7: str = "", option8: str = "", option9: str = "", option10: str = ""):
    options = [
        option1,
        option2,
        option3,
        option4,
        option5,
        option6,
        option7,
        option8,
        option9,
        option10
    ]

    options = [sublist for sublist in options if any(item.strip() for item in sublist)]
    if len(options) <= 1:
        await ctx.send("You need to provide a question and at least 2 options for the poll.",delete_after=5)
        return

    if len(options) > 10:
        await ctx.send("You can't have more than 10 options for the poll.",delete_after=5)
        return

    poll_message = f"# {question}\n\n"

    for i, option in enumerate(options, start=1):
        poll_message += f"{i}. {option}\n"

    poll_message += "\nReact with the corresponding number to vote!"

    poll = await ctx.send(poll_message)

    for i in range(1, min(len(options) + 1, 10)):
        await poll.add_reaction(f"{i}\u20e3")

    if len(options) == 10:
        await poll.add_reaction("\U0001f51f")

# Userinfo command
@bot.hybrid_command(name='userinfo',description="Displays user info.")
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    embed = discord.Embed(title="User Information", color=discord.Color.blue())
    
    if member.bot:
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Bot", value=True, inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.set_footer(text='powered by iamscienceman')
    else:
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
        embed.add_field(name="Top Role", value=member.top_role.name, inline=True)
        embed.add_field(name="Bot", value=False, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Activity", value=member.activity.name if member.activity else "None", inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.set_footer(text='powered by iamscienceman')
    
    await ctx.send(embed=embed)

# Serverinfo command
@bot.hybrid_command(name='serverinfo', description='Displays information about the server.')
async def serverinfo(ctx):
    server = ctx.guild
    embed = discord.Embed(title="Server Information", color=discord.Color.blue())

    embed.add_field(name="Server Name", value=server.name, inline=True)
    embed.add_field(name="Server ID", value=server.id, inline=True)
    embed.add_field(name="Owner", value=server.owner, inline=True)
    embed.add_field(name="Members", value=server.member_count, inline=True)
    embed.add_field(name="Roles", value=len(server.roles), inline=True)
    embed.add_field(name="Text Channels", value=len(server.text_channels), inline=True)
    embed.add_field(name="Voice Channels", value=len(server.voice_channels), inline=True)
    embed.add_field(name="Creation Date", value=server.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=server.icon.url)
    embed.set_footer(text='powered by iamscienceman')

    await ctx.send(embed=embed)

# Avatar command
@bot.hybrid_command(name='avatar', description="Displays the avatar of user.")
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    embed = discord.Embed(title="User Avatar", color=discord.Color.blue())
    embed.set_footer(text='powered by iamscienceman')
    
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Bot", value=member.bot, inline=True)
    else:
        embed.add_field(name="Error",value="Default avatar", inline=False)
    
    await ctx.send(embed=embed)

# 8ball command
@bot.hybrid_command(name='8ball', description='Gives you a random answer.')
async def random_answer(ctx, question):
    response = random.choice(ball_answers)
    await ctx.send(response)

# Roll command
@bot.hybrid_command(name='roll',description="Roll a dice with a specified number of sides.")
async def roll(ctx, sides: int):
        if sides <= 1:
            await ctx.send("Number of sides must be greater than 1.")
            return
        if type(sides) is float:
            await ctx.send("Number is a float! Unable to proceed!")
            return

        result = random.randint(1, sides)
        await ctx.send(f"Rolled a {sides}-sided dice and got: {result}")

# Flip command
@bot.hybrid_command(name='flip',description='Flips a coin.')
async def flip(ctx):
    sides = [
        "Heads",
        "Tails"
    ]
    response = random.choice(sides)
    await ctx.send(response)

# Uptime command
@bot.hybrid_command(name='uptime',description="Displays the time bot has been online for.")
async def uptime(ctx):
    delta = datetime.datetime.utcnow() - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"Uptime: {days}d {hours}:{minutes}:{seconds}")

########## ADMIN COMMANDS SECTION ##########

# Kick command
@bot.hybrid_command(name='kick',description="Kicks a member from server.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked.')

# Ban command
@bot.hybrid_command(name='ban',description="Bans a member from server.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')

# Mute command
@bot.hybrid_command(name='mute',description="Mutes a member from server.")
@commands.has_permissions(manage_roles=True)
async def tempmute(ctx, member: discord.Member, duration: int, *, reason="No reason"):
    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name="Muted")

    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'{member.mention} has been muted for {duration} seconds.')

    for channel in guild.channels:
        await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await asyncio.sleep(duration)
    await member.remove_roles(muted_role)

# Unmute command
@bot.hybrid_command(name='unmute',description='Unmutes a member from server.')
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted_role)
    await ctx.send(f'{member.mention} has been unmuted.')

# Clear command
@bot.hybrid_command(name='clear',description="Bulk delte messages.")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=1000)
    await ctx.send(f'{amount} messages cleared.', delete_after=5)

# Lockdown command
@bot.hybrid_command(name='lockdown',description="Locks down the channel with an optional to send message.")
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx, message: str=""):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False

    embed = discord.Embed(title="CHANNEL LOCKDOWN",description="An admin requested channel lockdown.", color=discord.Color.red())

    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed.add_field(name="Reason", value=message,inline=False)
    embed.set_footer(text='powered by iamscienceman')
    await ctx.send(embed=embed)

# Unlockdown command
@bot.hybrid_command(name='unlockdown',description="Unlocks the channel.")
@commands.has_permissions(manage_channels=True)
async def unlockdown(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel unlocked.')

# RUN THE BOT
bot.start_time = datetime.datetime.utcnow()
bot.run(os.getenv("DISCORD_TOKEN"))