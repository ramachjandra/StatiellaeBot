
from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config

app = Flask(__name__)
bot = telegram.Bot(token=config.BOT_TOKEN)

@app.route(f"/{config.BOT_TOKEN}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id if update.message else update.callback_query.message.chat.id

    if update.message and update.message.text:
        text = update.message.text.lower()
        if text == "/start":
            keyboard = [[InlineKeyboardButton("Vai al sito", url="https://example.com")],
                        [InlineKeyboardButton("Mostra messaggio", callback_data="mostra_messaggio")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=chat_id, text="Benvenuto! Cosa vuoi fare?", reply_markup=reply_markup)
        else:
            bot.send_message(chat_id=chat_id, text=f"Hai scritto: {text}")
    elif update.callback_query:
        query = update.callback_query
        if query.data == "mostra_messaggio":
            bot.send_message(chat_id=chat_id, text="Hai premuto il pulsante!")

    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "Bot attivo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
