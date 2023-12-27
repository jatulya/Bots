import discord
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():  #called when the bot is ready to be used
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):
  #triggers each time a msg is received
  if msg.author == client.user:  #if the msg is from the bot itself, ignore
    return

  if msg.content.startswith('$hello'):  #if the msg starts with $hello -> a cmd to bot
    await msg.channel.send('Hello!')  #send Hello! to the channel

#running the bot
client.run(os.getenv('BOT1_TOKEN'))