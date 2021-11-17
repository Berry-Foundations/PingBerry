# PingBerry

import os
import discord
import pingbot
import datetime
import web
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	web.super_run()
	await client.change_presence(activity=discord.Game(name="PingBerry!", type=discord.ActivityType.playing, start=datetime.datetime.now()))
	print(f'{client.user} is active.')

@client.event
async def on_message(ctx):
	if ctx.author == client.user:
		return
	
	pings = pingbot.pings(ctx.content)
	for i in pings:
		if i == client.user.id:
			pass
		else:
			user = await client.fetch_user(i)
			await pingbot.send(client, ctx, user)
	
	__m__ = ctx.content.split(' ')[0].lower()
	if __m__ in [f'<@!895701111074328586>', 'ping', 'pingberry', 'aditya', 'banana-is-sus:tm:', 'banana-is-sus™️']:
		message = ctx.content
		msg = message.split(' ')
		if len(msg) > 1:
			cmd = msg[1].lower()
			await pingbot.trigger(ctx, client, cmd)
		else:
			await pingbot.trigger(ctx, client, 'help')

@client.event
async def on_raw_reaction_add(payload):
	await pingbot.feedback(payload, client)

try:
	token = os.getenv('TOKEN')
	client.run(token)
	asyncio.sleep(20)
except Exception as e:
	print(e)

