
from flask import Flask, request
from config import TOKEN, WEBHOOK_PATH
import requests
import json, os

app = Flask(__name__)

API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    url = API + "/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=data)

def start(chat_id):
    keyboard = {
        "inline_keyboard":[
            [{"text":"شراء رقم 📱","callback_data":"buy_number"}],
            [{"text":"حسابي 👤","callback_data":"account"}]
        ]
    }
    send_message(chat_id,"اهلا بك في بوت الأرقام الوهمية",keyboard)

def account(chat_id):
    send_message(chat_id,"حسابك مسجل في البوت ✅")

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = request.json

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text","")

        if text == "/start":
            start(chat_id)
        else:
            send_message(chat_id,"تم استلام رسالتك")

    if "callback_query" in update:
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        data = update["callback_query"]["data"]

        if data == "account":
            account(chat_id)

        if data == "buy_number":
            send_message(chat_id,"ميزة شراء الأرقام سيتم ربطها مع API المواقع")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request
import telebot
import os

app = Flask(__name__)

# هان حط التوكن الجديد بتاعك
TOKEN = "هان_حط_التوكن_الجديد"
bot = telebot.TeleBot(TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return 'OK', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! البوت شغال ✅")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    app.run()
