# -*- coding: utf-8 -*-

TOKEN = "M32UHIU4HHONEW98553EREWR.F@K3T0K3N.23NUON3ORN23OIR2.WER23R23RE"

!pip install discord.py
!pip install nest_asyncio

import asyncio
import discord
from discord.ext import commands as cmd
import nest_asyncio

nest_asyncio.apply()

import requests

url = 'https://prices.runescape.wiki/api/v1/osrs'
header = {
    'User-Agent': 'price_tracker',
    'DiscordU': 'jinx_shrimp'
}
response = requests.get(url + '/latest', headers = header)

responseN = requests.get(url + '/mapping', headers = header)

name_data = responseN.json()
NAMES_IDS = {}
for i in name_data:
  NAMES_IDS[i['name']] = i['id']

responseN.close()
response = requests.get(url + '/latest', headers = header)
response.close()
price_data = response.json()

client = cmd.Bot(command_prefix = '!', intents = discord.Intents.all())

@client.event
async def on_ready():
  print("Initialized\n-----------------")


@client.command()
async def hi(ctx):
  await ctx.send("hi")



@client.event
async def on_message(message):
  channel = client.get_channel(message.channel.id)
  if message.author.id == 204626158015217664 or message.author.id == 151360903831355393:
    await client.process_commands(message)
    await channel.send('Get your money up, not your funny up!')
  else:
    await client.process_commands(message)
    return


@client.command()
async def price(ctx, *, args):
  args = args.capitalize()
  if args not in NAMES_IDS:
    await ctx.send('you spelled ' + args + ' wrong dummy')
    return

  item_price = price_data['data'][str(NAMES_IDS[args])]
  avg = (item_price['high'] + item_price['low']) / 2
  avg = ('{:,}'.format(avg))
  await ctx.send('```ansi\n\u001b[0;32mCurrent street price for '+ args + ' is: ' + avg + '\n```')

client.run(TOKEN)
