import os
import requests
import telebot
from flask import Flask, request

# আপনার তথ্যসমূহ
TOKEN = "8946958697:AAFl-TWsgySSP2787ohoFabxzLCkOTtyuVw" # @BotFather থেকে পাওয়া টোকেন
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# শর্টনার সাইট কনফিগারেশন
SITES = [
    {"name": "GPLinks", "url": "https://gplinks-lilac.vercel.app/api", "api": "akash19888"},
    {"name": "STLink Gold", "url": "https://stlink-gold.vercel.app/api", "api": "akash198"},
    {"name": "STLinks", "url": "https://stlinks.vercel.app/api", "api": "akash1988"}
]

def shorten_link(base_url, api_key, long_url):
    try:
        # সাধারণত এই সাইটগুলো GET রিকোয়েস্ট গ্রহণ করে
        params = {'api': api_key, 'url': long_url, 'format': 'text'}
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "লিংক তৈরি করা যায়নি"
    except:
        return "সার্ভার এরর!"

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Invalid Request', 403

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আমাকে একটি বড় লিংক পাঠান, আমি ৩টি শর্টনার থেকে ছোট করে দেব।")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if not url.startswith("http"):
        bot.reply_to(message, "দয়া করে একটি সঠিক লিংক দিন (http:// বা https:// সহ)")
        return

    msg = bot.reply_to(message, "লিংক ছোট করা হচ্ছে, দয়া করে অপেক্ষা করুন...")
    
    result_text = "✅ আপনার শর্ট লিংকগুলো:\n\n"
    for site in SITES:
        short = shorten_link(site['url'], site['api'], url)
        result_text += f"🔗 {site['name']}: {short}\n"
    
    bot.edit_message_text(result_text, message.chat.id, msg.message_id)

@app.route('/')
def index():
    return "Bot is running..."
