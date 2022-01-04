# Discord.py Bot with Translation Functionality
Created using Discord.py and DeepL's translation API. Hosted on replit.

The main functionality of this bot is Japanese to English translation. The bot will attempt to translate English to Japanese as well, but translates to English by default. See wiki for details & additional feature plans/ideas.

# The Inspiration
I created this bot for use on a Japanese learning Discord server. When I was a beginner in Japanese, I would often shy away from participating in "Japanese-only" chats, since there were many words I didn't understand. I didn't want to pester people by asking them what their sentencecs meant, but I also didn't want to copy+paste dozens of messages into Google Translate so I could follow the conversation. I thought back on these times as I wondered why the "Japanese-only" chat was so inactive in a Japanese learning Discord server I'm in, and decided to make a bot to help make the chat more accessible to beginners.  

My hope is that by giving members access to a convenient translation tool, beginners will feel less overwhelmed when peering into a chat full of higher-level Japanese speakers, and more confident to join in the conversation.

# Current Features
The bot is currently capable of Japanese to English translation, and English to Japanese translation (in most cases - see wiki for details). As of now, users can manually translate Japanese or English phrases by entering: "!translate [phrase]" into the Discord chat. The bot will perform an API call using DeepL's translation API, and reply to the user with their translated text.

# Planned Features
The main feature I plan to integrate is "translation via reply", in which users could reply to a Japanese message with "!translate", and have the entire message translated by the bot. This would reduce chat clutter (albeit only slightly), and vastly improve the bot's usability.

There are many additonal features I'd like to add, such as private translation (to further reduce chat clutter) and pronunciation lookup (using Forvo's API). However, there are significant roadblocks and drawbacks to both of those features, so I don't see myself implementing them in the near future. See wiki for details.
