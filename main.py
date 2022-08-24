import os
import requests
import emoji
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
	print(translateMe)
	if translateMe == "": # If no args, get the msg this command replied to
		translateMe = await ctx.channel.fetch_message(ctx.message.reference.message_id)
		translateMe = translateMe.content
	if(emoji.demojize(translateMe).isascii()): # Text is EN if all chars (excl emoji) are ascii
		source_lang = 'EN'
		target_lang = 'JA'
		print(translateMe, "is English")
	else: # Else, text is JA
		source_lang = 'JA'
		target_lang = 'EN'
		print(translateMe, "is Japanese")
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
token = os.environ['DISCORD_BOT_SECRET']
try:
	bot.run(token)  # Starts the bot
except Exception as e:
	print("Bot unable to start")
	print(e.__class__)
	if bot.is_ws_ratelimited():
		print("Rate Limited, Unable to start")