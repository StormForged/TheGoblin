import random
import discord
from discord.ext import commands
import json
import aiohttp
import requests

import credentials
import chatResponses
import onMessage
import rolls
import nsfw as _nsfw
import stringHelpers
import chatBot

intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(command_prefix = ('Goblin ', 'goblin ', 'gobbo ', 'Gobbo','b '), intents = intents)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('--------')

@bot.event
async def on_message(message):	
	if(onMessage.checkGarfield(message.content)):
		await message.channel.send("nuthin")

	if 'ss13' in message.content and not message.author.bot:
		decider = random.randint(0,4)
		if(decider == 1):
			await message.channel.send(onMessage.mockery(message.content))

	decider = random.randint(1, 100)
	if(decider == 69) and not message.author.bot: 
		await message.channel.send(onMessage.mockery(message.content))
	
	await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error, *args):
	if isinstance(error, commands.errors.NSFWChannelRequired):
		await ctx.send("dis izzent a cooma channel!")
	else:
		await ctx.send(random.choice(chatResponses.errors))

@bot.command()
async def roll(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	if(len(args) == 0):
		await ctx.send(rolls.d20())
		return
	
	if(args[0][0].isalpha() == 0):
		await ctx.send(embed = rolls.userRoll(args))
	else:
		await ctx.send(rolls.d20Verbose(args))

@bot.command()
@commands.is_nsfw()
async def nsfw(ctx, *args):
	if(len(args) > 0):
		await _nsfw.userTags(ctx, args)
		return

	await _nsfw.random(ctx)

@bot.command()
async def rule34(ctx, *args):
	if(len(args) > 0):
		await _nsfw.rule34Tags(ctx, args)
		return
	
	await _nsfw.rule34Random(ctx)

@bot.command()
async def flip(ctx, *args):
	if(len(args) > 0):
		await ctx.send(rolls.flipMulti(int(args[0])))
		return

	await ctx.send(rolls.flipSingle())

@bot.command()
async def remind(ctx, *args):
	await ctx.send("alreddy 4got lmao")

@bot.command()
async def bet(ctx, *args):
	if(len(args) > 0):
		await ctx.send(rolls.betMulti(int(args[0])))
		return
	
	await ctx.send(rolls.betSingle())

@bot.command()
async def bitcoin(ctx):
	url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
	async with aiohttp.ClientSession() as session:  # Async HTTP request
		raw_response = await session.get(url)
		response = await raw_response.text()
		response = json.loads(response)
		await ctx.send("Bitcoinz iz " + response['bpi']['AUD']['rate'] + "bux")	

@bot.command()
async def wheelchair(ctx):
	await ctx.send("You're and")
	
@bot.command()
async def nise(ctx):
	await ctx.send("<:mikudesu:230366418821054464>")

@bot.command()
async def postit(ctx):
	await ctx.send(file = discord.File('it.png'))
	
@bot.command()
async def sleepy(ctx):
	await ctx.send(file = discord.File('sleepy.png'))
	
@bot.command(name = 'wakey',
				aliases = ['wakie'])
async def wakey(ctx):
	await ctx.send(file = discord.File('wakey.png'))
	
@bot.command()
async def dare(ctx):
	await ctx.send(file = discord.File('dare.png'))
	
@bot.command(name = 'wagey',
				aliases = ['wagie'])
async def wagey(ctx):
	await ctx.send(file = discord.File('wagey.png'))
	
@bot.command(name='8ball',
                aliases=['eight_ball', 'eightball', '8-ball'])
async def eight_ball(ctx):
	await ctx.send(random.choice(chatResponses.possible_responses) + ", " + ctx.message.author.mention + " " + "<a:fuuuuck:641605864582545429>")

@bot.command(name = 'is', hidden = 'true', aliases = ['have','did','would','does','should','has','cant',"can't",'can','do','are', 'will', 'am', 'art','was','wast','be','if','may','were','what'])
async def _is(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	if(len(args) > 2 and 'or' in args):
		await ctx.send(chatBot.isOptions(args) + ctx.message.author.mention)
	else:
		if(random.randint(0,30) == 25):
			await ctx.send("shut up, " + ctx.message.author.mention)
		else:
			await ctx.send(random.choice(chatResponses.is_responses) + ", " + ctx.message.author.mention)

@bot.command(hidden = 'true')
async def where(ctx, *args):
	possible_responses = ['my ass', 'ur ass', 'doopers fanny', 'israel', 'under goblinas boob flap', 'nowhere fuck off']
	await ctx.send(random.choice(possible_responses) + "<:mikudesu:230366418821054464>")

@bot.command(hidden = 'true')
async def say(ctx, *args):
    await ctx.send(stringHelpers.args2str(args))

@bot.command(hidden = 'true', aliases = ['whens', "when's"])
async def when(ctx, *args):
    await ctx.send(random.choice(chatResponses.when_responses))

@bot.command(hidden = 'true')
async def rate(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	args = stringHelpers.args2str(args)
	await ctx.send(random.choice(chatResponses.choice_responses) + " " + args + " is a " + str(random.randint(0,10)) + "/10")

@bot.command()
async def dndalign(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	args = stringHelpers.args2str(args)
	await ctx.send(random.choice(chatResponses.choice_responses) 
		+ " " + args + " is " + random.choice(chatResponses.dndalignments))

@bot.command(hidden = 'true')
async def which(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	await ctx.send(chatBot.which(args))

@bot.command(hidden = 'true')
async def why(ctx, *arg):
    await ctx.send("y keep askion gobliin y? goblin dunno y da fuck goblin no u dum?")
	
@bot.command(hidden = 'true')
async def hours(ctx, *args):
	num = random.randint(0,8)

	if(num == 0):
		await ctx.send("now")
	else:
		await ctx.send(str(num) + " hours")

@bot.command(hidden = 'true', aliases = ['whose', "who's", "who'd","whos"])
async def who(ctx, *args):
	args = stringHelpers.youMeChecker(args)

	dndChannel = bot.get_channel(782795167643336734)
	if(ctx.channel == dndChannel):
		await ctx.send(chatBot.whoDND(ctx))
		return
	
	if(len(args) > 1):
		if(args[1].endswith(',')):
			temp = args[1]
			temp = temp[:-1]
			args[1] = temp

		if(args[0] == 'would' and args[1] == 'win'):
			await ctx.send(chatBot.wouldWin(args))
			return

	if(len(args) > 2):
		if("or" in args):
			await ctx.send(chatBot.isOptions(args))
			return
		
	await ctx.send(chatBot.whoMembers(ctx))


@bot.command(hidden = 'true')
async def smash(ctx, *args):
	if len(args) > 1 and args[0] == 'or' and args[1] == 'pass':
		mes = 'smash' if random.randint(0,1) == 1 else 'pass'
		await ctx.send(mes)

@bot.command()
async def smile(ctx):
	await ctx.send("later")

@bot.command()
async def grayscale(ctx):
	await ctx.send("later")

@bot.command()
async def fmk(ctx, *args):
	if(len(args) > 1):
		fmk = [args[0], args[1], args[2]]
		random.shuffle(fmk)
		await ctx.send("gunna fuk " + fmk[0] + ", guna marry " + fmk[1] + ", and " + fmk[2] + " gitz killd")

@bot.command()
async def mmr(ctx):
	url = 'https://api.opendota.com/api/players/93577387'
	async with aiohttp.ClientSession() as session: #async HTTP request
		raw_response = await session.get(url)
		response = await raw_response.text()
		response = json.loads(response)
		await ctx.send("MMR is..." + str(response['solo_competitive_rank']))

@bot.command()
async def hero(ctx):
	hero = random.randint(0, len(chatResponses.heroes))
	embed = discord.Embed()
	embed.set_author(name = chatResponses.heroes[hero])
	embed.set_image(url = "https://stormforged.moe/heroes/" + chatResponses.heroesURL[hero] + ".png")
	embed.set_footer(text = "do it faggit")

	await ctx.send(embed = embed)

@bot.command()
async def image(ctx, *args):
	if 'aki99' in args:
		await ctx.send("no")
		return
	
	query = args

	page = 1

	start = (page - 1) * 10 + 1

	url = f"https://www.googleapis.com/customsearch/v1?key={credentials.API_KEY}&cx={credentials.SEARCH_ENGINE_ID}&searchType=image&safe=off&q={query}&start={start}"

	data = requests.get(url).json()

	search_items = data.get("items")

	roll = random.randint(0,9)

	await ctx.send(search_items[roll].get("link"))

bot.run(credentials.TOKEN)