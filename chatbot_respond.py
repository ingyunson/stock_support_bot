import pandas as pd
import datetime
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,  MessageHandler, Filters, RegexHandler, ConversationHandler

SET_VALUE, INPUT_VALUE = range(2)

userdata = pd.read_csv('user_db_test.csv')
del userdata['Unnamed: 0']

def default(user_id, cap = 500, ben = 400, debt = 200, per = 10, pbr = 1, roic = 8, roe = 5, bps = 1, eps = 10, buy = 5, sell = 20):
    userdata.loc[userdata.User_id == user_id, '자본유보율'] = cap
    userdata.loc[userdata.User_id == user_id, '연매출'] = ben
    userdata.loc[userdata.User_id == user_id, '부채비율'] = debt
    userdata.loc[userdata.User_id == user_id, 'PER'] = per
    userdata.loc[userdata.User_id == user_id, 'PBR'] = pbr
    userdata.loc[userdata.User_id == user_id, 'ROIC'] = roic
    userdata.loc[userdata.User_id == user_id, 'ROE'] = roe
    userdata.loc[userdata.User_id == user_id, 'BPS'] = bps
    userdata.loc[userdata.User_id == user_id, 'EPS'] = eps
    userdata.loc[userdata.User_id == user_id, '매수적정가'] = buy
    userdata.loc[userdata.User_id == user_id, '매도적정가'] = sell
    userdata.to_csv('user_db_test.csv')

    return ConversationHandler.END


#chatbot reply
'''
def get_message(bot, update):
    print('notice message')
    notice = '현재 사용할 수 있는 명령은 다음과 같습니다.\n\n/set : 사용자의 주식 알림 설정을 수정'
    update.message.reply_text(notice)
'''

#chatvbot conversation


def set(bot, update):
    keyboard =[['자본유보율', '연매출', '부채비율'],
               ['PER', 'PBR', 'ROIC'],
               ['ROE', 'BPS', 'EPS'],
               ['매수적정가', '매도적정가'],
               ['기본 설정으로 되돌리기']]
    print('keyboard ok')
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard = True)
    user_id = update.message.from_user.id
    name = update.message.from_user.last_name + update.message.from_user.first_name
    print('db ready')
    cap = userdata.loc[userdata.User_id == user_id, '자본유보율'].values[0]
    ben = userdata.loc[userdata.User_id == user_id, '연매출'].values[0]
    debt = userdata.loc[userdata.User_id == user_id, '부채비율'].values[0]
    per = userdata.loc[userdata.User_id == user_id, 'PER'].values[0]
    pbr = userdata.loc[userdata.User_id == user_id, 'PBR'].values[0]
    roic = userdata.loc[userdata.User_id == user_id, 'ROIC'].values[0]
    roe = userdata.loc[userdata.User_id == user_id, 'ROE'].values[0]
    bps = userdata.loc[userdata.User_id == user_id, 'BPS'].values[0]
    eps = userdata.loc[userdata.User_id == user_id, 'EPS'].values[0]
    buy = userdata.loc[userdata.User_id == user_id, '매수적정가'].values[0]
    sell = userdata.loc[userdata.User_id == user_id, '매도적정가'].values[0]
    print('data get ok')

    set_message = '현재 {name} 님의 설정은 다음과 같습니다.\n취소를 원하시면 /cancel을 입력해주세요\n\n자본유보율 = {cap}\n연매출 = {ben}억 이상\n부채비율 = {debt}% 미만\nPER = {per}\nPBR = {pbr}\nROIC = {roic}\nROE = {roe}\nBPS = {bps}\nEPS = {eps}\n매수적정가 = {buy}%\n매도적정가 = {sell}%'.format(name = name, cap = cap, ben = ben, debt = debt, per = per, pbr = pbr, roic = roic, roe = roe, bps = bps, eps = eps, buy = buy, sell = sell)
    print('message ok')
    if user_id in userdata['User_id'].values:
        update.message.reply_text(set_message, reply_markup=reply_markup)

        return SET_VALUE

    else:
        update.message.reply_text('등록되어 있지 않은 사용자입니다. 사용자를 등록해주세요.')

        return ConversationHandler.END


def cancel(bot, update):
    print('cancel')
    reply_markup = telegram.ReplyKeyboardRemove()
    update.message.reply_text('이용해주셔서 감사합니다.', reply_markup=reply_markup)

    return ConversationHandler.END

def set_value(bot, update):
    text = update.message.text
    user_id = update.message.from_user.id
    if text == '기본 설정으로 되돌리기':
        update.message.reply_text('기본 설정으로 되돌립니다.')
        default(user_id)

        return ConversationHandler.END
    else:
        global select
        select = text
        user_id = update.message.from_user.id
        value = userdata.loc[userdata.User_id == user_id, select].values[0]
        reply_markup = telegram.ReplyKeyboardRemove()
        update.message.reply_text("선택하신 항목은 '{select}'입니다.\n현재 값은 {value}입니다.\n변경을 원하는 수치를 입력해주세요.".format(select=text, value=value), reply_markup=reply_markup)

        return INPUT_VALUE


def input_value(bot, update):
    change_num = update.message.text
    user_id = update.message.from_user.id
    update.message.reply_text("'{select}'의 수치를 {value}로 변경 완료했습니다. 감사합니다.".format(select = select, value = change_num))
    userdata.loc[userdata.User_id == user_id, select] = change_num
    userdata.to_csv('user_db_test.csv')

    return ConversationHandler.END


def main():


    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')

    my_token = '492877807:AAEcHwvVyI8Sc9Bj31izc_cBanq0v4BZq24'
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

    #message_handler = MessageHandler(Filters.text, get_message)
    #update.dispatcher.add_handler(message_handler)

    dp.add_handler(conv_handler)
    update.start_polling()
    update.idle()

if __name__ == '__main__':
    main()