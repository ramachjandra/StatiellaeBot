ISTRUZIONI PER IL DEPLOY SU RENDER

1. Crea un nuovo Web Service su https://dashboard.render.com
2. Carica questi file su GitHub o direttamente su Render
3. Imposta il build command vuoto
4. Start command: python main.py
5. Quando Render assegna un URL (es. https://mio-bot.onrender.com), sostituiscilo al posto di "https://example.onrender.com" nel setWebhook (può essere fatto anche con Postman o curl):
   https://api.telegram.org/bot<IL_TUO_TOKEN>/setWebhook?url=https://mio-bot.onrender.com/<IL_TUO_TOKEN>