import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8740014068:AAH_M8MlNz59IhjQ1QCtR3aKvRMA7KPGXqw"
WOLFRAM_KEY = "P8EX35GPXE"

def solve_everything(question):
    try:
        url = "http://api.wolframalpha.com/v2/query"
        params = {"input": question, "appid": WOLFRAM_KEY, "output": "json", "format": "plaintext"}
        response = requests.get(url, params=params)
        data = response.json()
        
        if "queryresult" in data and data["queryresult"]["pods"]:
            for pod in data["queryresult"]["pods"]:
                if pod["title"] in ["Result", "Solution", "Answer"]:
                    return f"✅ {question}\n\n📌 {pod['subpods'][0]['plaintext']}"
            return f"✅ {question}\n\n📌 {data['queryresult']['pods'][0]['subpods'][0]['plaintext']}"
        return "❌ Не могу найти ответ"
    except:
        return "❌ Ошибка"

async def start(update, context):
    await update.message.reply_text("🧠 Бот-репетитор 24/7!\n\nПримеры:\n2x + 5 = 15\nстолица Франции")

async def handle_text(update, context):
    text = update.message.text.strip()
    if text.startswith('/'):
        return
    result = solve_everything(text)
    await update.message.reply_text(result)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
