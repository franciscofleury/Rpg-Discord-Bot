# -- coding: utf-8 --
import discord
import asyncio
from discord.ext import commands
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

#intents = discord.Intents.all()
cred = credentials.Certificate('./rpgbot.json')
default_app = firebase_admin.initialize_app(cred)
client = commands.Bot(command_prefix='$')

db = firestore.client()

def worldBackup(server, game):
    db.collection('Servers').document(server).collection(game).document('mundo').set(world)

def read_token():
    with open("token.txt",'r') as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

@client.command(name = 'setgame')
async def setgame(context):
    nomeMundo = context.message.content[context.message.content.find('nome=')+5:]
    global world
    world = {'name':nomeMundo,'gm':context.message.author.name}
    worldBackup(context.guild.name,nomeMundo)
    db.collection('Servers').document(context.guild.name).set({'current':nomeMundo})


def get_world(server, game):
    doc = db.collection('Servers').document(server).collection(game).document('mundo').get()
    if doc.exists:
        global world
        world = doc.to_dict()

@client.event
async def on_ready():
    print('Informações básicas:')
    print('Nome do bot: {0}'.format(client.user.name))
    print('Id: {0}'.format(client.user.id))
    print('Server: {0}'.format(client.guilds))
    print('-------------------------------------------------------------------------------')

    await client.change_presence(status=discord.Status.online, activity=discord.Game(""))

client.run(token)