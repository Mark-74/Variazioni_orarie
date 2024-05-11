import discord, requests, server, datetime
from discord.ext import commands, tasks
from discord import app_commands

instances = dict()
tzinfo = datetime.timezone(datetime.timedelta(hours=2))
times = [
    datetime.time(hour=19, minute=2, tzinfo=tzinfo)
]

token = open('token.txt', 'r').readline()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("BlackJack"))
    synced = await bot.tree.sync()
    update.start()
    print(f"{len(synced)} commands loaded.")
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name='ping', description='replies with pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"pong! requested by {interaction.user.mention}")

@bot.tree.command(name='register', description='registers the server to get updates!')
async def register(interaction: discord.Interaction, class_year_and_section: str):
    
    
    if instances.get(interaction.guild_id) is None:
        instances[interaction.guild_id] = server.server(guild=interaction.guild, channel=interaction.channel, class_identifier=class_year_and_section)
        await interaction.response.send_message("Server added to update list!", ephemeral=True)
    else:
        await interaction.response.send_message("The server is already registered, there is no need to register it again.", ephemeral=True)

@tasks.loop(time=times)
async def update():
    for guild in instances.values():
        await guild.update()
        
bot.run(token)