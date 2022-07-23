#!/usr/bin/python3.10

import os
import discord
from dotenv import load_dotenv
from scraper import scrape,top_scrape

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Creating an instance of Client
client = discord.Client()

# Checks if the bot has successfully connected
@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

# Function that replies to a user's message
@client.event
async def on_message(message):
	
	# Prevents the bot from messaging itself
	if message.author == client.user:
		return

	if message.content == '/ssb':
		specialsTable = scrape()
		await message.channel.send(f'Here are the specials for today: \n```\n{specialsTable}\n```')

	botCommands = message.content.split(' ')
	if len(botCommands) > 1 and botCommands[0] == '/ssb':
		if botCommands[1] == 'top' or botCommands[1] == 'top_sellers':
			topTable = top_scrape()
			await message.channel.send(f'Here are the top sellers for today: \n```\n{topTable}\n```')


client.run(TOKEN)