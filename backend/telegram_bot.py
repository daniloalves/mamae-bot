import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from dotenv import load_dotenv
import asyncio

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '0'))  # Coloque o chat_id do admin

conteudo_pendente = {}

async def enviar_para_aprovacao(texto, imagem_url, hashtags, post_id):
    keyboard = [
        [InlineKeyboardButton("Aprovar", callback_data=f'aprovar_{post_id}')],
        [InlineKeyboardButton("Gerar Outro", callback_data=f'gerar_{post_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    from telegram import Bot
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=imagem_url,
        caption=f"{texto}\n\n{hashtags}",
        reply_markup=reply_markup
    )
    conteudo_pendente[post_id] = (texto, imagem_url, hashtags)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data.startswith('aprovar_'):
        post_id = data.split('_')[1]
        await query.edit_message_caption(caption="Aprovado! Publicando...")
        # Chame função de publicação aqui
        from social_publish import publicar_fluxo
        texto, imagem_url, hashtags = conteudo_pendente[post_id]
        publicar_fluxo(texto, imagem_url, hashtags)
        del conteudo_pendente[post_id]
    elif data.startswith('gerar_'):
        post_id = data.split('_')[1]
        await query.edit_message_caption(caption="Gerando novo conteúdo...")
        # Chame função para gerar novo conteúdo
        del conteudo_pendente[post_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot de aprovação de conteúdo ativo.")

def iniciar_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.run_polling()
