from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import telegram.error

# Inserisci qui il token valido
TOKEN = "7783620639:AAEanbapO1Ci2dnBvwxhfSiP2eBC0TQPKio"

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
    ["🚲 Servizi", "📞 Contatti"],
    ["⏰ Orari", "❓ FAQ"],
    ["🤚 Start", "🦘 Contatta Giada"]
], resize_keyboard=True)

# Dizionari di risposte
RISPOSTE = {
    "📍 Vetrina": "🔎 Consulta la vetrina aggiornata:\nhttps://www.immobiliarestatiellae.it/immobili",
    "📄 Documenti": (
        "📄 Scarica i documenti utili:\n"
        "- Contratto incarico: https://www.immobiliarestatiellae.it/contratto.pdf\n"
        "- Guida venditore: https://www.immobiliarestatiellae.it/guida.pdf"
    ),
    "🚲 Servizi": (
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
    "🤚 Start": WELCOME_MESSAGE
}

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=WELCOME_MESSAGE,
        parse_mode="Markdown",
        reply_markup=main_menu
    )

# Gestione dei messaggi
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    chat_id = update.effective_chat.id

    if text in RISPOSTE:
        await context.bot.send_message(
            chat_id=chat_id,
            text=RISPOSTE[text],
            parse_mode="Markdown",
            reply_markup=main_menu
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="❓ Non ho capito la richiesta. Verrai contattato via WhatsApp da *Giada* nel più breve tempo possibile.",
            parse_mode="Markdown",
            reply_markup=main_menu
        )

# Costruzione app e registrazione handler
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Avvio polling con gestione errori
if __name__ == "__main__":
    try:
        app.run_polling()
    except telegram.error.Conflict:
        print("❗ Un'altra istanza del bot è già attiva. Arresto automatico.")
