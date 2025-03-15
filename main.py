import os
import requests
import emoji
import csv
import discord
from keep_alive import keep_alive
from discord.ext import commands
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    intents=intents,
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)

bot.author_id = os.environ['DISCORD_BOT_AUTHOR_ID']  # Discord ID of the bot author

# Function to update and retrieve the translation count from a file
def get_translation_count():
    try:
        with open('./messageCount.txt', 'r') as file:
            count = int(file.read())
    except FileNotFoundError:
        count = 0  # If the file doesn't exist, assume 0 translations
    return count

def update_translation_count(count):
    with open('./messageCount.txt', 'w') as file:
        file.write(str(count))

@bot.event
async def on_ready():  # When the bot is ready
    print("Bot connected!")
    print(bot.user)  # Prints the bot's username and ID
    user_count = sum(g.approximate_member_count for g in bot.guilds)
    server_count = len(bot.guilds)
    activityMessage = f"Serving {user_count} users, across {server_count} servers" 
    print(activityMessage)
    await bot.change_presence(activity=discord.CustomActivity(name=activityMessage))


@bot.command(name="translate", aliases=["tl"])
async def translate(ctx, *args):
    '''Translates JP -> EN, and vice-versa.\n
        Reply to a message you wish to translate with: !translate\n
        Or, enter: !translate [Sentence to be translated]'''

    print('TL request received')
    channel = ctx.channel.name
    server = ctx.guild.name
    user = ctx.author

    translateMe = ""
    for arg in args:
        translateMe += arg + " "

    print("Translation request: ", translateMe)
    if translateMe == "":  # If no args, get the msg this command replied to
        translateMe = await ctx.channel.fetch_message(
            ctx.message.reference.message_id)
        translateMe = translateMe.content
    if (emoji.demojize(translateMe).isascii()
            ):  # Text is EN if all chars (excl emoji) are ascii
        source_lang = 'EN'
        target_lang = 'JA'
    else:  # Else, text is JA
        source_lang = 'JA'
        target_lang = 'EN'
    url = "https://api-free.deepl.com/v2/translate?auth_key={}".format(
        os.getenv('DEEPL_API_KEY'))
    headers = {
        'text': translateMe,
        'source_lang': source_lang,
        'target_lang': target_lang
    }
    
    try:
        response = requests.get(url, headers)
        responseJSON = response.json()
        result = responseJSON['translations'][0]['text']
        print("Translated output: ", result)
        await ctx.reply(result)
    except:
        errMsg = "Translation failed. Error code: {}".format(
            response.status_code)
        print("Error: ", errMsg)
        await ctx.reply(errMsg)


keep_alive()  # Starts a webserver to be pinged.
token = os.environ['DISCORD_BOT_SECRET']  # Discord bot token: Discord dev portal -> Your Bot -> Token

try:
    bot.run(token)  # Starts the bot
except Exception as e:
    print("Bot unable to start")
    print(e.__class__)
    print(e.status)
    # print(e.__dict__)
    print(e.response)
    if e.status == 429:
        print("Rate Limited, Unable to start")
