import discord
from discord.ext import commands

from asyncio import TimeoutError

import aiosqlite as asql

from pathlib import Path
from os import getenv
from dotenv import load_dotenv

# Token stuff
load_dotenv()
token = getenv('TOKEN')

# Database stuff
filepath = Path(__file__).parent.absolute()
dbname = "Bot.sql"

# Detection stuff
# The command which you use to bump your server
command = "!d bump"

# Roles
# We use key-pair values - key is the threshold and value is the role ID
# Should order them from the smallest threshold to the largest
# No two keys or values should be the same
roles = [
    [1, 830872472739381248],
    [2, 830872506272710677],
    [5, 830872533837414511]
]

# Define discord bot
bot = commands.Bot(command_prefix="t!")

# Fires off when the bot is internally ready to receive events
@bot.event
async def on_ready():
    # We create our database
    async with asql.connect(filepath/dbname) as db:
        # Create table
        await db.execute("CREATE TABLE IF NOT EXISTS users (key INTEGER PRIMARY KEY, id INTEGER, points INTEGER)")
        # Save changes
        await db.commit()
    print("Bot is ready!")

# Event which triggers whenever someone sends a message
@bot.event
async def on_message(message):
    if (len(message.embeds) > 0):
        print(message.embeds[0].color, type(message.embeds[0].color))
        print(message.embeds[0].title, type(message.embeds[0].title))
        print(message.embeds[0].description, type(message.embeds[0].description))
    # We check if the message is the command
    if (message.content == command):
        # We check if it's the bot who sent the message
        # if it's the right channel
        # if the users id is mentioned in the message
        # We use this check in our wait_for()
        def check(m):
            return m.author.id == 302050872383242240 and m.channel == message.channel and str(message.author.id) in m.embeds[0].description

        try:
            # We wait for response, if bot doesn't reply we get timeout
            msg = await bot.wait_for('message', check=check, timeout=60)

            # Accept
            if (str(msg.embeds[0].colour) == "#24b7b7"):
            # if (True):
                print("Accepted")
                async with asql.connect(filepath/dbname) as db:
                    # Get user points
                    cursor = await db.execute('SELECT points FROM users WHERE id=?', (message.author.id, ))
                    points = await cursor.fetchone()
                    # Add point to user
                    # Register user if we've not seen him yet
                    if (points is None):
                        await db.execute('INSERT INTO users (id, points) VALUES(?,?)', (message.author.id, 1))
                        points = 1
                    # Update user data
                    else:
                        points = points[0] + 1
                        await db.execute('UPDATE users SET points=? WHERE id=?', (points, message.author.id))
                    # Save changes
                    await db.commit()

                print(f"Points: {points}")

                # Asign user new role if he got a new one

                # Get role for user
                counter = 0
                assigned = False
                assigned_role = None
                for role in roles:
                    if (points < role[0]):
                        assigned = True
                        if (counter > 0):
                            print(f"Assign {roles[counter - 1]}")
                            assigned_role = roles[counter - 1]
                        break
                    counter += 1
                if (assigned == False):
                    print(f"Assign {roles[-1]}")
                    assigned_role = roles[-1]

                if (assigned_role is None):
                    return

                if (assigned_role[1] in [role.id for role in message.author.roles]):
                    return
                else:
                    user_roles = [role.id for role in message.author.roles]
                    guild_roles = await message.author.guild.fetch_roles()
                    bot_roles = [role[1] for role in roles]
                    for role in bot_roles:
                        if (role in user_roles):
                            for guild_role in guild_roles:
                                if (guild_role.id == role):
                                    await message.author.remove_roles(guild_role)
                    for guild_role in guild_roles:
                        if (guild_role.id == assigned_role[1]):
                            await message.author.add_roles(guild_role)
                    return
            elif (str(msg.embeds[0].colour) == "#eb4c61"):
                print("Rejected")
                return
            else:
                print("Reject because of unknown message")
                return
        except TimeoutError:
            print("Dishboard didn't reply in time...")
            return
    else:
        await bot.process_commands(message)

@bot.command()
@commands.guild_only()
async def check(ctx, member: discord.Member):
    async with asql.connect(filepath/dbname) as db:
        # Get user points
        cursor = await db.execute('SELECT points FROM users WHERE id=?', (member.id, ))
        points = await cursor.fetchone()
        if (points is None):
            points = 0
        else:
            points = points[0]
    await ctx.send(f"Member {member.mention} has {points} points!")

@bot.command()
@commands.guild_only()
@commands.has_guild_permissions(administrator=True)
async def reset(ctx, member: discord.Member):
    async with asql.connect(filepath/dbname) as db:
        # Get user points
        await db.execute('UPDATE users SET points=? WHERE id=?', (0, member.id))
        await db.commit()
    await ctx.send(f"Reset points for member {member.mention}.")

# Starts the bot
# Anything after this point won't get executed
bot.run(token)