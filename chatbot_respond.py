import pandas as pd
import datetime
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,  MessageHandler, Filters, RegexHandler, ConversationHandler

SET_VALUE, INPUT_VALUE = range(2)

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


def set(bot, update):
    keyboard =[['자본유보율', '연매출', '부채비율'],
               ['PER', 'PBR', 'ROIC'],
               ['ROE', 'EPS'],
               ['매수적정가', '매도적정가'],
               ['기본 설정으로 되돌리기']]

    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard = True)
    update.message.reply_text('수정하고자 하는 항목을 선택해주세요', reply_markup=reply_markup)

    return SET_VALUE

def cancel(bot, update):
    print('cancel')
    reply_markup = telegram.ReplyKeyboardRemove()
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=reply_markup)

    return ConversationHandler.END

def set_value(bot, update):
    text = update.message.text
    global select
    select = text
    reply_markup = telegram.ReplyKeyboardRemove()
    update.message.reply_text("선택하신 항목은 '{select}'입니다.\n현재 값은 {value}입니다.\n변경을 원하는 수치를 입력해주세요.".format(select=text, value=10), reply_markup=reply_markup)

    return INPUT_VALUE

def input_value(bot, update):
    text = update.message.text
    update.message.reply_text("'{select}'의 수치를 {value}로 변경 완료했습니다. 감사합니다.".format(select = select, value = text))

    return ConversationHandler.END


def main():
    userdata = pd.read_csv('user_db_test.csv')
    del userdata['Unnamed: 0']

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')

    my_token = <TOKEN>
    bot = telegram.Bot(token = my_token)   #bot을 선언합니다.

    update = Updater(my_token)
    updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.
    dp = update.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('set', set)],

        states={
            SET_VALUE: [RegexHandler('^(자본유보율|연매출|부채비율|PER|PBR|ROIC|ROE|EPS|매수적정가|매도적정가|기본 설정으로 되돌리기)$', set_value)],
            INPUT_VALUE: [MessageHandler(Filters.text, input_value)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    print('chatbot is ready')

    dp.add_handler(conv_handler)
    update.start_polling()
    update.idle()

if __name__ == '__main__':
    main()