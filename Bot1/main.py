import discord
import os
import requests
import json
import random
from replit import db

intents = discord.Intents.default()
client = discord.Client(intents=intents)

#list of sad words bot will be checking
sad_words = ['depressed', 'miserbale', 'sad', 'unhappy', 'angry', 'depressing', 'depression', 'gloomy', 'disheartened', 'discouraged']

#bot will be starting with these, user could add more to the list
start_enc = ['Cheer up!', 'Hang in there!', 'You are a great person!']

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

def update_enc(enc_msg):
  #checking if thte database has the key 'encouragements'
  if "encouragement" in db.keys():
    #storing the values of the key in enc
    enc = db["encouragement"]
    #updating the list with the new message
    enc.append(enc_msg)
    #storing the updated list back in the db
    db["encouragement"] = enc
  else:
    #if the key does not exist, create it and store the new msg in a list 
    db["encouragement"] = [enc_msg]
    
def del_enc(index):
  enc = db["encouragement"]
  if len(enc) > index:
    del enc[index]
    db["encouragement"] = enc
  
@client.event
async def on_message(msg):
  #triggers each time a msg is received
  if msg.author == client.user:  #if the msg is from the bot itself, ignore
    return

  msgCont = msg.content

  if msgCont.startswith('$hello'):  #if the msg starts with $hello -> a cmd to bot
    await msg.channel.send('Hello!')  #send Hello! to the channel

  if msgCont.startswith('$inspire'):
    quote = get_quote()
    await msg.channel.send(quote)

  #when the bot chooses the enc quote to display, we also need choice of quotes to be from the user submitted quotes
  options = start_enc
  if "encouragement" in db.keys():
    for quotes in db["encouragement"]:
      options.append(quotes)
  
  #checking if any sad words are in the msg
  if any(word in msgCont for word in sad_words):
    await msg.channel.send(random.choice(options))

  #the command to add a new encouraging message
  if msgCont.startswith('$new'):
    #the 1 in the arg performs one split => [0]th ele is everything before $new and [1]th ele is everything after $new
    encMsg = msgCont.split("$new ", 1)[1]
    update_enc(encMsg)
    await msg.channel.send("New encouraging message added.")

  #the command to delete an encouraging message
  if msgCont.startswith('$delete'):
    enc = []
    if "encouragement" in db.keys():
      #because we are converting the number into integer, the space would be gone, therefore no "$delete "
      index = int(msgCont.split("$delete ", 1)[1])
      try:
        enc = db["encouragement"][index]
        await msg.channel.send("The quote '" + enc + "' has been deleted." )
        del_enc(index)
        enc = db["encouragement"]
      except IndexError as e:
        await msg.channel.send(e)
    else:
      await msg.channel.send("No encouraging messages to delete.")

#running the bot
client.run(os.getenv('BOT1_TOKEN'))