import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import random

# Global variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APP_ID = os.getenv('APP_ID')

helpstring = "* **/prompts**: 2 characters and 2 prompts.\n" + \
	"* **/prompts <number of characters> <number of prompts>**: " + \
	"Customize the number of characters and prompts, up to 10 for both. " + \
	"Default is 2, if no number is given.\n" + \
	"* **/help**: " + \
	"Generates this help message.\n\n" + \
	"Note that repeated characters/prompts are possible."

characters = open('dcmk_characters.txt').readlines()
characters = [c.strip() for c in characters]
prompts = open('prompts.txt').readlines()
prompts = [p.strip() for p in prompts]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents, application_id=APP_ID)
tree = app_commands.CommandTree(client)
client.tree = tree

def SelectFromList(lst, n):
	# To do: eliminate the possibility of duplicates.
	return random.choices(lst, k=n)

def FormattedPrompts(n_char: int, n_prompts: int):
	if n_char < 0 or n_prompts < 0:
		return "Please use numbers greater than 0"
	if n_char > 10 or n_prompts > 10:
		return "Max 10 characters and prompts"

	selected_chars = SelectFromList(characters, n_char)
	selected_prompts = SelectFromList(prompts, n_prompts)

	formatted = ''
	if selected_chars:
		formatted += '**Characters:**\n'
		for c in selected_chars:
			formatted += f'{c}\n'

	if selected_chars and selected_prompts:
		formatted = formatted + '\n'

	if selected_prompts:
		formatted += "**Prompts:**\n"
		for p in selected_prompts:
			formatted += f'{p}\n'

	return formatted

@tree.command(name = "prompts", description = "Get DCMK prompts")
@app_commands.describe(
	num_characters="Number of random characters desired, from 0 to 10", 
	num_prompts="Number of random prompts desired, from 0 to 10")
async def get_prompts(interaction, num_characters: int = 2, num_prompts: int = 2):
	print('sending prompts in', interaction.guild.name)
	await interaction.response.send_message(
		FormattedPrompts(num_characters, num_prompts))

@tree.command(name = "help", description = "Promptsbot help")
async def get_help(interaction):
	print('sending help in', interaction.guild.name)
	await interaction.response.send_message(helpstring)

@client.event
async def on_ready():
	await tree.sync()
	print(f'{client.user} is synced and ready!')

if __name__ == '__main__':
	client.run(TOKEN)