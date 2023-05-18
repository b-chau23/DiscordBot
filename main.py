from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from random import randint
import time


load_dotenv('.env')

TOKEN: str = os.getenv('TOKEN')
GUILD: str = os.getenv('GUILD')


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(f'{bot.user.name} has connected to Discord!\n'  # print connection message
          f'{guild.name}(id: {guild.id})'
          )

    members = '\n - '.join([member.name for member in guild.members])  # print all members in server
    print(f'Guild Members:\n - {members}')


# Have the bot REE
@bot.command(name='reee', help="-Bot replies with REEEEE")
async def on_message(message):
    if message.author == bot.user.name:  # disables infinite bot loop
        return
    text = "REEEEEEEEEEE"

    await message.channel.send(text)


# Have the bot REE at someone
@bot.command(name='ree', help="-Mention a member to REEE at them")
async def mention_ping(ctx, member: discord.Member):  # REEEEEEEEEEEEEEEEEEEEEEE
    await ctx.send(f"REEEEEEEEEEE {member.mention}")


@bot.event
async def on_command_error(ctx, error):  # Fails Role Check
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

    elif isinstance(error, commands.errors.CommandOnCooldown):  # Lmao get fucked dumbass / sends over-use message
        slugma = randint(1, 10)
        if slugma == 1:
            await ctx.send("slugma balls bitch", file=discord.File('slugma.jpg'))
        else:
            await ctx.send('Command is on Cooldown.')


# sends user to specified channel (in this case "hell")
@bot.command(name="banish")
@commands.cooldown(1, 60.0)  # prevent over-usage
async def on_message(ctx, member: discord.Member):
    channel = bot.get_channel(843852696254808094)  # <-- hell
    await member.move_to(channel)
    await ctx.send(f"User {member} has been sent to hell")


# sends 2 users to hell (Specifically Amir and Tenzin){might make it more interesting later}
@bot.command(name="banish2")
@commands.cooldown(1, 60.0)
async def on_message(ctx, member: discord.Member, member2: discord.Member):
    channel = bot.get_channel(843852696254808094)  # <-- hell
    await member.move_to(channel)
    await member2.move_to(channel)
    await ctx.send(f"User {member} and {member2} has been sent to hell")


# Mute a user just cause ya can
@bot.command(name="mute")
@commands.cooldown(1, 60.0)
async def on_message(ctx, member: discord.Member):
    await member.edit(mute=True)


# Unmute member
@bot.command(name="unmute")
async def on_message(ctx, member: discord.Member):
    await member.edit(mute=False)


# Delete every message a user sends (Deletion Portion)
# Default silence time is 10 seconds
async def murder(member, sil_time=10):
    start = time.time()

    @bot.event
    async def on_message(ctx):
        end = time.time()
        if end > (start + float(sil_time)):
            pass
        elif ctx.author.id == member:
            await ctx.delete()


# Delete every message a user sends (Telling bot which user to delete messages)
@bot.command(name="silence")
async def on_message(ctx, member: discord.Member, gib_time):
    # .Member does not work on .author

    if member.id != 839691704000446464:
        if float(gib_time) <= 600.0:
            silenced_time = gib_time
            silenced_member = member.id
            await ctx.send(f'{ctx.member} has been silenced for {gib_time} seconds!')
            await murder(silenced_member, silenced_time)
        elif float(gib_time) > 600.0:
            silenced_time = gib_time
            silenced_member = ctx.author.id
            await ctx.send(f'you fucked up {ctx.author.name}')
            await ctx.send(f'{ctx.author.name} has been silenced for {gib_time} seconds!')
            await murder(silenced_member, silenced_time)
    else:
        silenced_time = gib_time
        silenced_member = ctx.author.id
        await ctx.send(f'YOU CANT SILENCE GOD, PEASANT')
        await ctx.send(f'{ctx.author} has been silenced!')
        await murder(silenced_member, silenced_time)


bot.run(TOKEN)
