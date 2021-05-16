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
client = commands.Bot(command_prefix='/')

db = firestore.client()
def sendChar(guilda, username):
    docPer = db.collection('Servers').document(guilda).collection('Players').document(username).get()
    if docPer.exists:
        userDoc = docPer.to_dict()
        emb = discord.Embed(title=userDoc['nome'])
        for key, value in userDoc.items():
            if key != 'status':
                emb.add_field(name=f'**{key}**', value=value)
        if len(userDoc['status']) > 1:
            stringStat = ''      
            for key, value in userDoc['status'].items():
                to_add = '> **{}**: {}\n'.format(key, str(value))
                stringStat += to_add
        else:
            stringStat = 'Nenhum status definido ainda'
        emb.add_field(name='Status',value=stringStat, inline=False)
        return emb
        
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
    db.collection('Servers').document(context.guild.name).set(world)

@client.command(name = 'setcharacter')
async def setcharacter(context):
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    if charDoc.exists:
        await context.message.channel.send('Você já criou seu personagem!')
    else:
        if context.message.content.find('nome=') != -1 and context.message.content.find('prof=') != -1 and context.message.content.find('idade=') != -1 and context.message.content.find('sexo=') != -1 and context.message.content.find('nacionalidade=')!= -1 and context.message.content.find('moradia=') != -1 and context.message.content.find('aparencia=') != -1:
            nm = context.message.content[context.message.content.find('nome=')+5:context.message.content.find(' *',context.message.content.find('nome='))]
            profissao = context.message.content[context.message.content.find('prof=')+5:context.message.content.find(' *',context.message.content.find('prof='))]
            idade = context.message.content[context.message.content.find('idade=')+6:context.message.content.find(' *',context.message.content.find('idade='))]
            sexo = context.message.content[context.message.content.find('sexo=')+5:context.message.content.find(' *',context.message.content.find('sexo='))]
            nacionalidade = context.message.content[context.message.content.find('nacionalidade=')+14:context.message.content.find(' *',context.message.content.find('nacionalidade='))]
            moradia = context.message.content[context.message.content.find('moradia=')+8:context.message.content.find(' *',context.message.content.find('moradia='))]
            aparencia = context.message.content[context.message.content.find('aparencia=')+10:context.message.content.find(' *',context.message.content.find('aparencia='))]
        
            charSave = {'nome':nm,'player':context.message.author.name,'profissão':profissao,'idade':idade,'sexo':sexo,'nacionalidade':nacionalidade,'moradia':moradia,'aparência':aparencia,'status':{}}
            db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).set(charSave)
            await context.message.channel.send('Personagem criado com sucesso!')
            await context.message.channel.send(embed=sendChar(context.guild.name, context.message.author.name))
        else:
            await context.message.channel.send('O comando foi digitado de maneira errada, por favor verifique nas regras o formato correto.')

@client.command(name='character')
async def character(context):
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    if charDoc.exists:
       await context.message.author.send(embed=sendChar(context.guild.name, context.message.author.name))
    else:
        await context.message.channel.send('Você ainda não criou um personagem!')

@client.command(name = 'setstatus')
async def setstatus(context):
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    if charDoc.exists:
        if context.message.content.find('INT=') != -1 and context.message.content.find('FOR=') != -1 and context.message.content.find('APA=') != -1 and context.message.content.find('CON=') != -1 and context.message.content.find('tamanho=')!= -1 and context.message.content.find('POD=') != -1 and context.message.content.find('DES=') != -1 and context.message.content.find('SOR=') != -1 and context.message.content.find('EDU=') != -1:
            inteligencia = int(context.message.content[context.message.content.find('INT=')+4:context.message.content.find(' *',context.message.content.find('INT='))])
            forca = int(context.message.content[context.message.content.find('FOR=')+4:context.message.content.find(' *',context.message.content.find('FOR='))])
            aparencia = int(context.message.content[context.message.content.find('APA=')+4:context.message.content.find(' *',context.message.content.find('APA='))])
            constituicao = int(context.message.content[context.message.content.find('CON=')+4:context.message.content.find(' *',context.message.content.find('CON='))])
            tamanho = int(context.message.content[context.message.content.find('tamanho=')+8:context.message.content.find(' *',context.message.content.find('tamanho='))])
            poder = int(context.message.content[context.message.content.find('POD=')+4:context.message.content.find(' *',context.message.content.find('POD='))])
            dextreza = int(context.message.content[context.message.content.find('DES=')+4:context.message.content.find(' *',context.message.content.find('DES='))])
            sorte = int(context.message.content[context.message.content.find('SOR=')+4:context.message.content.find(' *',context.message.content.find('SOR='))])
            educacao = int(context.message.content[context.message.content.find('EDU=')+4:context.message.content.find(' *',context.message.content.find('EDU='))])
            corpo = 0
            movimento = 7
            if (tamanho + forca) <= 12:
                corpo = -2
            elif (tamanho + forca) >= 13 and (tamanho + forca) <= 16:
                corpo = -1
            elif (tamanho + forca) >= 25 and (tamanho + forca) <= 32:
                corpo = 1
            elif (tamanho + forca) >= 33 and (tamanho + forca) <=40:
                corpo = 2
            if forca > tamanho and dextreza > tamanho:
                movimento = 9
            elif forca >= tamanho or dextreza >= tamanho:
                movimento = 8
            uDoc = charDoc.to_dict()
            if uDoc['idade'] >= 40 and uDoc['idade'] < 50:
                movimento -= 1
            elif uDoc['idade'] >= 50 and uDoc['idade'] < 60:
                movimento -= 2
            elif uDoc['idade'] >= 60 and uDoc['idade'] < 70:
                movimento -= 3
            elif uDoc['idade'] >= 70 and uDoc['idade'] < 80:
                movimento -= 4
            elif uDoc['idade'] >= 80:
                movimento -= 5
            statSave = {'inteligência': inteligencia, 'força': forca, 'aparência': aparencia, 'constituição': constituicao, 'tamanho': tamanho, 'poder': poder, 'dextreza': dextreza, 'sorte': sorte, 'educação': educacao, 'corpo': corpo, 'movimento': movimento}
            db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).update({'status': statSave})
            await context.message.channel.send('Status salvos com sucesso!')
    else:
        await context.message.channel.send('Você ainda não criou um personagem!')

@client.command(name = 'upstat')
async def upstat(context):
    stat = context.message.content[7:context.message.content.find(' *')]
    number = int(context.message.content[context.message.content.find(' *')+3:])
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    
@client.event
async def on_ready():
    print('Informações básicas:')
    print('Nome do bot: {0}'.format(client.user.name))
    print('Id: {0}'.format(client.user.id))
    print('Server: {0}'.format(client.guilds))
    print('-------------------------------------------------------------------------------')

    await client.change_presence(status=discord.Status.online, activity=discord.Game("Steins Gate"))

client.run(token)