import os
import requests
import telebot
from flask import Flask, request

# আপনার তথ্যসমূহ
TOKEN = "8946958697:AAFl-TWsgySSP2787ohoFabxzLCkOTtyuVw" 
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# শর্টনার সাইট কনফিগারেশন (ক্রমানুযায়ী)
SITES = [
    {"name": "GPLinks", "url": "https://gplinks-lilac.vercel.app/api", "api": "akash19888"},
    {"name": "STLink Gold", "url": "https://stlink-gold.vercel.app/api", "api": "akash198"},
    {"name": "STLinks", "url": "https://stlinks.vercel.app/api", "api": "akash1988"}
]

def shorten_link(base_url, api_key, long_url):
    try:
        params = {'api': api_key, 'url': long_url, 'format': 'text'}
        response = requests.get(base_url, params=params, timeout=15)
        if response.status_code == 200 and response.text.startswith("http"):
            return response.text.strip()
        else:
            return None
    except:
        return None

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
    bot.reply_to(message, "স্বাগতম! আমাকে একটি বড় লিংক পাঠান, আমি সেটি ৩টি শর্টনারের ভেতর দিয়ে পাস করিয়ে ১টি ফাইনাল লিংক দেব।")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    original_url = message.text.strip()
    
    if not original_url.startswith("http"):
        bot.reply_to(message, "দয়া করে একটি সঠিক লিংক দিন (http:// বা https:// সহ)")
        return

    wait_msg = bot.reply_to(message, "🔗 লিংকটি ৩টি লেয়ারে ছোট করা হচ্ছে, দয়া করে অপেক্ষা করুন...")
    
    # চেইনিং প্রসেস শুরু
    current_url = original_url
    success = True
    
    for site in SITES:
        shortened = shorten_link(site['url'], site['api'], current_url)
        if shortened:
            current_url = shortened # আগের শর্ট লিংক এখন নতুন ইনপুট
        else:
            success = False
            error_site = site['name']
            break

    if success:
        final_text = f"✅ আপনার ফাইনাল শর্ট লিংক:\n\n{current_url}"
        bot.edit_message_text(final_text, message.chat.id, wait_msg.message_id)
    else:
        bot.edit_message_text(f"❌ দুঃখিত, {error_site} থেকে লিংক শর্ট করার সময় সমস্যা হয়েছে।", message.chat.id, wait_msg.message_id)

@app.route('/')
def index():
    return "Bot is running with Chaining system..."
