# -- coding: utf-8 --
import discord
import random
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

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def sendChar(guilda, username):
    docPer = db.collection('Servers').document(guilda).collection('Players').document(username).get()
    if docPer.exists:
        userDoc = docPer.to_dict()
        emb = discord.Embed(title=userDoc['nome'])
        for key, value in userDoc.items():
            if key != 'status' and key != 'pericia' and key != 'attacks':
                emb.add_field(name=f'**{key}**', value=value)
        if len(userDoc['status']) > 1:
            stringStat = ''
            stringStatus = ''     
            for key, value in userDoc['status'].items():
                to_add = '> **{}**: {}\n'.format(key, str(value))
                stringStatus += to_add
        else:
            stringStatus = 'Nenhum status definido ainda'
        if len(userDoc['pericia']) > 1:
            stringStat = ''      
            for key, value in userDoc['pericia'].items():
                to_add = '> **{}**: {}\n'.format(key, str(value))
                stringStat += to_add
        else:
            stringStat = 'Nenhuma pericia definida ainda'

        emb.add_field(name='Status',value=stringStatus, inline=False)
        emb.add_field(name='Perícia',value=stringStat, inline=False)
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
            idade = int(context.message.content[context.message.content.find('idade=')+6:context.message.content.find(' *',context.message.content.find('idade='))])
            sexo = context.message.content[context.message.content.find('sexo=')+5:context.message.content.find(' *',context.message.content.find('sexo='))]
            nacionalidade = context.message.content[context.message.content.find('nacionalidade=')+14:context.message.content.find(' *',context.message.content.find('nacionalidade='))]
            moradia = context.message.content[context.message.content.find('moradia=')+8:context.message.content.find(' *',context.message.content.find('moradia='))]
            aparencia = context.message.content[context.message.content.find('aparencia=')+10:context.message.content.find(' *',context.message.content.find('aparencia='))]
        
            charSave = {'nome':nm,'player':context.message.author.name,'profissão':profissao,'idade':idade,'sexo':sexo,'nacionalidade':nacionalidade,'moradia':moradia,'aparência':aparencia,'status':{},'attacks':{}}
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
       await context.message.channel.send('Ficha de personagem enviada pelo privado!')
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
            statSave = {'inteligencia': inteligencia, 'força': forca, 'aparencia': aparencia, 'constituição': constituicao, 'tamanho': tamanho, 'poder': poder, 'dextreza': dextreza, 'sorte': sorte, 'educação': educacao, 'corpo': corpo, 'movimento': movimento}
            db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).update({'status': statSave, 'pericia': {'arremessar':4,'contabilidade':2,'dirigir':4,'encontrar':5,'escalar':8,'esconder':2,'escutar':5,'espingarda':5,'esquiva':int(dextreza/2),'fotografia':2,'furtividade':4,'historia':4,'historia natural':2,'intimidar':3,'lingua nativa':educacao,'lutar':5,'nadar':4,'ocultar':2,'persuadir':2,'biblioteca':4,'p.socorros':6,'pistola':4,'psicologia':2,'pular':4,'rastrear':2,'reparo.e':2,'rifle':5,'reparo.m':2,'metralhadora':3}})
            await context.message.channel.send('Status salvos com sucesso!')
    else:
        await context.message.channel.send('Você ainda não criou um personagem!')

@client.command(name = 'upstat')
async def upstat(context):
    valid_stats = ['INT','FOR','APA',' CON','tamanho','POD','DES','SOR','EDU']
    correct_name = {'INT': 'inteligencia','FOR': 'força', 'APA': 'aparencia','CON': 'constituição', 'tamanho': 'tamanho', 'POD':'poder','DES':'dextreza','SOR':'sorte','EDU':'educação'}
    stat = context.message.content[8:context.message.content.find(' *')]
    number = int(context.message.content[context.message.content.find(' *')+3:])
    if stat in valid_stats:
        charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
        if charDoc.exists:
            resultDict = charDoc.to_dict()
        resultDict['status'][correct_name[stat]] = number
        db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).set(resultDict)
        await context.message.channel.send('Status de '+correct_name[stat]+' atualizado com sucesso!')
    else:
        print(stat)
        await context.message.channel.send('Digite um status válido')

@client.command(name = 'roll')
async def roll(context):
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    
    if charDoc.exists:
        rollDoc = charDoc.to_dict()
        valid_roll = ['inteligencia','força','aparencia','constituição','poder','dextreza','sorte']
        valid_per = ['arremessar','contabilidade','dirigir','encontrar','escalar','esconder','escutar','espingarda','esquiva','fotografia','furtividade','historia','historia natural','intimidar','lingua nativa','lutar','nadar','ocultar','persuadir','biblioteca','p.socorros','pistola','psicologia','pular','rastrear','reparo.e','rifle','reparo.m','metralhadora']
        to_roll = context.message.content[6:]
        vantagem = 1
        if context.message.content.find('vantagem=') != -1:
            to_roll = context.message.content[6: context.message.content.find(' *')]
            vantagem = int(context.message.content[context.message.content.find('vantagem=')+9:])
        if to_roll in valid_roll:
            list_dice = []
            for num in range(0,abs(vantagem)+1):
                list_dice.append(random.randint(1, 20))
            if vantagem <0:
                
                dice = min(list_dice)
            else:
                
                dice = max(list_dice)
            await context.message.channel.send('Os número rolados foram... '+ str(list_dice) + '!')
            await context.message.channel.send('O número escolhido foi '+str(dice)+'!')
            if int(dice + (rollDoc['status'][to_roll]/4)) >= 21:
                await context.message.channel.send('SUCESSO EXTREMO')
            elif int(dice + (rollDoc['status'][to_roll]/2)) >= 21:
                await context.message.channel.send('SUCESSO BOM')
            elif int(dice + (rollDoc['status'][to_roll])) >= 21:
                await context.message.channel.send('SUCESSO NORMAL')
            elif dice == 1:
                await context.message.channel.send('DESASTRE')
            else:
                await context.message.channel.send('FRACASSO')
        elif to_roll in valid_per:
            dice = random.randint(1, 20)
            await context.message.channel.send('O número rolado foi... '+ str(dice) + '!')
            if int(dice + (rollDoc['pericia'][to_roll]/4)) >= 21:
                await context.message.channel.send('SUCESSO EXTREMO')
            elif int(dice + (rollDoc['pericia'][to_roll]/2)) >= 21:
                await context.message.channel.send('SUCESSO BOM')
            elif int(dice + (rollDoc['pericia'][to_roll])) >= 21:
                await context.message.channel.send('SUCESSO NORMAL')
            elif dice == 1:
                await context.message.channel.send('DESASTRE')
            else:
                await context.message.channel.send('FRACASSO')
        else:
            await context.message.channel.send('Digite um status ou uma perícia válida.')
    else:
        await context.message.channel.send('Você ainda não criou seu personagem!')
@client.command(name = 'uppericia')
async def uppericia(context):
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    
    if charDoc.exists:
        upDoc = charDoc.to_dict()
        peri = context.message.content[11: context.message.content.find(' *')]
        valor = int(context.message.content[context.message.content.find(' *')+3:])
        valid_per = ['arremessar','contabilidade','dirigir','encontrar','escalar','esconder','escutar','espingarda','esquiva','fotografia','furtividade','historia','historia natural','intimidar','lingua nativa','lutar','nadar','ocultar','persuadir','biblioteca','p.socorros','pistola','psicologia','pular','rastrear','reparo.e','rifle','reparo.m','metralhadora']
        if peri in valid_per:
            upDoc['pericia'][peri] = valor
            db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).set(upDoc)
            await context.message.channel.send('Perícia '+ peri + ' atualizada com sucesso!')
        else:
            print(peri)
            await context.message.channel.send('Digite uma perícia válida')
    else:
        await context.message.channel.send('Você não criou seu personagem ainda!')

@client.command(name = 'setattack')
async def setattack(context):
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    
    if charDoc.exists:
        nome = context.message.content[context.message.content.find('nome=')+5: context.message.content.find(' *',context.message.content.find('nome='))]
        tipo = context.message.content[context.message.content.find('tipo=')+5: context.message.content.find(' *',context.message.content.find('tipo='))]
        dano = int(context.message.content[context.message.content.find('dano=')+5: context.message.content.find(' *',context.message.content.find('dano='))])
        uso_rodada = int(context.message.content[context.message.content.find('uso_rodada=')+11: context.message.content.find(' *',context.message.content.find('uso_rodada='))])
        dado_total = context.message.content[context.message.content.find('dado=')+5: context.message.content.find(' *',context.message.content.find('dado='))]
        if context.message.content.find('municao=') != 1:
            municao = int(context.message.content[context.message.content.find('municao=')+8: context.message.content.find(' *',context.message.content.find('municao='))])
        else:
            municao = False
        newAttack = charDoc.to_dict()['attacks']
        newAttack[nome] = {'nome':nome,'tipo':tipo,'dano':dano,'uso_rodada':uso_rodada,'dado': dado_total, 'municao':municao, 'atual_municao':municao }
        db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).update({'attacks':newAttack})
        await context.message.channel.send('Ataque criado com sucesso!')
    else:
        await context.message.channel.send('Você não criou seu personagem ainda!')
@client.command(name = 'attack')
async def attack(context):
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    attack = context.message.content[8:]
    vantagem = 0
    if context.message.content.find('vantagem=') != -1:
        attack = context.message.content[8: context.message.content.find(' *')]
        vantagem = int(context.message.content[context.message.content.find('vantagem=')+9:])
    if charDoc.exists:
        if attack in charDoc.to_dict()['attacks']:
            ataque = charDoc.to_dict()['attacks'][attack]
            to_saveAt = charDoc.to_dict()['attacks']
            if ataque['tipo'] in charDoc.to_dict()['pericia']:
                go = False
                if ataque['municao'] == False:
                    go = True
                elif ataque['atual_municao'] > 0:
                    go = True
                    to_saveAt[attack]['atual_municao'] = ataque['atual_municao'] -1
                    print(ataque['atual_municao'])
                    db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).update({'attacks':to_saveAt})
                    await context.message.channel.send('Munição: '+str(ataque['atual_municao']-1))
                else:
                    await context.message.channel.send('SEM MUNIÇÃO!')
                if go:
                    list_dice = []
                    for num in range(0,abs(vantagem)+1):
                        list_dice.append(random.randint(1, 20))
                    if vantagem <0:
                    
                        dice = min(list_dice)
                    else:
                    
                        dice = max(list_dice)
                    await context.message.channel.send('Os número rolados foram... '+ str(list_dice) + '!')
                    await context.message.channel.send('O número escolhido foi '+str(dice)+'!')
                    if int(dice + (charDoc.to_dict()['pericia'][ataque['tipo']]/4)) >= 21:
                        await context.message.channel.send('SUCESSO EXTREMO')
                        await context.message.channel.send(danoMaximo(ataque['dado'],ataque['dano']))
                        await context.message.channel.send('DANO MÁXIMO!')
                            
                    elif int(dice + (charDoc.to_dict()['pericia'][ataque['tipo']]/2)) >= 21:
                        await context.message.channel.send('SUCESSO BOM')
                        await context.message.channel.send('O dano de seu ataque foi de '+str(danoDado(ataque['dado'],ataque['dano']))+ '!')
                    elif int(dice + (charDoc.to_dict()['pericia'][ataque['tipo']])) >= 21:
                        await context.message.channel.send('SUCESSO NORMAL')
                        await context.message.channel.send('O dano de seu ataque foi de '+str(danoDado(ataque['dado'],ataque['dano']))+ '!')
                    elif dice == 1:
                        await context.message.channel.send('DESASTRE')
                    else:
                        await context.message.channel.send('FRACASSO')
            else:
                await context.message.channel.send('Esse ataque não é válido')
        else:
            await context.message.channel.send('Esse ataque não existe')
@client.command(name = 'reload')
async def reload(context):
    charDoc = db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).get()
    attack = context.message.content[8:]
    if charDoc.exists:
        if charDoc.to_dict()['attacks'][attack]['municao'] != False:
            temp_ataque = charDoc.to_dict()['attacks']
            temp_ataque[attack]['atual_municao'] = temp_ataque[attack]['municao']
            db.collection('Servers').document(context.guild.name).collection('Players').document(context.message.author.name).update({'attacks':temp_ataque})
            await context.message.channel.send('Ataque recarregado com sucesso!')
def danoMaximo(dado,dano):
    startando = 0
    dano_total = dano
    lista_full = list(find_all(dado,'/'))
    lista_full.append(len(dado))
    for dice in lista_full:
        mini_dado = dado[startando:dice]
        multiplo = int(mini_dado[0:mini_dado.find('d')])
        valor = int(mini_dado[mini_dado.find('d')+1:])
        dano_total += multiplo * valor
        startando = dice+1
    return(dano_total)

def danoDado(dado,dano):
    startando = 0
    dano_total = dano
    lista_full = list(find_all(dado,'/'))
    lista_full.append(len(dado))
    for dice in lista_full:
        mini_dado = dado[startando:dice]
        multiplo = int(mini_dado[0:mini_dado.find('d')])
        valorDado = int(mini_dado[mini_dado.find('d')+1:])
        for i in range(0,multiplo):
            dano_total += random.randint(1,valorDado+1)
        startando = dice+1
    return(dano_total)
@client.event
async def on_ready():
    print('Informações básicas:')
    print('Nome do bot: {0}'.format(client.user.name))
    print('Id: {0}'.format(client.user.id))
    print('Server: {0}'.format(client.guilds))
    print('-------------------------------------------------------------------------------')

    await client.change_presence(status=discord.Status.online, activity=discord.Game("Steins Gate"))

client.run(token)