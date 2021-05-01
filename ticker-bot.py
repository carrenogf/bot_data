from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler,Filters, CallbackQueryHandler
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os

IMPUT_TEXT = 0

def start(update,context):
	update.message.reply_text(
		text="Hola, bienvenido, que deseas hacer?",
		reply_markup= InlineKeyboardMarkup([
			[InlineKeyboardButton(text='Consultar ticker', callback_data='ticker')]
			]))
def ticker_command_handler(update,context):
	update.message.reply_text("Enviame el nombre del ticker que deseas consultar.")

	return IMPUT_TEXT

def ticker_callback_handler(update,context):
    query = update.callback_query
    query.answer()
    #query.edit_message_text(text='Enviame el nombre del ticker que deseas consultar.')
    query.from_user.send_message("Enviame el nombre del ticker que deseas consultar.")
    return IMPUT_TEXT

def input_text(update,context):
    text = update.message.text
    resultado = quote(text)
    if resultado == "":
        resultado = "Ticker invalido, probá de nuevo!"
    update.message.reply_text(resultado,reply_markup= InlineKeyboardMarkup([
			[InlineKeyboardButton(text='Consultar ticker', callback_data='ticker')]
			]))
    return ConversationHandler.END

def quote(symbol):
    TOK = '2RG2NEF3IPXMIPX3'
    function = 'GLOBAL_QUOTE'
    url = 'https://www.alphavantage.co/query'
    parametros = {'function':function,'symbol':symbol,'apikey':TOK}
    r = requests.get(url, params=parametros)
    js = r.json()['Global Quote']
    #df = pd.DataFrame.from_dict(js, orient = 'index')
    texto = ""
    for dato in js:
        texto= texto+ dato + "\t" +js[dato] + "\n"
  
    return texto

data = quote('GGAL')

if __name__ == '__main__':
    TOKEN = os.getenv("TOKEN")
    updater = Updater(token=TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(ConversationHandler(
		entry_points=[
		CommandHandler('ticker',ticker_command_handler),
		CallbackQueryHandler(pattern='ticker',callback=ticker_callback_handler)
		],

		states={
		IMPUT_TEXT: [MessageHandler(Filters.text,input_text)]
		},

		fallbacks=[]
	))


    updater.start_polling()
    updater.idle()



