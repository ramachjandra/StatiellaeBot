from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode
import os

TOKEN = "7783620639:AAEanbapO1Ci2dnBvwxhfSiP2eBC0TQPKio"
WEBHOOK_URL = "https://statiellaebot.onrender.com"  # 🔁 SOSTITUISCI con il tuo URL completo Render

# Messaggio di benvenuto
WELCOME_MESSAGE = """
👋 Benvenuto nell’*assistente automatico di Statiellae Immobiliare!*

Questo assistente è attivo 24/7 per fornirti informazioni utili.

Per richieste urgenti puoi contattare direttamente *Giada* su WhatsApp al **320 807 0022**.

👇 Usa il menu qui sotto per iniziare.
"""

# Tastiera principale
main_menu = ReplyKeyboardMarkup([
    ["📍 Vetrina", "📄 Documenti"],
    ["🛠 Servizi", "📞 Contatti"],
    ["⏰ Orari", "❓ FAQ"],
    ["🦘 Contatta Giada", "🔄 Riavvia"]
], resize_keyboard=True)

# Risposte generali
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

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    menu_state[user_id] = "main"
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)

# Messaggi normali
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

# Nuovi membri nel gruppo
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if not member.is_bot:
            await update.message.reply_text(
                f"👋 Benvenuto {member.full_name} nel gruppo di Statiellae Immobiliare!\n\n"
                "Questo è l’assistente automatico, attivo 24h su 24, per rispondere alle domande più comuni.",
                reply_markup=main_menu
            )

# Avvio con webhook
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    await app.bot.set_webhook(WEBHOOK_URL)
await app.run_webhook(
    listen="0.0.0.0",
    port=int(https://statiellaebot.onrender.com("PORT", 10000)),
    webhook_url="/webhook"
)

    )

import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

