import os
import nest_asyncio
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

TOKEN = "7783620639:AAEanbapO1Ci2dnBvwxhfSiP2eBC0TQPKio"
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

menu_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    menu_state[user_id] = "main"
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text in RISPOSTE:
        await update.message.reply_text(RISPOSTE[text], parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
    else:
        await update.message.reply_text(
            "🚫 Mi dispiace, non ho capito la richiesta. Questo assistente automatico è pensato per rispondere solo alle domande più comuni.\n"
            "Per domande specifiche, verrai ricontattato privatamente via WhatsApp da *Giada*.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu
        )

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if not member.is_bot:
            await update.message.reply_text(
                f"👋 Benvenuto {member.full_name} nel gruppo di Statiellae Immobiliare!\n\n"
                "Questo è l’assistente automatico, attivo 24h su 24, per rispondere alle domande più comuni.",
                reply_markup=main_menu
            )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    await app.bot.set_webhook(url=WEBHOOK_URL)

    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_path="/webhook",
    )

# Per ambienti che hanno già un event loop (come Render)
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
