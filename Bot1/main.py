import discord
import os
import requests
import json

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():  #called when the bot is ready to be used
  print('We have logged in as {0.user}'.format(client))

#get quotes from zenquotes.io
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  #the url is taken from the documentation of zenquotes.io
  json_data = json.loads(response.text) #where did .text come from
  #a json object contains a datalist with dictionaries with 'q': quote & 'a': author
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_message(msg):
  #triggers each time a msg is received
  if msg.author == client.user:  #if the msg is from the bot itself, ignore
    return

  if msg.content.startswith('$hello'):  #if the msg starts with $hello -> a cmd to bot
    await msg.channel.send('Hello!')  #send Hello! to the channel

  if msg.content.startswith('$inspire'):
    quote = get_quote()
    await msg.channel.send(quote)

#running the bot
client.run(os.getenv('BOT1_TOKEN'))

