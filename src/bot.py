import os
import random
import asyncio
import discord
import chatterbot

from dotenv import load_dotenv
from discord.ext import commands
from chatterbot.trainers import ListTrainer

load_dotenv()
client = commands.Bot(command_prefix=commands.when_mentioned, help_command=None)

# try:
#     os.remove('db.sqlite3')
# except FileNotFoundError:
#     pass

chatbot = chatterbot.ChatBot('ChatKI', read_only=True)
trainer = ListTrainer(chatbot)
trainer.train(open('ai.txt').readlines())

@client.event
async def on_ready():
    print('\n\nONLINE as', client.user)

async def one_minute_loop():
    await client.wait_until_ready()

    while not client.is_closed():
        if not random.randint(0, 10):
            await client.change_presence(activity=discord.Game('Minecraft'))
        
        if not random.randint(0, 5):
            await client.change_presence(status=discord.Status.online)
        
        if not random.randint(0, 5):
            await client.change_presence(status=discord.Status.dnd)
        
        if not random.randint(0, 5):
            await client.change_presence(status=discord.Status.idle)

        if not random.randint(0, 20):
            await client.change_presence(activity=discord.Game('Osu!'))

        if not random.randint(0, 5):
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='YouTube'))
            
        if not random.randint(0, 30):
            await client.change_presence(activity=discord.Game('Lunar Client'))
        
        await asyncio.sleep(60)

client.loop.create_task(one_minute_loop())

@client.event
async def on_message(message):
    if (not isinstance(message.channel, discord.DMChannel)) or message.author == client.user:
        return 

    # variable replacer dictionary
    replacer = {
        '%game%': client.activity.name if client.activity else 'nichts',
    }

    # correct text without spelling mistakes
    response = str(chatbot.get_response(message.content.lower()))

    for key in replacer.keys():
        response = response.replace(key, replacer[key]) 
    
    # text with spelling mistakes
    response2 = ''

    # to avoid formatting problems
    colons = 0 # colons in the text
    percent = 0 # percent signs

    for c in response:
        if c == ':':
            colons += 1
        if c == '%':
            percent += 1

        if (c != '^') and (colons/2 == colons//2) and (percent/2 == percent//2) and (not 'http' in response):
            if not random.randint(0, 30):
                response2 += random.choice('ioeuoyöuxyaem10eüa194ze')
            elif not random.randint(0, 2):
                response2 += c.lower()
            else:
                response2 += c
        else:
            response2 += c
    
    sent = [] # list of messages that were sent
    
    await asyncio.sleep(1)

    if '^' in response:
        for msg in response2.split('^'):
            await asyncio.sleep(0.4)

            async with message.channel.typing():
                if not msg.startswith('http'):
                    await asyncio.sleep(len(msg)*0.1)

                if message.content.endswith('?'):
                    sent.append(await message.reply(msg))
                else:
                    sent.append(await message.channel.send(msg))
            
    else:
        async with message.channel.typing():
            await asyncio.sleep(len(response2)*0.1)

            if message.content.endswith('?'):
                sent.append(await message.reply(response2))
            else:
                sent.append(await message.channel.send(response2))
    
    # repair & edit spelling mistake(s) in the text
    if response != response2:
        # message(s) actually have/has mistakes
        count = 0

        for msg in sent:
            if random.randint(0, 4):
                await asyncio.sleep(2, 5)
                await msg.edit(content=response.split('^')[count])
            
            count += 1

client.run(os.getenv('TOKEN'))
