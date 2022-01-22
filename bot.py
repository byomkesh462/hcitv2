import requests
from os import environ
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
#from pyrogram.raw.types import InputMediaPhotoExternal

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY')

bot = Client('gplink bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)

#r = requests.get('https://hcitv.herokuapp.com/hit.php?url={link}')
#event = r.json()

@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm GPlink bot. Just send me link and get short link")


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    event = await get_shortlink(link)
    #r =  await requests.get('https://hcitv.herokuapp.com/hit.php?url={link}')
    #event = r.json()
    try:
        hls_link = event.get('hls')
        posterimage = event.get('posterImage')
        videoimage = event.get('videoImage')
        subtitle = event.get('subtitle') if (event.get('subtitle') is not None) else "No Subtitle Found"
        lower = event.get('270p')
        medium = event.get('360p')
        higher = event.get('720p')
        title = event.get('title')
        description = event.get('description')
        #hls_link = await get_shortlink(link)
        await message.reply(f'Here is your [HLS Link]({hls_link})', quote=True)
        await bot.send_photo(
        chat_id=message.chat.id,
        photo=f"{videoimage}",
        caption=f"**🔰 Name:** `{title}`\n\n**🔰 Description:** `{description}`\n\n🔗 Here is your [HLS Link]({hls_link})",
        reply_to_message_id=message.message_id,
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text="🔗 HLS YTDL Link 🔗", url=hls_link) ], 
                                             [ InlineKeyboardButton(text="270P", url=lower),
                                               InlineKeyboardButton(text="360P", url=medium),
                                               InlineKeyboardButton(text="720P", url=higher) ],
                                             [ InlineKeyboardButton(text="Poster", url=posterimage),                                                
                                               InlineKeyboardButton(text="Thumbnail", url=videoimage) ], 
                                             [ InlineKeyboardButton(text="📝  Subtitles  📝", url=subtitle) ] ] ) )
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = f'https://hcitv.herokuapp.com/hit.php?url={link}'
    #params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, raise_for_status=True) as response:
            data = await response.json()
            return data


bot.run()
