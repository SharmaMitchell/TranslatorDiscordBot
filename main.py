import os
import requests
#from secrets import DEEPL_API_KEY
from keep_alive import keep_alive
from discord.ext import commands

bot = commands.Bot(
	command_prefix="!",  # Change to desired prefix
	case_insensitive=True  # Commands aren't case-sensitive
)

bot.author_id = 157610726326927361  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def test(ctx):
	await ctx.send("hai")

@bot.command()
async def translate(ctx,*args):
	translateMe = ""
	for arg in args: translateMe += arg + " "
	if(translateMe.replace(" ","").isalnum()): # Text is EN if all chars (besides spaces) are alphanumeric
		source_lang = 'EN'
		target_lang = 'JA'
		print("EN->JP")
	else: # Else, assume text is JA (impetfect, but should cover most cases)
		source_lang = 'JA'
		target_lang = 'EN'
	url = "https://api-free.deepl.com/v2/translate?auth_key={}".format(os.getenv('DEEPL_API_KEY'))
	headers = {'text' : translateMe, 'source_lang' : source_lang, 'target_lang' : target_lang}
	response = requests.get(url, headers)
	responseJSON = response.json()
	#print(responseJSON)
	try:
		result = responseJSON['translations'][0]['text']
		await ctx.reply(result)
	except:
		errMsg = "Translation failed. Error code: {}".format(response.status_code)
		await ctx.reply(errMsg)

extensions = [
	#'cogs.cog_example'  # Same name as it would be if you were importing it
	#'cogs.cog_translate'
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot