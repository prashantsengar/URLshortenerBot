import worker
import logging
from uuid import uuid4
logging.basicConfig(level=logging.INFO,filename='h.txt',filemode='w',
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, Filters, RegexHandler
from telegram.utils.helpers import escape_markdown
##from telegram import InlineKeyboardButton, InlineKeyboardMarkup

token = BOT_TOKEN

users = set()
def add_user(user, bot):
    users.add(user.id)
    with open('users.txt','w') as file:
        file.write(str(users))
    bot.send_message(-1001322632288, text=str(users))
    bot.send_message(-1001322632288, text=f'Total number of users: {len(users)}')
    
    
def inlinequery(update, context):
    """Handle the inline query."""
    query = context.inline_query.query

    results = list()
    if worker.is_url(query):
        
        if 'longer.ga' in query:
            long_url = worker.expand(query)
            q = InlineQueryResultArticle(
                id=uuid4(),
                title="Expanded URL",
                input_message_content=InputTextMessageContent(long_url))
            results.clear()
            results.append(q)
        else:
            short_url = worker.shorten(query)
            results = [InlineQueryResultArticle(
                id=uuid4(),
                title="Short URL",
                input_message_content=InputTextMessageContent(short_url))]
    ##        results.clear()
    ##        results.append(q)
    else:
        results.clear()
        q = InlineQueryResultArticle(
                id=uuid4(),
                title="Invalid URL",
                input_message_content=InputTextMessageContent('URL is invalid'))
        results.append(q)

    context.inline_query.answer(results)



def short(bot, update, args):
    if args:
        print('hello')
    ##    print(update.args)
        print(args)
        url = args[0]
        print('again')
        keyword=None
        if len(args)>1:
            keyword = args[1]
        if worker.is_url(url):
            try:
                short_url = worker.shorten(url, keyword)
                if type(short_url)==tuple:
                    short_url=short_url[0]
                    update.message.reply_text('This URL is already in our database')
                update.message.reply_text('Here is the short URL:')
                update.message.reply_text(short_url)

            except Exception as e:
                update.message.reply_text('There was some problem')
                print('yo')
                if str(e)=='keyword':
                    msg = (f'\'{keyword}\' keyword is already registered\n'
                           'Please send another keyword or'
                            ' leave it blank to randomize it')
                    update.message.reply_text(msg)
                print(e)
                logging.warning(e)
        else:
            update.message.reply_text(f'{url} is not a valid URL')
    else:
        update.message.reply_text(f'Am I supposed to dance in the rain? :D')
        update.message.reply_text(f'''Please send me the URL to be shortened in this format
                                  \n/short URL keyword(optional)''')
        
def expand(bot, update, args):
    url = args[0]
    if worker.is_url(url):
        try:
            long_url = worker.expand(url)
            update.message.reply_text('Here is the expanded URL:')
            update.message.reply_text(long_url)
        except Exception as e:
            print(e)
            logging.warning(e)
            update.message.reply_text('There was some problem')
        
    else:
        update.message.reply_text(f'{url} is not a valid URL')

def start(bot, update):
    msg="""Hi, I am URL shortener bot. I can shorten any URL that you send me. If you have a short URL, I can expand it too.
Usage
/short URL keyword(optional)
/expand SHORT_URL

Contact @yoptgyo_bot for any queries"""
    
    update.message.reply_text(msg)
    add_user(update.effective_user, bot)
##    print(update.effective_user)

##def start_callback(update, context):
####    user_says = " ".join(context.args)
####    update.message.reply_text("You said: " + user_says)
##    context.message.reply_text("Welcome to my awesome bot!")
    
def main():
    updater = Updater(token)
##    updater.dispatcher.add_handler(CommandHandler('start',start))
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler('short',short,pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('expand',expand,pass_args=True))
    updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
