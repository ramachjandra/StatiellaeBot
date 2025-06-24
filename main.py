import os
import nest_asyncio
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

TOKEN = os.environ.get("BOT_TOKEN", "7783620639:AAEanbapO1Ci2dnBvwxhfSiP2eBC0TQPKio")
WEBHOOK_URL = "https://statiellaebot.onrender.com/webhook"

WELCOME_MESSAGE = """
👋 Benvenuto nell’*assistente automatico di Statiellae Immobiliare!*

Questo assistente è attivo 24/7 per fornirti informazioni utili.

Per richieste urgenti puoi contattare direttamente *Giada* su WhatsApp al **320 807 0022**.

👇 Usa il menu qui sotto per iniziare.
"""

main_menu = ReplyKeyboardMarkup([
    ["📍 Vetrina", "📄 Documenti"],
    ["🛠 Servizi", "📞 Contatti"],
    ["⏰ Orari", "❓ FAQ"],
    ["🦘 Contatta Giada", "🔄 Riavvia"]
], resize_keyboard=True)

RISPOSTE = {
    "📍 Vetrina": "🔎 Consulta la vetrina aggiornata:\nhttps://www.immobiliarestatiellae.it/immobili",
    "📄 Documenti": (
        "📄 Scarica i documenti utili:\n"
        "- Contratto incarico: https://www.immobiliarestatiellae.it/contratto.pdf\n"
        "- Guida venditore: https://www.immobiliarestatiellae.it/guida.pdf"
    ),
    "🛠 Servizi": (
        "📋 Offriamo:\n"
        "- Compravendita e affitti\n"
        "- Vetrina esclusiva con foto/video/drone\n"
        "- Attivazione utenze luce/gas/internet/acqua\n"
        "- Supporto a clienti stranieri\n"
        "- Assistenza legale e notarile\n"
        "- Valutazioni e consulenza affitti turistici"
    ),
    "📞 Contatti": (
        "📞 Tel: 0144 35 77 29\n"
        "📱 Cell: 320 807 0022\n"
        "📧 Email: giada.berettaromeo@immobiliarestatiellae.it"
    ),
    "⏰ Orari": (
        "🕒 Siamo aperti:\n"
        "Lunedì–Sabato: 09:30–12:00 / 15:30–19:30\n"
        "🗓️ Domenica: *su appuntamento*"
    ),
    "🦘 Contatta Giada": "📱 WhatsApp o telefono: 320 807 0022",
    "🔄 Riavvia": WELCOME_MESSAGE
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = RISPOSTE.get(text, "🚫 Comando non riconosciuto. Usa il menu.")
    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
