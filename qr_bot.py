from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler,Filters, CallbackQueryHandler
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
import qrcode
import os

IMPUT_TEXT = 0

def start(update,context):
	update.message.reply_text(
		text="Hola, bienvenido, que deseas hacer? \n\nUsa /qr para generar un código qr.",
		reply_markup= InlineKeyboardMarkup([
			[InlineKeyboardButton(text='Generar QR', callback_data='qr')]
			]))

def qr_command_handler(update,context):
	update.message.reply_text("Enviame el texto para generarte un código QR.")

	return IMPUT_TEXT

def qr_callback_handler(update,context):
	query = update.callback_query
	query.answer()

	query.edit_message_text(
		text='Enviame el texto para generarte un código QR.'
		)

	return IMPUT_TEXT


def gerate_qr(text):

	filename = text + '.jpg'

	img = qrcode.make(text)
	img.save(filename)

	return filename

def send_qr(filename, chat):
	
	chat.send_action(
		action=ChatAction.UPLOAD_PHOTO,
		timeout=None
		)
	chat.send_photo(
		photo=open(filename, 'rb')
		)

	os.unlink(filename)

def input_text(update,context):

	text = update.message.text

	filename= gerate_qr(text)

	chat =  update.message.chat

	send_qr(filename,chat)

	return ConversationHandler.END

if __name__ == '__main__':

	updater = Updater(token='1719260461:AAE9fc1u7aVNJ605Zl8uAZSUypetJnultss', use_context=True)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler('start',start))
	dp.add_handler(ConversationHandler(
		entry_points=[
		CommandHandler('qr',qr_command_handler),
		CallbackQueryHandler(pattern='qr',callback=qr_callback_handler)
		],

		states={
		IMPUT_TEXT: [MessageHandler(Filters.text,input_text)]
		},

		fallbacks=[]
	))


	updater.start_polling()
	updater.idle()
