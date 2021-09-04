from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


#buttonlar
START_BUTTONS= InlineKeyboardMarkup(
       [[
        InlineKeyboardButton('📋 Qoʻllanma', callback_data='qullanma')
        ]]
    )
    
QULLANMA_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📕 PDF qanday yaratiladi?', callback_data='pdf')
        ],[
       InlineKeyboardButton('✍🏻 PDF nomi qanday oʻzgartiriladi?', callback_data='pdf_r')
        ],[
     InlineKeyboardButton('Orqaga', callback_data='bosh')
        ]]
    )
     
BACK_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Orqaga', callback_data='back')

        ]]
     )

DEV_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📞 Bogʻlanish', url='https: //t.me/LiderBoy')

        ]]
     )
DEL_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🗑', callback_data="del")
    
    
        ]])