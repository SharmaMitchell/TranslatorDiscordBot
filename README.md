# Discord Bot with Translation Functionality
![KomiBot-Banner](https://user-images.githubusercontent.com/90817905/162596866-dcc3a9cc-8abb-4575-bcf8-f015561e52f2.png)
Created using the Discord.py python library for Discord chat integration, and DeepL's translation API.

This bot translates Discord chat messages from Japanese to English (and vice versa). Users can enter "!translate [text]" into the Discord chat to have their text translated, or reply to a message with "!translate" to have the message they replied to translated. (The abbreviation "!tl" can also be used, in place of "!translate".)

This functionality allows users to quickly look up words they don't know how to say in Japanese, translate words they don't understand into English, or translate entire phrases between the two languages - all without having to switch back & forth between a dictionary website and Discord. 
See wiki for details & additional feature plans/ideas.

## Usage
To use the bot for Japanese-English translation, you can add my deployment called "KomiBot" to your Discord server by [clicking here](https://discord.com/api/oauth2/authorize?client_id=926710612900331601&permissions=274877910016&scope=bot).  

To adapt the bot to your own use case (different languages, translation tools, slash commands, etc.), fork the repository and create your own `DEEPL_API_KEY`, `DISCORD_BOT_SECRET`, and `DISCORD_BOT_AUTHOR_ID` environment variables. After that, you should be able to run the bot and change it as needed!

Feel free to reach out to me (Mitchell) on [Discord](https://discord.com/users/157610726326927361) if you have any questions.

## Current Features
The bot is currently capable of Japanese to English translation, and English to Japanese translation (in most cases - see wiki for details). As of now, users can translate Japanese or English phrases by entering: "!translate [phrase]" into the Discord chat. Additionally, users can reply to any message with "!translate" to have the entire message translated.

## Planned Features
There are many additional features I'd like to add, such as private translation via slash commands (to further reduce chat clutter) and pronunciation lookup (using Forvo's API). These are on my long-term to-do list for the bot, but will likely require significant refactoring to set up, so I'm not sure when they'll be available.  

If you'd like to contribute, you're welcome to fork the repository and create a pull request for a new feature implementation. Feature ideas are also welcome in the issues tab!

## Known Issues
- Text containing *any* non-ASCII text (excluding emojis) is treated as Japanese
- Custom Discord community emojis excluded from output, or "demojified" (replaced with emoji name)

Both of the above issues are because of how the bot checks source language of input text: by convering unicode emojis to their english representation (e.g. 😂 -> \: joy \:), then checking if the string is able to be encoded in ASCII. 

This method is fast (yielding fast translation throughput), and works as intended for the bot's use case. However, in rare cases it can result in unexpected translation output. For example, if a sentence that is 99% English contains a single Japanese character, it will be "translated" back into English. Custom emoji for Discord communities are also sometimes "demojified" (converted to their emoji title), and returned to the discord chat as-is in the translation output. 

## The Inspiration
I created this bot for use on a Japanese learning Discord server. As someone who studied Japanese for 4 years, I remember being a beginner in the language, shying away from participating in "Japanese-only" chats, since there were many words I didn't understand. I didn't want to pester people by asking them what their sentences meant, but I also didn't want to copy+paste dozens of messages into Google Translate so I could follow the conversation. I thought back on these times as I wondered why the "Japanese-only" chat room was so inactive in a Japanese learning Discord server I'm in, and decided to make a bot to help make the chat more accessible to beginners.  

My hope is that by giving members access to a convenient translation tool, beginners will feel less overwhelmed when peering into a chat room full of higher-level Japanese speakers, and more confident to join in the conversation.

## The Implementation
I started by creating a simple Discord bot using the Discord.py library, which made it quick to set up a bot to monitor chat messages, waiting for a command. I then implemented a translation command, which would parse any text following "!translate" at the beginning of a chat message. Using the python request module, I set up a function to send the text from the translate command, along with the source & target languages, to the DeepL translation API, which would return the translated text. Finally, I used a Discord.py function to have the bot reply the translated text to the user who used the "!translate" command. 

I later iterated upon the !translate function to have it automatically detect the source language by checking if the source text can be encoded with ASCII. Japanese characters cannot be encoded with ASCII, so messages containing non-ASCII characters are sent to DeepL as Japanese to be translated into English (known issue: emojis. See wiki and/or "Known Issues" below)

Additionally, I implemented a feature allowing users to reply to a message with the translation command to have the entire message translated. To do this, I added a condition to the translation function to check if the message containing the "!translate" command was empty (other than the command). In this case, the message that the command replied to will be used as the source text for the translation.



**Thanks for reading!** I hope this bot helps with your langauge learning journey (or your cross-language communication with your team, or your language barrier relationship, etc. etc.)!

