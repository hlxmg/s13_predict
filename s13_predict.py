import random
import numpy as np
import collections

#定义常量
experiment_cnt = 1
round_cnt = 3 #达到3胜晋级
#mu代表实力值，sigma代表稳定性，值越大越不稳定
jdg_mu = 98
jdg_sigma = 1
blg_mu = 95
blg_sigma = 3
lng_mu = 97
lng_sigma = 2.5
wbg_mu = 96
wbg_sigma = 3.5
gen_mu = 97
gen_sigma = 0.5
t1_mu = 96
t1_sigma = 3
kt_mu = 95
kt_sigma = 2.5
dk_mu = 94
dk_sigma = 3.5
waika_mu = 90
waika_sigma = 4
team_list = ['JDG', 'BLG', 'LNG', 'WBG', 'GEN', 'T1', 'KT', 'DK', 'WK1', 'WK2', 'WK3', 'Wk4', 'WK5', 'Wk6', 'WK7', 'WK8']

#创建队伍
class team():
    global jdg_mu, jdg_sigma, blg_mu, blg_sigma, lng_mu, lng_sigma, wbg_mu, wbg_sigma, gen_mu, gen_sigma, t1_mu, t1_sigma, kt_mu, kt_sigma, dk_mu, dk_sigma
    def __init__(self):
        global dk_mu
        self.jdg = random.gauss(jdg_mu,jdg_sigma)
        self.lng = random.gauss(lng_mu,lng_sigma)
        self.blg = random.gauss(blg_mu, blg_sigma)
        self.wbg = random.gauss(wbg_mu, wbg_sigma)
        self.gen = random.gauss(gen_mu, gen_sigma)
        self.t1 = random.gauss(t1_mu, t1_sigma)
        self.kt = random.gauss(kt_mu, kt_sigma)
        self.dk = random.gauss(dk_mu, dk_sigma)
        self.waika = random.gauss(waika_mu, waika_sigma)

def get_scores(baozhong):
    global dk_mu
    JDG, GEN, BLG, T1, LNG, KT, WBG, DK, WK1, WK2, WK3, Wk4, WK5, Wk6, WK7, WK8 = \
        team().jdg, team().gen, team().blg, team().t1, team().lng, team().kt, team().wbg, team().dk, \
            team().waika, team().waika, team().waika, team().waika, team().waika, team().waika, team().waika, team().waika
    dk_mu += baozhong
    return [JDG, BLG, LNG, WBG, GEN, T1, KT, DK, WK1, WK2, WK3, Wk4, WK5, Wk6, WK7, WK8]

def print_pool(pools):
    #team_list = ['JDG', 'BLG', 'LNG', 'WBG', 'GEN', 'T1', 'KT', 'DK', 'WK1', 'WK2', 'WK3', 'Wk4', 'WK5', 'Wk6', 'WK7', 'WK8']
    for i in range(round_cnt):
        print('{}胜{}负晋级淘汰赛队伍有'.format(round_cnt, i), end='')
        print(','.join(team_list[i] for i in pools[round_cnt][i]))

def predict(print_log=True, return_baqiang=False, baozhong=0):
    global dk_mu
    dk_mu = 94
    for i in range(experiment_cnt):
        # print('This is {}st experiment!!!'.format(i+1))
        # print('JDG:{:.3f},GEN:{:.3f},BLG:{:.3f},T1:{:.3f},LNG:{:.3f},KT:{:.3f},WBG:{:.3f},DK:{:.3f},waika:{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}'
        #       .format(JDG, GEN, BLG, T1, LNG, KT, WBG, DK, WK1, WK2, WK3, Wk4, WK5, Wk6, WK7, WK8))

        pools = [[[] for _ in range(round_cnt+1)] for __ in range(round_cnt+1)] #胜败达到3即晋级或淘汰
        sign = [[0]*(round_cnt+1) for _ in range(round_cnt+1)]
        pools[0][0] = list(range(16)) #共16支队伍

        next_round = collections.deque([(0, 0)])
        while next_round:
            w, l = next_round.popleft()
            if w == round_cnt or l == round_cnt:
                continue
            n = len(pools[w][l])
            if print_log:
                print('{}胜{}败池子里有{}个战队'.format(w,l,n), list(team_list[t] for t in pools[w][l]))
            #抽签
            flag = False
            while not flag:
                flag = True
                sample1 = random.sample(pools[w][l], n//2)
                sample2 = [i for i in pools[w][l] if i not in sample1]
                for a, b in zip(sample1, sample2):
                    if w==0 and l==0 and ((0 <= a <= 3 and 0 <= b <= 3) or (4 <= a <= 7 and 4 <= b <= 7)):
                        flag = False
                        break
            if print_log:
                print('{}胜{}负池子抽签结果'.format(w,l), list(team_list[t] for t in sample1), list(team_list[t] for t in sample2))

            #当天比赛状态及结果
            scores = get_scores(baozhong)

            for a,b in zip(sample1, sample2):
                if scores[a] > scores[b]:
                    pools[w+1][l].append(a)
                    pools[w][l+1].append(b)
                else:
                    pools[w+1][l].append(b)
                    pools[w][l+1].append(a)
            # 不需要重复计算
            if sign[w+1][l] == 0:
                next_round.append((w+1,l))
            if sign[w][l+1] == 0:
                next_round.append((w,l+1))
            sign[w+1][l] = 1
            sign[w][l+1] = 1

        # 池子情况
        if print_log:
            print_pool(pools)

        #八强抽签
        sample1 = []
        sample2 = []
        sample1.extend(pools[3][0])
        sample1.extend(pools[3][1][:2])
        sample2.extend(pools[3][2])
        sample2.append(pools[3][1][2])
        random.shuffle(sample1)
        random.shuffle(sample2)
        baqiang = []
        baqiang.extend(sample1)
        baqiang.extend(sample2)
        if return_baqiang:
            return [team_list[i] for i in baqiang]
        #print(sample1, sample2)
        if print_log:
            print('八强抽签结果是', end='\n')
            print(','.join(team_list[i] for i in sample1))
            print(','.join(team_list[i] for i in sample2))

        # 八强赛
        scores = get_scores(baozhong)

        siqiang1 = []
        siqiang2 = []
        for i in range(4):
            if i <= 1:
                if scores[sample1[i]] > scores[sample2[i]]:
                    siqiang1.append(sample1[i])
                else:
                    siqiang1.append(sample2[i])
            else:
                if scores[sample1[i]] > scores[sample2[i]]:
                    siqiang2.append(sample1[i])
                else:
                    siqiang2.append(sample2[i])

        if print_log:
            print('晋级四强的队伍是', end='')
            print(','.join(team_list[i] for i in siqiang1+siqiang2))


        #四强赛
        zongjuesai = []
        scores = get_scores(baozhong)

        if scores[siqiang1[0]] > scores[siqiang1[1]]:
            zongjuesai.append(siqiang1[0])
        else:
            zongjuesai.append(siqiang1[1])
        if scores[siqiang2[0]] > scores[siqiang2[1]]:
            zongjuesai.append(siqiang2[0])
        else:
            zongjuesai.append(siqiang2[1])
        if print_log:
            print('晋级总决赛的队伍是',end='')
            print(','.join(team_list[i] for i in zongjuesai))

        #总决赛
        scores = get_scores(baozhong)
        #print('dk实力为', dk_mu)
        if print_log:
            print('获得S13总冠军的队伍是', end='')
        if scores[zongjuesai[0]] > scores[zongjuesai[1]]:
            if print_log:
                print(team_list[zongjuesai[0]])
            return team_list[zongjuesai[0]]
        else:
            if print_log:
                print(team_list[zongjuesai[1]])
            return team_list[zongjuesai[1]]