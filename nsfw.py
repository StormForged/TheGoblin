import credentials

import json
import discord
import aiohttp
import random as rand
import xml.etree.ElementTree as ET

#db = danbooru
#r34 = rule34
dbURL = 'https://danbooru.donmai.us/posts.json?random=true&limit=1&tags='
dbAuthorURL = 'https://danbooru.donmai.us/posts/'
dbFooter = "Picture from danbooru.donmai.us"

r34PostsURL = "https://rule34.xxx/index.php?page=post&s=view&id="
auth =  aiohttp.BasicAuth(login = credentials.danbooruUser, password = credentials.danbooruPass)

async def random(ctx):
	async with aiohttp.ClientSession(auth = auth) as session:
		raw_response = await session.get(dbURL)
		response = await raw_response.text()

		response = json.loads(response)

		authorURL = dbAuthorURL + str(response[0]['id'])
		imgURL = response[0]['file_url']

		await ctx.send(embed = embedGenerator("Random", authorURL, imgURL, dbFooter))

async def userTags(ctx, args):
	tags = collateTags(args, False)
	
	if(tags == "no"):
		await ctx.send("nope")
		return

	requestURL = dbURL + tags

	tags = tags.replace("%20", " ")

	async with aiohttp.ClientSession(auth = auth) as session:
		raw_response = await session.get(requestURL)
		response = await raw_response.text()

		response = json.loads(response)

		authorURL = dbAuthorURL + str(response[0]['id'])
		imgURL = response[0]['file_url']

		await ctx.send(embed = embedGenerator(tags, authorURL, imgURL, dbFooter))

async def rule34Random(ctx):
	async with aiohttp.ClientSession() as session:
		raw_response = await session.get('https://rule34.xxx/index.php?page=dapi&s=post&q=index&')
		response = await raw_response.text()

		root = ET.fromstring(response)

		num = rand.randint(0, len(root) - 1)

		imgURL = root[num].get('file_url')
		authorURL = r34PostsURL + root[num].get('id')

		await ctx.send(embed = embedGenerator("Random in last 100 posts", authorURL, imgURL, "Image from rule34.xx"))

async def rule34Tags(ctx, args):
	tags = collateTags(args, True)
	
	if(tags == "no"):
		await ctx.send("nope")
		return

	async with aiohttp.ClientSession() as session:
		raw_response = await session.get('https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + tags)
		response = await raw_response.text()

		root = ET.fromstring(response)

		num = rand.randint(0, len(root) - 1)

		imgURL = root[num].get('file_url')
		authorURL = r34PostsURL + root[num].get('id')
		tags = tags.replace("+", " ")

		await ctx.send(embed = embedGenerator(tags, authorURL, imgURL, "Image from rule34.xx"))

def embedGenerator(tags, authorUrl, imgUrl, footer):
	embed = discord.Embed()
	embed.set_author(name = "Search result for: " + tags, url = authorUrl)
	embed.set_image(url = imgUrl)
	embed.set_footer(text = footer)
	
	return embed

def collateTags(args, r34):
	token = '%20'
	if(r34):
		token = '+'

	tags = ''
	for arg in args:
		if arg == "aki99":
			return "no"
		
		tags += arg + token

	return tags