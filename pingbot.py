# PingBot

import discord
import os

def embed(client, title:str, content:str):
	e = discord.Embed(
		title = 'PingBerry',
		color = 0xed4245,
		description = '*A bot to inform you about your Offline Pings!*'
	)
	e.set_thumbnail(
		url = client.user.avatar_url
	)
	e.set_footer(
		text = "Services under Berry Foundations - Attachment Studios",
		icon_url = "https://images-ext-1.discordapp.net/external/x_dF_ppBthHmRPQi75iuRXLMfK0wuAW2sBLTdtNlXAc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/894098855220617216/d9b9a3b48a054b9847401bb9178ed438.webp"
	)
	e.add_field(
		name = title,
		value = content
	)

	return e

def pings(text:str):
	users = []
	if "<@!" in text:
		__itr1__ = text.split('<@!')
		del __itr1__[0]
		for i in __itr1__:
			__itr2__ = i.split('>')
			users.append(__itr2__[0])
	__real__ = []
	for e in range(len(users)):
		u = users[e]
		try:
			uid = int(u)
		except:
			uid = ''
		if uid == '':
			pass
		else:
			__real__.append(uid)
	users = __real__
	return users

async def feedback(payload, client):
	u = await client.fetch_user(payload.user_id)

	if u == client.user:
		return
	
	e = payload.emoji.name

	c = await client.fetch_channel(payload.channel_id)
	m = await c.fetch_message(payload.message_id)

	if m.author == client.user:
		pass
	else:
		return

	if e == "🗑️":
		await m.delete()
	elif e == "❌":
		f = open('internal/pr.csv', 'r')
		__d__ = f.read().split(f'{m.id}')
		if len(__d__) < 2:
			e = embed(client, "Warning", "Request not valid.")
			await m.edit(embed = e)
		else:
			_d = __d__[1].split(',,')
			del _d[0]
			n_d = ",,".join(_d)
			_f = open('internal/pr.csv', 'w')
			_f.write(n_d)
			_f.close()
			e = embed(client, "Request Cancelled", "This request was cancelled.")
			await m.edit(embed=e)
		f.close()
		await m.remove_reaction('❌', client.user)
		await m.remove_reaction('✅', client.user)
	elif e == "❔":
		await help(client, m)
	elif e == "✅":
		f = open('internal/pr.csv', 'r')
		__d__ = f.read().split(f'{m.id}')
		if len(__d__) < 2:
			e = embed(client, "Warning", "Request not valid.")
			await m.edit(embed = e)
		else:
			_d = __d__[1].split(',,')
			req = _d[0].split(',')
			del _d[0]
			n_d = ",,".join(_d)
			_f = open('internal/pr.csv', 'w')
			_f.write(n_d)
			_f.close()
			del req[0]
			t = req[0]
			if t == "halt+":
				halt = await execute_halt(u)
				if halt:
					e = embed(client, "Halt Ping Services", f'Successfully halted Ping Services for [`{u.name}`](https://discord.com/users/{u.id}).')
					await m.edit(embed=e)
				else:
					e = embed(client, "Halt Ping Services", f'Failed to halt Ping Services for [`{u.name}`](https://discord.com/users/{u.id}).')
					await u.edit(embed=e)
		f.close()
		await m.remove_reaction('❌', client.user)
		await m.remove_reaction('✅', client.user)

async def send(client, ctx, user):
	if ctx.channel.type == discord.ChannelType.private:
		return
	
	f = open('internal/halt.csv', 'r')
	haltlist = f.read()
	f.close()

	if f',{user.id},' in haltlist:
		return
	
	user_status = user.mutual_guilds[0].get_member(user.id).status

	if user_status == discord.Status.offline:
		pass
	else:
		return
	
	__message__ = ctx.content[:47]

	if __message__ == ctx.content:
		pass
	else:
		__message__ += "..."
		__message__ += f'\n[View Complete Message](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.id})'
	
	__guild__ = ctx.guild.name[:7]

	if __guild__ == ctx.guild.name:
		pass
	else:
		__guild__ += "..."
	
	__channel__ = ctx.channel.name[:7]

	if __channel__ == ctx.channel.name:
		pass
	else:
		__channel__ += "..."
	
	__author__ = ctx.author.name[:17]

	if __author__ == ctx.author.name:
		pass
	else:
		__author__ += "..."
	
	e = embed(client, "Message", __message__)

	e.add_field(
		name="Information",
		value=f"""Author: [{__author__}](https://discord.com/users/{ctx.author.id})
Address: [{__guild__}/#{__channel__}](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id})"""
	)

	m = await user.send(embed=e)
	await m.add_reaction('🗑️')
	await m.add_reaction('❔')

async def trigger(ctx, client, command:str):
	dm = ctx.channel.type == discord.ChannelType.private

	f = open('internal/dm.csv', 'r')
	dm_list = f.read().split(',')
	f.close()
	
	if dm:
		if command in dm_list:
			pass
		else:
			e = embed(client, "Restrictions", "The command you used can not be used in a DM channel. Please use it in server only.")
			m = await ctx.reply(embed=e)
			await m.add_reaction('🗑️')

			return
	
	if command == "help" or command == "":
		await help(client, ctx)
	elif command == "halt":
		await halt(client, ctx)
	elif command == "unhalt":
		await unhalt(client, ctx)

async def help(client, message):
	f = open('help/main.md', 'r')
	d = f.read()
	f.close()

	contents = message.content.split(' ')
	__contents__ = []

	for c in contents:
		if c == '':
			pass
		else:
			__contents__.append(c)
	
	contents = __contents__

	if len(contents) == 0:
		pass
	else:
		del contents[0]

	e = None

	if len(contents) == 0:
		e = embed(client, "Help", d)
	else:
		if contents[0].lower() == "help":
			del contents[0]
			if len(contents) == 0:
				e = embed(client, "Help", d)
			else:
				query = " ".join(contents).lower()
				if os.path.isfile("help/" + query + '.md'):
					f = open(f'help/{query}.md', 'r')
					e = embed(client, f"Help - `{query}`", f.read())
					f.close()
				else:
					e = embed(client, "Help - Not Found", f'Failed to find help/tutorial for `{query}`.')
	
	if e == None:
		return
	
	m = await message.reply(embed=e)
	await m.add_reaction('🗑️')

async def halt(client, ctx):
	f = open('internal/halt.csv', 'r')
	haltlist = f.read()
	f.close()

	if f',{ctx.author.id},' in haltlist:
		e = embed(client, "Halt Ping Services", f"**Request failed**. [`{ctx.author.name}`](https://discord.com/users/{ctx.author.id}) is already halted the services.")
		m = await ctx.reply(embed=e)
		await m.add_reaction('🗑️')
	else:
		await confirm_halt(client, ctx.author)
		
		e = embed(client, "Halt Ping Services", f'Sent halt request to [`{ctx.author.name}`](https://discord.com/users/{ctx.author.id}).')
		m = await ctx.reply(embed=e)
		await m.add_reaction('🗑️')

async def confirm_halt(client, user):
	e = embed(client, "Halt Ping Services", "Please confirm to halt ping services.")

	m = await user.send(embed=e)
	await m.add_reaction('❌')
	await m.add_reaction('✅')
	await m.add_reaction('🗑️')

	f = open('internal/pr.csv', 'a')
	f.write(f',,{m.id},halt+,{user.id}')
	f.close()

async def execute_halt(user):
	try:
		f = open('internal/halt.csv', 'a')
		f.write(f'{user.id},')
		f.close()
		return True
	except:
		return False

async def unhalt(client, ctx):
	f = open('internal/halt.csv', 'r')
	d = f.read()
	f.close()

	if f'{ctx.author.id},' in d:
		try:
			f = open('internal/halt.csv', 'w')
			f.write(d.replace(f'{ctx.author.id},', ''))
			f.close()
			e = embed(client, "Halt Ping Services", "User removed halt list.")
		except:
			e = embed(client, "Halt Ping Services", "Failed to remove user from halt list.")

		m = await ctx.channel.send(embed=e)
		await m.add_reaction('🗑️')
	else:
		e = embed(client, "Halt Ping Services", "User not in the halt list.")

		m = await ctx.channel.send(embed=e)
		await m.add_reaction('🗑️')

