import pandas as pd
import datetime
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


MESSAGE = range(1)

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


def config(bot, update):
    reply_keyboard = [['자본유보율', '연매출'], ['부채비율', 'PER'], ['ROIC', 'ROE'], ['BPS', 'EPS'], ['매수 마진', '매도 마진']['최초설정으로', '중단']]

    update.message.reply_text('이 명령은 설정을 변경하는 명령입니다.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MESSAGE


def message(bot, update):
    user = update.message.from_user
    update.message.reply_text('ㅇㅇㅇ 명령을 수정합니다.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END



def main():
    userdata = pd.read_csv('user_db_test.csv')
    del userdata['Unnamed: 0']

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')

    my_token = '729504243:AAFQEqyGx_yjOkSEBoNCUToP2KLH0VR-WX4'
    bot = telegram.Bot(token = my_token)   #bot을 선언합니다.

    update = Updater(my_token)
    updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.
    dp = update.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('config', config)],

        states={
            MESSAGE: [RegexHandler('자본유보율', '연매출', '부채비율', 'PER', 'ROIC', 'ROE', 'BPS', 'EPS', '목표수익률', message)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    print('chatbot is ready')
    start_handler = CommandHandler('start', start_command)
    dp.add_handler(start_handler)
    dp.add_handler(conv_handler)

    update.start_polling()
    update.idle()




    print('chatbot is ready')
    start_handler = CommandHandler('start', start_command)
    updater.dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()