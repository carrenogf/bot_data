from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler,Filters
from bs4 import BeautifulSoup
import requests
import logging
import os

IMPUT_TEXT = 0

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update,context):
	update.message.reply_text(
		text="Bienvenido! soy el robot de pruba de Fran")

def dolar(update,context):
  texto = dolar_scraping()
  context.bot.send_message(chat_id=update.effective_chat.id, text=texto)

def gaceta(update,context):
  texto = gaceta_scraping()
  context.bot.send_message(chat_id=update.effective_chat.id, text=texto)

def dolar_scraping():
    url = requests.get('https://www.dolarhoy.com/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find_all('div', {'class': 'val'})
    titulos = ['Blue compra','Blue venta','Mep compra','Mep venta','CCL compra','CCL venta','Solidario']
    texto = ""
    try:
      for i  in range(len(titulos)):
        texto = texto + titulos[i] + " : " + result[i].text + " \n"
    except:
      texto = "Hubo un error al obtener los datos"
    return texto

def gaceta_scraping():
    url = requests.get('https://www.lagaceta.com.ar/ultimo-momento')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find_all('div', {'class': 'text'})
    lista = []
    for titulo in result:
     lista.append(titulo.text)
    lista.pop() #elimina el ultimo
    texto = ""
    for i in range(10):
      if not "GACETA" in lista[i] :
        texto = texto + "\n" + str(i+1) +") " + lista[i][1:] + "--------"
    return texto


def ticker(update,context):
	update.message.reply_text("Enviame el nombre del ticker que deseas consultar.")
	return IMPUT_TEXT

def respuesta_ticker(update,context):
    text = update.message.text
    resultado = quote(text)
    if resultado == "":
        resultado = f"No encontré {text}, Probá con:\n" + searchSimbol(text)
    update.message.reply_text(resultado)
    return ConversationHandler.END

def quote(symbol):
    TOKENAV = os.getenv("TOKENAV")
    function = 'GLOBAL_QUOTE'
    url = 'https://www.alphavantage.co/query'
    parametros = {'function':function,'symbol':symbol,'apikey':TOKENAV}
    r = requests.get(url, params=parametros)
    js = r.json()['Global Quote']
    texto = ""
    for dato in js:
        texto= texto+ dato + "\t" +js[dato] + "\n"
    return texto

def searchSimbol(keywords):
    TOKENAV = os.getenv("TOKENAV")
    function = 'SYMBOL_SEARCH'
    url = 'https://www.alphavantage.co/query'
    parametros = {'function':function,'keywords':keywords,'apikey':TOKENAV}
    r = requests.get(url, params=parametros)
    js = r.json()['bestMatches']
    texto = ""
    for dato in js:
        texto= texto+ dato["1. symbol"] + "  -  " +dato["2. name"]  + "\n"
    return texto

if __name__ == '__main__':
    TOKEN = os.getenv("TOKEN")
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('dolar', dolar))
    dp.add_handler(CommandHandler('gaceta', gaceta))
    dp.add_handler(ConversationHandler(
		entry_points=[CommandHandler('ticker',ticker)],
		states={IMPUT_TEXT: [MessageHandler(Filters.text,respuesta_ticker)]},
		fallbacks=[]
	))


    updater.start_polling()
    updater.idle()



