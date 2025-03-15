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

def increment_translation_count():
    try:
        # Open the file in read and write mode
        with open('./messageCount.txt', 'r+') as file:
            # Read the current count from the file
            file_content = file.read()

            # If the file is empty or has an invalid value, start with count = 0
            if file_content.strip() == "":  # Checking if the file is empty
                count = 0
            else:
                count = int(file_content)  # Convert the content to an integer

            # Increment the count
            count += 1

            # Move the file pointer to the beginning of the file
            file.seek(0)

            # Write the updated count as a string
            file.write(str(count))

    except FileNotFoundError:
        # If the file doesn't exist, create it and write the count as 1
        with open('./messageCount.txt', 'w') as file:
            file.write("1")

@bot.event
async def on_ready():  # When the bot is ready
    print("Bot connected!")
    print(bot.user)  # Prints the bot's username and ID
    
    # List to store guilds with their names and member counts
    guilds_info = []
    
    # Fetch guilds with counts to get the approximate member count
    async for guild in bot.fetch_guilds(with_counts=True):  # Fetch guilds with member counts
        guilds_info.append((guild.name, guild.approximate_member_count or 0))
    
    # Sort the guilds by member count in descending order
    guilds_info.sort(key=lambda x: x[1], reverse=True)
    
    # Total member count calculation
    total_members = sum(guild[1] for guild in guilds_info)
    
    # Server count
    server_count = len(bot.guilds)
    
    # Update the activity status with the total members and server count
    activityMessage = f"Serving {total_members} users, across {server_count} servers"
    print(activityMessage)
    await bot.change_presence(activity=discord.CustomActivity(name=activityMessage))
    
    # Print the top 10 guilds by member count
    print("\nTop 10 Guilds by Members:")
    for i in range(min(10, len(guilds_info))):  # Print top 10 or less if there are fewer than 10 guilds
        guild_name, member_count = guilds_info[i]
        print(f"{i + 1}. {guild_name}: {member_count} members")


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
        print("Error: ", response.text)
        await ctx.reply(errMsg)
    increment_translation_count()


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
