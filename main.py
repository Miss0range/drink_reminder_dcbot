import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
import random
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
guild_id_str = os.getenv("GUILD_ID")
if guild_id_str is None:
    raise ValueError("GUILD_ID environment variable not set!")

GUILD_ID = int(guild_id_str)  # Convert string to int here

GUILD = discord.Object(id=GUILD_ID)

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

class Client(commands.Bot):
        
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        self.drink_water_message = ['多喝热水', '喝了吗', '大郎该喝水了']
        self.drink_water_filename = ['hs1.jpg', 'hs2.jpg', 'hs3.png']
        self.bg_task = asyncio.create_task(self.cron_6_hour())
        self.bg_task = asyncio.create_task(self.cron_1_day())
        try:
            synced = await self.tree.sync(guild=GUILD)
            print(f'Synced {len(synced)} commands to guild')
        except Exception as e:
            print(f'Error syncing slash command {e}')


    async def on_member_join(self, member):
        #get channel to send 
        for channel in member.guild.text_channels:
            if channel.name.lower() in [name.lower() for name in ['主聊天室', 'general', 'bot', 'chat']] \
            and channel.permissions_for(member.guild.me).send_messages:
                print(f"=> Sending welcome message in #{channel.name}")
                # Optionally include an image
                if channel.name == '主聊天室':
                    file_name = 'welcome.webp'
                    message = '你好鸭 美味的小孩'
                else:
                    file_name = 'welcome2.gif'
                    message= 'Welcome to the server,'
                try:
                    with open(f'./assets/{file_name}', 'rb') as f:
                        image = discord.File(f, filename=file_name)

                    await channel.send(
                        content=f"{message} {member.mention}! 🎉",
                        file=image
                    )
                except FileNotFoundError:
                    await channel.send(f"Welcome to the server, {member.mention}! 🎉")
                break  # Stop after sending to the first matching channel
    
    async def on_message(self, message):
        # prevent bot reply to itself
        if message.author == self.user:
            return
    
    # async def on_message_edit(self, before, after):
    #     await after.channel.send(f'Old Message {after.content}')

    async def cron_6_hour(self):
        await self.wait_until_ready()
        await asyncio.sleep(21600)
        while not self.is_closed():
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.name.lower() in ['主聊天室', 'general', 'bot', 'chat'] and channel.permissions_for(guild.me).send_messages:
                        print('=> start sending 6 hour cron message')
                        random_file_name = './assets/' + random.choice(self.drink_water_filename)
                        message = random.choice(self.drink_water_message)
                        with open(random_file_name, 'rb') as f:
                            image = discord.File(f, filename=random_file_name)
                        await channel.send(message, file=image)
                        break
            await asyncio.sleep(21600)


    async def cron_1_day(self):
        await self.wait_until_ready()
        await asyncio.sleep(86400)
        while not self.is_closed():
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.name.lower() in ['主聊天室', 'general', 'bot', 'chat'] and channel.permissions_for(guild.me).send_messages:
                        print('=> start sending 1 day cron message')
                        with open('./assets/tg.jpg', 'rb') as f:
                            image = discord.File(f, filename='tg.jpg')
                        await channel.send(file=image)
                        break
            await asyncio.sleep(86400)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(command_prefix="!", intents=intents)

@client.tree.command(name="wcyd", description="你好 我吃一点", guild=GUILD)
async def displayWCYD(interaction: discord.Interaction):
    with open('./assets/cyd.WEBP', 'rb') as f:
        image = discord.File(f, filename='cyd.WEBP')
    await interaction.response.send_message(file=image)

@client.tree.command(name="jc", description="随机夹菜", guild=GUILD)
async def displayWCYD(interaction: discord.Interaction):
    files = [f for f in os.listdir('./assets/cai') if os.path.isfile(os.path.join('./assets/cai', f))]
    if not files:
        print(f"Error: No files found in directory assets/cai.")
        return
    file_name = random.choice(files)
    with open(f'./assets/cai/{file_name}', 'rb') as f:
        image = discord.File(f, filename=file_name)
    await interaction.response.send_message(file=image)
    return
keep_alive()
client.run(BOT_TOKEN)