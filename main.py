import discord
import os
import asyncio
import random
from dotenv import load_dotenv

load_dotenv()

class Client(discord.Client):
        
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        self.drink_water_message = ['多喝热水', '喝了吗', '大郎该喝水了']
        self.drink_water_filename = ['hs1.jpg', 'hs2.jpg', 'hs3.png']
        self.bg_task = asyncio.create_task(self.cron_1_hour())
        self.bg_task = asyncio.create_task(self.cron_1_day())
    
    async def on_message(self, message):
        # prevent bot reply to itself
        if message.author == self.user:
            return
        if '我吃一点' in message.content:
            with open('./assets/cyd.WEBP', 'rb') as f:
                image = discord.File(f, filename='cyd.WEBP')
            await message.channel.send(file=image)
            return
        if '猫夹菜' in message.content:
            files = [f for f in os.listdir('./assets/cai') if os.path.isfile(os.path.join('./assets/cai', f))]
            if not files:
                print(f"Error: No files found in directory assets/cai.")
                return
            file_name = random.choice(files)
            with open(f'./assets/cai/{file_name}', 'rb') as f:
                image = discord.File(f, filename=file_name)
            await message.channel.send(file=image)
            return
    
    # async def on_message_edit(self, before, after):
    #     await after.channel.send(f'Old Message {after.content}')

    async def cron_1_hour(self):
        await self.wait_until_ready()
        while not self.is_closed():
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.name.lower() in ['主聊天室', 'general', 'bot', 'chat'] and channel.permissions_for(guild.me).send_messages:
                        print('=> start sending 1 hour cron message')
                        random_file_name = './assets/' + random.choice(self.drink_water_filename)
                        message = random.choice(self.drink_water_message)
                        with open(random_file_name, 'rb') as f:
                            image = discord.File(f, filename=random_file_name)
                        await channel.send(message, file=image)
                        break
            await asyncio.sleep(3600)


    async def cron_1_day(self):
        await self.wait_until_ready()
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

client = Client(intents=intents)
BOT_TOKEN = os.getenv('BOT_TOKEN')
client.run(BOT_TOKEN)