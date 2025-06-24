from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7783620639:AAEanbapO1Ci2dnBvwxhfSiP2eBC0TQPKio"

# Messaggio di benvenuto
WELCOME_MESSAGE = """
👋 Benvenuto nell’*assistente automatico di Statiellae Immobiliare!*

Questo assistente è stato pensato per aiutarti a trovare rapidamente le risposte alle domande più comuni e fornirti informazioni utili in autonomia, 24 ore su 24.

Nel frattempo, per domande più specifiche o urgenti puoi contattare direttamente *Giada* al numero **320 807 0022** (WhatsApp): ti risponderà nel più breve tempo possibile.

📌 Con il menu qui sotto puoi:
– Sfogliare la vetrina degli immobili disponibili  
– Scaricare documenti e guide utili  
– Scoprire i servizi offerti  
– Trovare i nostri contatti e orari  
– Leggere le risposte alle domande più frequenti

👇 Scegli una voce dal menu qui sotto per iniziare!
"""

# Tastiera principale
main_menu = ReplyKeyboardMarkup([
    ["📍 Vetrina", "📄 Documenti"],
    ["🚲 Servizi", "📞 Contatti"],
    ["⏰ Orari", "❓ FAQ"],
    ["🤚 Start", "🦘 Contatta Giada"]
], resize_keyboard=True)

# Sottomenu FAQ
faq_menu = ReplyKeyboardMarkup([
    ["❓ Incarico", "❓ Provvigioni"],
    ["❓ Documenti", "❓ Affitti"],
    ["❓ Pubblicazione", "❓ Tempi"],
    ["❓ Dettagli immobile"],
    ["🔙 Indietro"]
], resize_keyboard=True)

# Risposte generali
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

# Risposte FAQ
FAQ = {
    "❓ Incarico": "📄 L'incarico è necessario per vendere. Garantisce chiarezza e tutela entrambe le parti.",
    "❓ Provvigioni": "💰 Le provvigioni variano. Applichiamo un minimo pratica per immobili sotto i 50.000 €.",
    "❓ Documenti": "📦 Servono: visura, planimetria, atto di proprietà, certificazioni. Ti aiutiamo noi!",
    "❓ Affitti": "🔐 Richiediamo garanzie solide: buste paga, referenze, assicurazioni. Tutela massima per il proprietario.",
    "❓ Pubblicazione": "🌐 Pubblicazione su Immobiliare.it, Casa.it, Idealista, ecc. con foto/video professionali.",
    "❓ Tempi": "🗓️ Il tempo medio dipende dalla zona e dalla documentazione. Lavoriamo per vendere nel minor tempo possibile.",
    "❓ Dettagli immobile": (
        "📋 Per ogni immobile presente nella vetrina trovi indicato un *numero di riferimento* sulla foto principale (es. 'Rif. 001').\n\n"
        "⬇️ Dopo aver scelto l’immobile che ti interessa, usa il *menu a tendina* che trovi poco sopra la vetrina per aprire la relativa *scheda dettagliata*.\n\n"
        "📸 In ogni scheda troverai: foto in alta risoluzione, video, planimetrie, descrizioni approfondite e documenti utili per valutarlo al meglio.\n"
        "✅ La scheda dettagliata degli immobili presente su immobiliarestatiellae.it è la più ricca e completa che potrai trovare sugli altri annunci dei vari portali e social ✅"
    )
}

menu_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    menu_state[user_id] = "main"
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown", reply_markup=main_menu)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    # DEBUG: stampa chat ID
    print(f"📩 Messaggio ricevuto da chat ID: {update.effective_chat.id}, tipo: {update.effective_chat.type}, testo: {text}")

    if text == "❓ FAQ":
        menu_state[user_id] = "faq"
        await update.message.reply_text("❓ Domande frequenti:", reply_markup=faq_menu)

    elif text == "🔙 Indietro":
        menu_state[user_id] = "main"
        await update.message.reply_text("🔙 Torna al menu principale.", reply_markup=main_menu)

    elif text in FAQ:
        await update.message.reply_text(FAQ[text], parse_mode="Markdown", reply_markup=faq_menu)

    elif text in RISPOSTE:
        await update.message.reply_text(RISPOSTE[text], parse_mode="Markdown", reply_markup=main_menu)

    else:
        await update.message.reply_text(
            "❓ Non ho capito la richiesta. Verrai contattato via WhatsApp da *Giada* nel più breve tempo possibile. ",
            parse_mode="Markdown",
            reply_markup=main_menu
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
app.run_polling()
