import pandas as pd

userdata = pd.read_csv('user_db.csv')
del userdata['Unnamed: 0']


def add_user(id):
    default = [200, 200, 200, 10, 5, 10, 10, 10, 10, 10]
    user = pd.DataFrame(columns=('User_id', '자본유보율', '연매출', '부채비율', 'PER', 'PBR', 'ROIC', 'ROE', 'BPS', 'EPS', '수익률'))
    user_data = [id] + default
    df_user = pd.DataFrame([user_data],
                           columns=['User_id', '자본유보율', '연매출', '부채비율', 'PER', 'PBR', 'ROIC', 'ROE', 'BPS', 'EPS',
                                    '수익률'])
    user = userdata.append(df_user, ignore_index=True)
    user.to_csv('user_db.csv')

    return user