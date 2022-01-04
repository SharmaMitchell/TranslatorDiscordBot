import os
import discord
import requests
from discord.ext import commands

class Commands(commands.Cog, name='Commands'):
	
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="translate",aliases=["tl"])
	async def translate(ctx,*args):
		translateMe = ""
		for arg in args: translateMe += str(arg) #+ " "
		url = "https://api-free.deepl.com/v2/translate?auth_key={}".format(os.getenv('DEEPL_API_KEY'))
		headers = {'text' : translateMe, 'source_lang' : 'JA', 'target_lang' : 'EN'}
		response = requests.get(url, headers)
		responseJSON = response.json()
		try:
			result = responseJSON['translations'][0]['text']
			await ctx.send(result)
		except:
			errMsg = "Translation failed. Error code: ", response.status_code
			await ctx.send(errMsg)

def setup(bot):
	bot.add_cog(Commands(bot))
