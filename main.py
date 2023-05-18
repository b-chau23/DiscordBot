import os
import time
import discord
from random import randint
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv('.env')

TOKEN: str = os.getenv('TOKEN')
GUILD: str = os.getenv('GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Messages terminal to confirm successful bot connection
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


# Error messages
@bot.event
async def on_command_error(ctx, error):
    # Role check failiure
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    # Command on cooldown error
    elif isinstance(error, commands.errors.CommandOnCooldown):
        # Create a random chance to send a 'unique' error message
        slugma = randint(1, 10)
        if slugma == 1:
            await ctx.send("slugma balls bitch", file=discord.File('slugma.jpg'))
        else:
            await ctx.send('Command is on Cooldown.')


# Removes targetted user from their current channel and moves them to a new one
@bot.command(name="banish")
@commands.cooldown(1, 60.0)  # prevent over-usage
async def on_message(ctx, member: discord.Member):
    channel: int = int(os.getenv('BANISH'))
    move_to = bot.get_channel(channel)
    await member.move_to(move_to)
    await ctx.send(f"User {member} has been sent to {bot.get_channel(move_to)}!")


# Mute a user from voice chat
@bot.command(name="mute")
@commands.cooldown(1, 60.0)
async def on_message(ctx, member: discord.Member):
    await member.edit(mute=True)


# Unmute a user from voice chat
@bot.command(name="unmute")
async def on_message(ctx, member: discord.Member):
    await member.edit(mute=False)

# Helper function for 'silence' command
# Delete every message a user sends 
# Default silence time is 10 seconds
async def delete_message(member, time_silenced=10):
    start = time.time()

    @bot.event
    async def on_message(ctx):
        end = time.time()
        if end > (start + float(time_silenced)):
            pass
        elif ctx.author.id == member:
            await ctx.delete()


# Receives member and time input,
# Identifies which user to delete messages from
@bot.command(name="silence")
async def on_message(ctx, member: discord.Member, given_time):
    # .Member does not work on .author

    # Ensure that the bot cannot silence itself by hardcoding its ID
    if member.id != 839691704000446464:
        # Silence time must be less than 5 minutes
        # If a time beyond 5 minutes is given, the user that called the command is silenced by that time instead
        if float(given_time) <= 300.0:
            silenced_time = given_time
            silenced_member = member.id
            await ctx.send(f'{ctx.member} has been silenced for {given_time} seconds!')
            await delete_message(silenced_member, silenced_time)
        elif float(given_time) > 300.0:
            silenced_time = given_time
            silenced_member = ctx.author.id
            await ctx.send(f'you messed up {ctx.author.name}')
            await ctx.send(f'{ctx.author.name} has been silenced for {given_time} seconds!')
            await delete_message(silenced_member, silenced_time)

    # Punish users by silencing the user that tried to silece the bot
    else:
        silenced_time = given_time
        silenced_member = ctx.author.id
        await ctx.send(f'YOU CANT SILENCE GOD, PEASANT')
        await ctx.send(f'{ctx.author} has been silenced!')
        await delete_message(silenced_member, silenced_time)


bot.run(TOKEN)
