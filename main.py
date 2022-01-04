import os
import requests
from keep_alive import keep_alive
from discord.ext import commands

bot = commands.Bot(
	command_prefix="!",  # Change to desired prefix
	case_insensitive=True  # Commands aren't case-sensitive
)

bot.author_id = 157610726326927361

@bot.event 
async def on_ready():  # When the bot is ready
    print("Bot connected!")
    print(bot.user)  # Prints the bot's username and ID

@bot.command(name="translate", aliases=["tl"])
async def translate(ctx,*args):
	'''Translates JP -> EN, and vice-versa.\n
	Reply to a message you wish to translate with: !translate\n
	Or, enter: !translate [Sentence to be translated]'''
	translateMe = ""
	for arg in args: translateMe += arg + " "
	if translateMe == "":
		translateMe = await ctx.channel.fetch_message(ctx.message.reference.message_id)
		translateMe = translateMe.content
	if(translateMe.isascii()): # Text is EN if all chars are ascii
		source_lang = 'EN'
		target_lang = 'JA'
	else: # Else, assume text is JA (impetfect, but should cover most cases)
		source_lang = 'JA'
		target_lang = 'EN'
	url = "https://api-free.deepl.com/v2/translate?auth_key={}".format(os.getenv('DEEPL_API_KEY'))
	headers = {'text' : translateMe, 'source_lang' : source_lang, 'target_lang' : target_lang}
	response = requests.get(url, headers)
	responseJSON = response.json()
	try:
		result = responseJSON['translations'][0]['text']
		await ctx.reply(result)
	except:
		errMsg = "Translation failed. Error code: {}".format(response.status_code)
		await ctx.reply(errMsg)

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot