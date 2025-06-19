import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')  # Coloque o chat_id do admin

updater = Updater(TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

conteudo_pendente = {}

def enviar_para_aprovacao(texto, imagem_url, hashtags, post_id):
    keyboard = [
        [InlineKeyboardButton("Aprovar", callback_data=f'aprovar_{post_id}')],
        [InlineKeyboardButton("Gerar Outro", callback_data=f'gerar_{post_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    updater.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=imagem_url,
        caption=f"{texto}\n\n{hashtags}",
        reply_markup=reply_markup
    )
    conteudo_pendente[post_id] = (texto, imagem_url, hashtags)

def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data.startswith('aprovar_'):
        post_id = data.split('_')[1]
        query.edit_message_caption(caption="Aprovado! Publicando...")
        # Chame função de publicação aqui
        from social_publish import publicar_fluxo
        texto, imagem_url, hashtags = conteudo_pendente[post_id]
        publicar_fluxo(texto, imagem_url, hashtags)
        del conteudo_pendente[post_id]
    elif data.startswith('gerar_'):
        post_id = data.split('_')[1]
        query.edit_message_caption(caption="Gerando novo conteúdo...")
        # Chame função para gerar novo conteúdo
        del conteudo_pendente[post_id]

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot de aprovação de conteúdo ativo.")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(callback_handler))

def iniciar_bot():
    updater.start_polling()
    updater.idle()
