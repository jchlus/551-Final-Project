#551 Final Project - Physical Helath Monitor via Discord
#Jaosn Chlus

import os
import discord
from discord.ext import commands
from datetime import datetime, date, timedelta
import time
import asyncio
import json

TOKEN='Nzg5OTA2MTUxMzY5MjExOTA0.X943bg.s5JTW2owVe3rmou8DiGB3WPt4_g'
GUILD = '789656056074207232'
 
client = commands.Bot(command_prefix='bit')

@client.event
async def on_ready():
    #loop gives it the ability to connect to multiple guilds
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
    #send a message to general challenge on powerup
    for channel in guild.channels:
        if channel.id == 789656056074207235:
            break
    await channel.send("Hello, Welcome back!")
    
    #checking events that happen today to send reminder
    f = open('data.json',)
    data = json.load(f) 
    today = datetime.today().strftime('%d-%m-%y')
    events = []
    
    for element in data:  
        if element["date"] == today:
            events.append(element["message"])

    if events == []:
        await channel.send("You have no events today") 
    else:
        await channel.send("You have the following events today:")
        for line in events:
            await channel.send(line)
    
    #3 hour loop for automated messages
    x = 1
    while x == 1:
        #reading reminders file, if a reminder is turned off it will not be updated until 3 hour rotation is over
        r = open('reminders.json',)
        reminders = json.load(r) 

        #0.5 hour
        await asyncio.sleep(1800)
        if reminders["sit"] == "True":
            await channel.send("Sit up straight")
        await eventManager(channel)

        #1 hour
        await asyncio.sleep(1800)
        if reminders["sit"] == "True":
            await channel.send("Sit up straight")
        if reminders["stand"] == "True":
            await channel.send("Stand Up")
        await eventManager(channel)

        #1.5 hour
        await asyncio.sleep(1800)
        if reminders["sit"] == "True":
            await channel.send("Sit up straight")
        await eventManager(channel)

        #2 hour
        await asyncio.sleep(1800)
        if reminders["sit"] == "True":
            await channel.send("Sit up straight")
        if reminders["stand"] == "True":
            await channel.send("Stand Up, maybe take a walk")
        if reminders["water"] == "True":
            await channel.send("Drink water")
        await eventManager(channel)

        #2.5 hour
        await asyncio.sleep(1800)
        if reminders["sit"] == "True":
            await channel.send("Sit up straight")
        await eventManager(channel)

        #3 hour
        await asyncio.sleep(1800)
        if reminders["sit"] == "True":
            await channel.send("Sit up straight")
        if reminders["stand"] == "True":
            await channel.send("Stand Up")
        if reminders["eyes"] == "True":
            await channel.send("Time to rest your eyes, maybe exercise!")
        await eventManager(channel)


#sends a direct message to new members and a message in the general chat welcoming the new member
@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"""Welcome to the server {member.mention}""")
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server! Say bit help to see my commands'
    )

#runs everytime a message is sent to the group
@client.event
async def on_message(message):
    #makes sure the bot does not talk to itself
    if message.author == client.user:
        return
    
    #messages to the bot must contain "bit"
    if "bit" in message.content:
        if message.content.find("hello") != -1:
            await message.channel.send(f"""Hi {message.author}""")
        if message.content.find("help") != -1:
            await message.channel.send("hello: Hi message\ncalendar: shows your events\ncreate: adds a new event to calendar\ndelete: deletes an event ex:\"bit delete: message of event\"")
            await message.channel.send("reminders: shows which auto messages are turned on\nauto: turn automatic messages on/off ex:\"bit auto sit\"")
        def check1(m):
            if (m.content.find('EVENT:') != -1 and m.channel == message.channel):
                date = m.content
                return date

        if message.content.find("create") != -1:
            await message.channel.send("Create a Task \nPlease implement the data in the following format: \nEVENT: DD-MM-YY, HH:MM, your message")
            event = await client.wait_for('message', check=check1)
            details = event.content.split(",")
            date = details[0].split(":")[1].strip()
            time = details[1].strip()
            msg = details[2].strip()
            today = datetime.today()
            today = today.replace(hour=0, minute=0, second=0, microsecond=0)
            
            try:
                date = datetime.strptime(date, '%d-%m-%y')
            except:
                await message.channel.send("Not a valid date")

            if date < today:
                await message.channel.send("Not a valid date")

            else:
                await message.channel.send(f"""saving event: {event.content}""") 
                with open('data.json') as json_file: 
                    data = json.load(json_file) 
                    y = {"date": date.strftime('%d-%m-%y'),
                        "time": time,
                        "message": msg
                        } 
                    # appending event to json file 
                    data.append(y) 
                write_json(data)  

        if message.content.find("calendar") != -1:
            f = open('data.json',)
            cal = json.load(f) 
            for i in cal:
                await message.channel.send(i)
            f.close()
        
        if message.content.find("delete") != -1:
            m = message.content.split(":")
            event = m[1].strip()
            new = []
            with open('data.json') as f:
                data = json.load(f)
                for element in data:
                    if element["message"] == event:
                        await message.channel.send("event deleted")
                    else: new.append(element)
                write_json(new)
                f.close()

        if message.content.find("auto") != -1:
            msg = message.content.split(" ")[2]
            r = open('reminders.json', "r")
            reminders = json.load(r)
            if reminders[msg] == "True":
                reminders[msg] = "False"
                updated = open("reminders.json", "w")
                json.dump(reminders, updated)
                updated.close()
                await message.channel.send(f"""{msg} has been removed from your automatic reminders""")
            elif reminders[msg] == "False":
                reminders[msg] = "True"
                updated = open("reminders.json", "w")
                json.dump(reminders, updated)
                updated.close()
                await message.channel.send(f"""{msg} has been added to your automatic reminders""")
        
        if message.content.find("reminders") != -1:
            r = open('reminders.json', "r")
            reminders = json.load(r)
            await message.channel.send("your automatic reminders include:")
            for line in reminders:
                if reminders[line] == "True":
                    await message.channel.send(f"""{line}""")
        
#checks what events in the calendar are happening in the next 30 minutes
async def eventManager(channel):
    f = open('data.json',)
    data = json.load(f) 
    today = datetime.today().strftime('%d-%m-%y')
    now = datetime.now()
    for element in data:
        if element["date"] == today:
            eventTime = element["time"]
            compareTime = datetime.strptime(eventTime, "%H:%M")
            compareTime = now.replace(minute=compareTime.time().minute)
            instance = compareTime - now
            if (instance < timedelta(minutes=30) and instance > timedelta(minutes=0)):
                await channel.send(f"""This event is coming up: {element["message"]} at {element["time"]}""")

def write_json(data, filename='data.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

client.run(TOKEN)