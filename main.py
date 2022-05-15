from bdb import effective
import coverpy as coverpy
import requests
from urllib import request, error
from telegram import Update, bot, update
from telegram import Update, ForceReply
from telegram.ext import (
    CallbackContext,
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    dispatcher
)
from googlesearch import search
from lyricsgenius import Genius
from bs4 import BeautifulSoup


def start(update: Update, context: CallbackContext):
    context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker='CAACAgIAAxkBAAEEnZ1icSYWIUleWggfbqFoLiMHbdXkjwACSAADbug3F8TgqJTdAzE-JAQ'
    )
    update.message.reply_text(
        'Welcome, {username}! \nEnter the artist & song name ⬇️\nPlease enter with "-"'
        '\nExample: Artist - Song title'.format(
            username=update.effective_user.first_name \
            if update.effective_user.first_name is not None \
            else update.effective_user.username
        )
    )


def lyr(update, context, coverpy=coverpy.CoverPy()):
    full_title = update.message.text
    full_title1 = full_title.split('-')
    searched = ''
    # getting youtube video lyrics
    searching = search(query=f'{full_title}' + 'lyrics youtube', lang='en', num=1, stop=1, pause=2)
    for s in searching:
        searched += s
    update.message.reply_text(f'VIDEO LYRICS: \n{searched}')
    # getting cover
    try:
        result = coverpy.get_cover(full_title)
        al_link = result.artwork(800)
    except coverpy.exceptions.NoResultsException:
        print("Nothing found.")
    except requests.exceptions.HTTPError:
        print("Could not execute GET request")
    update.message.reply_photo(al_link, 'Enjoy🎸')
    # getting lyrics
    genius = Genius('genius token')
    artist = genius.search_artist(full_title1[0], max_songs=0, sort="title")
    song = artist.song(full_title1[1])
    lyr1 = song.lyrics
    parted = lyr1.split('Verse')
    if len(lyr1) > 8000 or len(lyr1) > 6000 or len(lyr1) > 5000:
        update.message.reply_text(parted[0])
        update.message.reply_text(parted[1])
        update.message.reply_text(parted[2])
        parted2 = parted[3].split('')
        update.message.reply_text(parted2[0])
        update.message.reply_text(parted2[1:])
    elif len(lyr1) > 4096:
        update.message.reply_text(parted[0])
        update.message.reply_text(parted[1])
        update.message.reply_text(parted[2])
    else:
        update.message.reply_text(lyr1)


updater = Updater(token='token', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))

lyrs = MessageHandler(Filters.text, lyr)
updater.dispatcher.add_handler(lyrs)

updater.start_polling()
updater.idle()
