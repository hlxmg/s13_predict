import s13_predict
import s12_predict
from collections import Counter
from tqdm import tqdm

team_list = ['JDG', 'BLG', 'LNG', 'WBG', 'GEN', 'T1', 'KT', 'DK', 'WK1', 'WK2', 'WK3', 'Wk4', 'WK5', 'Wk6', 'WK7', 'WK8']
def cal_baqiang():
    baqiang12 = []
    baqiang13 = []
    cnt = 10000
    for i in tqdm(range(cnt)):
        a12 = s12_predict.predict(print_log=False, return_baqiang=True)
        baqiang12.extend(a12)
        a13 = s13_predict.predict(print_log=False, return_baqiang=True)
        baqiang13.extend(a13)
    result12 = Counter(baqiang12)
    result13 = Counter(baqiang13)
    for team in team_list:
        print('{}在s12八强概率为{:.2f}%，在s13八强的概率为{:.2f}%'.format(team, result12[team] / cnt * 100, result13[team] / cnt * 100))

def cal_guanjun():
    c12 = []
    c13 = []
    cnt = 100000
    for i in tqdm(range(cnt)):
        a12 = s12_predict.predict(print_log=False)
        c12.append(a12)
        a13 = s13_predict.predict(print_log=False)
        c13.append(a13)
    result12 = Counter(c12)
    result13 = Counter(c13)
    for team in team_list:
        print('{}在s12夺冠概率为{:.2f}%，在s13夺冠概率为{:.2f}%'.format(team, result12[team]/cnt*100, result13[team]/cnt*100))

def cal_all():
    c12 = []
    c13 = []
    baqiang12 = []
    baqiang13 = []
    bz = 0
    cnt = 10000
    for i in tqdm(range(cnt)):
        a12 = s12_predict.predict(print_log=False, return_baqiang=False, baozhong=bz)
        c12.append(a12)
        a13 = s13_predict.predict(print_log=False, return_baqiang=False, baozhong=bz)
        c13.append(a13)
        a12 = s12_predict.predict(print_log=False, return_baqiang=True, baozhong=bz)
        baqiang12.extend(a12)
        a13 = s13_predict.predict(print_log=False, return_baqiang=True, baozhong=bz)
        baqiang13.extend(a13)
    result12 = Counter(c12)
    result13 = Counter(c13)
    result121 = Counter(baqiang12)
    result131 = Counter(baqiang13)
    for team in team_list:
        print('{}在s12进八强概率为{:.2f}%，在s13进八强概率为{:.2f}%，在s12夺冠概率为{:.2f}%，在s13夺冠概率为{:.2f}%'
              .format(team, result121[team]/cnt*100, result131[team]/cnt*100, result12[team]/cnt*100, result13[team]/cnt*100))

def predict():
    s13_predict.predict(print_log=True)

# cal_baqiang()
#cal_guanjun()
# predict()
cal_all()