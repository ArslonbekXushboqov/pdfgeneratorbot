import os
import telebot
from PIL import Image
import shutil
from time import sleep
import sqlite3 as sql
from config import dbfile, admin, logs_channel, token
from buttons import *

with sql.connect(dbfile) as con:
    cur=con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER,
        name TEXT
    )""")

    con.commit()

def insert(userid, name):
    con= sql.connect(dbfile)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?",(userid,))

    if cur.fetchone() is None:

        cur.execute("INSERT INTO users(id,name)VALUES(?,?)",(userid,name))
        con.commit()

bot = telebot.TeleBot(token, parse_mode="markdown")

@bot.message_handler(commands=["start"])
def start(message):
	try:
		bot.send_chat_action(message.chat.id, "typing")
		u_name = message.from_user.first_name
		user_id = message.chat.id
		insert(user_id, u_name)
		msg = f"Salom [{message.from_user.first_name}](tg://user?id={message.chat.id})!\n\nMen sizga bir nechta rasmlardan PDF fayllarni yaratishga yordam beraman (PDF nomini ham oʻzingiz tanlaysiz)\n\n*Baʼtafsil *👇🏻"
		bot.send_message(message.chat.id, msg, reply_markup=START_BUTTONS)
	except Exception as ex:
		print(ex)
		
@bot.callback_query_handler(func=lambda call: call.data)
def callbacks(call):
	edit = call.data
	if edit == "del":
	           try:
	               for i in range(2):
	               	bot.delete_message(call.message.chat.id, call.message.message_id-i)
	           except:
	           	pass
	elif edit == 'qullanma':
		msg = f'Qanday yordam kerak? 🤓'
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = msg, reply_markup=QULLANMA_BUTTONS)
	elif edit == 'pdf':
		pdf = f"Kerakli rasmlarni yuklab boʻlganingizdan soʻng bajaradigan amalingiz:\n\nBotga */generate* buyrugʻini yuboring.\nBot sizga oʻzingizning ismingiz bilan nomlangan pdf faylni yuboradi.\nAgar boshqa nom qoʻymoqchi boʻlsangiz \n*/generate nimadir (/generate <fayl uchun nom>)* shu tarzda yuboring.\n\nMasalan mana bunday 👇🏻[­](https://telegra.ph/file/49b4f2b195dd0d5287cc3.jpg)"
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = pdf, reply_markup=BACK_BUTTONS)
	elif edit == 'pdf_r':
		pdf_r_msg = "Pdf faylni nomini oʻzgartirish uchun quyidagicha boʻladi:\nBotga kerakli rasmlarni yuklab boʻlganingizdan soʻng */generate nimadir (/generate <fayl uchun nom>)* shu tarzida yuborasiz.\n\nYoki \n*/generate id tarzida yuboring(Bunda fayl sizning telegram ID raqamingiz bilan nomlanadi.)* Masalan mana bunday 👇🏻[­](https://telegra.ph/file/3b5f24881807b40074726.jpg)"
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=pdf_r_msg, reply_markup=BACK_BUTTONS)
	elif edit == 'back':
		back_msg = f'Qanday yordam kerak? 🤓'
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = back_msg, reply_markup=QULLANMA_BUTTONS)
	elif edit == 'bosh':
		bosh_msg = 'Assalomu alaykum!\n\nMen sizga bir nechta rasmlardan PDF fayllarni yaratishga yordam beraman (PDF nomini ham oʻzingiz tanlaysiz)\n\n*Baʼtafsil *👇🏻'
		bot.edit_message_text(bosh_msg, call.message.chat.id, call.message.message_id, reply_markup=START_BUTTONS)
@bot.message_handler(commands=["id"])
def UsrId(message):
	bot.send_chat_action(message.chat.id, "typing")
	bot.send_message(message.chat.id, f'Sizning ID - `{message.chat.id}`')

@bot.message_handler(commands=["developer"])
def dev(message):
	bot.send_chat_action(message.chat.id, "typing")
	dev_msg = f"*Arslonbek Xushboqov (@LiderBoy)*\n\n_15 y.o Telegram Bot developer from  Kashkadarya 👨🏻‍💻_"
	bot.send_message(message.chat.id, dev_msg, reply_markup=DEV_BUTTONS)
	
PDF = {}
	
@bot.message_handler(content_types=['photo'])
def pic(message):
	picMsgId = bot.reply_to(message, "Rasm yuklanmoqda ⏳")
	
	if not isinstance(PDF.get(message.chat.id), list):
		PDF[message.chat.id] = []
	file_info = bot.get_file(message.photo[-1].file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	try:
		os.makedirs(f'./{message.chat.id}/imgs')
	except:
		pass
	with open(f'./{message.chat.id}/imgs/{message.chat.id}.jpg', 'wb') as new_file:
		new_file.write(downloaded_file)
	img = Image.open(f'./{message.chat.id}/imgs/{message.chat.id}.jpg').convert("RGB")
	PDF[message.chat.id].append(img)
	bot.edit_message_text(chat_id= message.chat.id, text = f"PDF ga  *{len(PDF[message.chat.id])}* ta sahifa qoʻshildi 🤓\n\nPDF yaratilishi uchun */generate* ni yuboring.\nAmalni bekor qilish uchun */cancel* ni yuboring.", message_id = picMsgId.message_id)
	
@bot.message_handler(commands=["cancel"])
def delQueue(message):
	try:
		shutil.rmtree(f'./{message.chat.id}')
		del PDF[message.chat.id]
	except:
	  pass
	finally:
		bot.reply_to(message, "Bekor qilindi❗️")

@bot.message_handler(commands=["generate"])
def generate(message):
	newName = message.text.replace('/generate', '')
	images = PDF.get(message.chat.id)
	if isinstance(images, list):
		pgnmbr = len(PDF[message.chat.id])
		del PDF[message.chat.id]
	if not images:
		ntFnded = bot.reply_to(message, "Pdf yaratish uchun rasm mavjud emas ⚠️")
		bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
		sleep(2)
		bot.delete_message(chat_id = message.chat.id, message_id = ntFnded.message_id)
		return
	gnrtMsgId = bot.send_message(message.chat.id, f'Biroz kuting...')
	if newName == f" id":
		fileName = f"{message.chat.id}" + ".pdf"
	elif len(newName) > 0 and len(newName) <= 25:
		fileName = f"{newName}" + ".pdf"
	elif len(newName) > 25:
		fileName = f"{message.chat.id}" + ".pdf"
	else:
		fileName = f"{message.from_user.first_name}" + ".pdf"
	path = os.path.join(f'./{message.chat.id}', fileName)
	images[0].save(path, save_all=True, append_images=images[1:])
	bot.edit_message_text(chat_id= message.chat.id, text = f'Yaratilmoqda 💚', message_id = gnrtMsgId.message_id)
	sendfile = open(path,'rb')
	bot.send_document(message.chat.id, sendfile, caption = f'📕 PDF nomi: *{fileName}*\n\n📄 Sahifalar soni: *{pgnmbr}* ta')
	shutil.rmtree(f'./{message.chat.id}')
	bot.edit_message_text(chat_id= message.chat.id, text = f'Muvaffaqiyatli yaratildi ✅', message_id = gnrtMsgId.message_id)
	bot.send_document(logs_channel, sendfile, caption = f'🥸 Yaratuvchi:  [{message.from_user.first_name}](tg://user?id={message.chat.id})\n\n📕 PDF nomi: *{fileName}*\n\n📄 Sahifalar soni: *{pgnmbr}* ta')
	
@bot.message_handler(content_types=['audio', 'document','gif', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def unsuprtd(message):
	bot.send_chat_action(message.chat.id, "typing")
	unSuprtd = bot.send_message(message.chat.id, f'Fayl turi qoʻllab quvvatlanmaydi ⚠️!')
	sleep(2)
	bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
	bot.delete_message(chat_id = message.chat.id, message_id = unSuprtd.message_id)
	
bot.polling()
