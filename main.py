import os
import requests
import emoji
import discord
from keep_alive import keep_alive
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()  # Default intents, no message_content intent required
intents.guilds = True  # Ensure guild-related events are enabled
intents.messages = True  # Enable message events
intents.reactions = True  # Enable reaction events

bot = discord.Client(intents=intents)

bot.author_id = os.environ['DISCORD_BOT_AUTHOR_ID']  # Discord ID of the bot author
messageCountFile = os.getenv('MESSAGE_COUNT_FILEPATH')

# Function to update and retrieve the translation count from a file
def get_translation_count():
    try:
        with open(messageCountFile, 'r') as file:
            count = int(file.read())
    except FileNotFoundError:
        count = 0  # If the file doesn't exist, assume 0 translations
    return count

def increment_translation_count():
    try:
        # Ensure the directory for the message count file exists
        os.makedirs(os.path.dirname(messageCountFile), exist_ok=True)

        with open(messageCountFile, 'r+') as file:
            file_content = file.read()
            count = int(file_content) if file_content.strip() else 0
            count += 1
            file.seek(0)
            file.write(str(count))
    except FileNotFoundError:
        logger.warning(f"Message count file not found at {messageCountFile}. Initializing with count 1.")
        try:
            with open(messageCountFile, 'w') as file:
                file.write("1")
        except Exception as e:
            logger.error(f"Failed to create message count file: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

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


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the bot is mentioned
    if bot.user.mentioned_in(message):
        translateMe = message.content.replace(f"<@{bot.user.id}>", "").strip()

        # If the message is a reply, fetch the replied-to message content
        if message.reference and not translateMe:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            translateMe = replied_message.content.strip()

        if not translateMe:  # If still no text provided, reply with usage instructions
            await message.reply("Please provide text to translate after mentioning me or reply to a message.")
            return

        print("Translation request received:", translateMe)

        # Determine source and target languages
        if emoji.demojize(translateMe).isascii():
            source_lang = 'EN'
            target_lang = 'JA'
        else:
            source_lang = 'JA'
            target_lang = 'EN'

        url = "https://api-free.deepl.com/v2/translate"
        headers = {
            'Authorization': f"DeepL-Auth-Key {os.getenv('DEEPL_API_KEY')}"
        }
        data = {
            'text': translateMe,
            'source_lang': source_lang,
            'target_lang': target_lang
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            responseJSON = response.json()

            if 'translations' in responseJSON and responseJSON['translations']:
                result = responseJSON['translations'][0]['text']
                print("Translated output:", result)
                await message.reply(result)
            else:
                logger.error("Unexpected API response format: %s", responseJSON)
                await message.reply("Translation failed due to an unexpected response format.")
        except Exception as e:
            logger.error("Error during translation: %s", e)
            await message.reply("Translation failed. Please try again later.")

        if messageCountFile:
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
