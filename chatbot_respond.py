import pandas as pd
import datetime
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,  MessageHandler, Filters, RegexHandler, ConversationHandler

SET_VALUE = range(1)

def modify(user_id, cap = 200, ben = 300, debt = 100, per = 5, pbr = 1, roic = 5, roe = 5, bps = 1, eps = 5, interest = 5):
    if user_id in userdata['User_id'].values:
        userdata.loc[userdata.User_id == user_id, '자본유보율'] = cap
        userdata.loc[userdata.User_id == user_id, '연매출'] = ben
        userdata.loc[userdata.User_id == user_id, '부채비율'] = debt
        userdata.loc[userdata.User_id == user_id, 'PER'] = per
        userdata.loc[userdata.User_id == user_id, 'PBR'] = pbr
        userdata.loc[userdata.User_id == user_id, 'ROIC'] = roic
        userdata.loc[userdata.User_id == user_id, 'ROE'] = roe
        userdata.loc[userdata.User_id == user_id, 'EPS'] = eps
        userdata.loc[userdata.User_id == user_id, '수익률'] = interest
    else:
        print('please add account')

    return userdata



#chatvbot commands

def start_command(bot, update):
    print("start")
    update.message.reply_text("주식 투자 보조용 챗봇입니다.\n'/join' 혹은 '/시작'을 입력하시면 정보를 등록합니다.")

def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def start_command(bot, update):
    print("start")
    update.message.reply_text("주식 투자 보조용 챗봇입니다.\n'/join' 혹은 '/시작'을 입력하시면 정보를 등록합니다.")

def set(bot, update):
    keyboard = [[InlineKeyboardButton("자본유보율", callback_data="자본유보율"), InlineKeyboardButton("연매출", callback_data="연매출"),
                 InlineKeyboardButton("부채비율", callback_data="부채비율")],
                [InlineKeyboardButton("PER", callback_data="PER"), InlineKeyboardButton("PBR", callback_data="PBR"),
                 InlineKeyboardButton("ROIC", callback_data="ROIC")],
                [InlineKeyboardButton("ROE", callback_data="ROE"), InlineKeyboardButton("EPS", callback_data="EPS")],
                [InlineKeyboardButton("매수적정가", callback_data="매수적정가"),
                 InlineKeyboardButton("매도적정가", callback_data="매도적정가")],
                [InlineKeyboardButton("cancel", callback_data="cancel")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('수정하고자 하는 항목을 선택해주세요:', reply_markup=reply_markup)

def set_value(bot, update):
    print("callback")
    cb = update.callback_query.data
    print(cb)

    if cb == 'cancel':
        bot.edit_message_text(text="취소하였습니다.", chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id)
        print(update.callback_query.message.chat_id, update.callback_query.message.message_id)

        return

    if cb != 'cancel':
        print(cb)

    '''
    if cb in userdata.columns:
        bot.edit_message_text(text="{select}이(가) 선택되었습니다. {select}의 현재 설정값은 {num}입니다.".format(select=cb, num=100),
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
    else:
        bot.edit_message_text(text="잘못된 입력입니다.", chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
    '''


'''
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('set', set)],

    states={
        SET_VALUE: [RegexHandler('^(자본유보율|연매출|부채비율|PER|PBR|ROIC|ROE|EPS|매수적정가|매도적정가)$', set_value)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
'''

def main():
    userdata = pd.read_csv('user_db_test.csv')
    del userdata['Unnamed: 0']

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')

    my_token = '492877807:AAEcHwvVyI8Sc9Bj31izc_cBanq0v4BZq24'
    bot = telegram.Bot(token = my_token)   #bot을 선언합니다.

    update = Updater(my_token)
    updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.
    dp = update.dispatcher

    print('chatbot is ready')
    start_handler = CommandHandler('start', start_command)
    config_handler = CommandHandler('set', set)
    dp.add_handler(config_handler)
    dp.add_handler(start_handler)
    dp.add_handler(CallbackQueryHandler(set_value))
    #dp.add_handler(conv_handler)

    update.start_polling()
    update.idle()

if __name__ == '__main__':
    main()