import discord, requests, server, datetime, os
from discord.ext import commands, tasks
from discord import app_commands

instances = dict()
tzinfo = datetime.timezone(datetime.timedelta(hours=2))
times = [
    datetime.time(hour=10, tzinfo=tzinfo),
    datetime.time(hour=12, tzinfo=tzinfo),
    datetime.time(hour=14, tzinfo=tzinfo),
    datetime.time(hour=16, tzinfo=tzinfo),
    datetime.time(hour=18, tzinfo=tzinfo),
    datetime.time(hour=20, tzinfo=tzinfo)
]

delete_times = [
    datetime.time(hour=1, tzinfo=tzinfo),
]

token = open('token.txt', 'r').readline()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    #adding old servers
    if os.path.exists("./servers.txt"):
        with open("./servers.txt", 'r') as file:
            for line in file.readlines():
                line = line.split("#")
                instances[line[0]] = server.server(line[0], bot.get_channel(int(line[1])), line[2])
    else:
        open("./servers.txt", 'w')
        
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity("listening to ITT Blaise Pascal"))
    synced = await bot.tree.sync()
                
    update.start()
    print(f"{len(synced)} commands loaded.")
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name='ping', description='replies with pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"pong! requested by {interaction.user.mention}")

@bot.tree.command(name='register', description='registers the server to get updates!')
async def register(interaction: discord.Interaction, class_year_and_section: str):
    print(f'LOGGER: registered a new server with guild_id: {interaction.guild_id} and class: {class_year_and_section}') # Logging the registration

    if instances.get(interaction.guild_id) is None:
        instances[interaction.guild_id] = server.server(guild_id=interaction.guild_id, channel=interaction.channel, class_identifier=class_year_and_section)
        open("./servers.txt", 'a').write(f'{interaction.guild_id}#{interaction.channel.id}#{class_year_and_section}')
        await interaction.response.send_message("Server added to update list!", ephemeral=True)
    else:
        await interaction.response.send_message("The server is already registered, there is no need to register it again.", ephemeral=True)

@tasks.loop(time=times)
async def update():
    for guild in instances.values():
        await guild.update()
        
    server.server.delete_pdf()

@tasks.loop(time=delete_times)
async def remove():
    for guild in instances.values():
        guild.delete_json()

bot.run(token)