import random
import numpy as np
import collections

#定义常量
experiment_cnt = 1
round_cnt = 3
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
        # self.shili = random.gauss(mu, sigma)
        self.jdg = random.gauss(jdg_mu,jdg_sigma)
        self.lng = random.gauss(lng_mu,lng_sigma)
        self.blg = random.gauss(blg_mu, blg_sigma)
        self.wbg = random.gauss(wbg_mu, wbg_sigma)
        self.gen = random.gauss(gen_mu, gen_sigma)
        self.t1 = random.gauss(t1_mu, t1_sigma)
        self.kt = random.gauss(kt_mu, kt_sigma)
        self.dk = random.gauss(dk_mu, dk_sigma)
        self.waika = random.gauss(waika_mu, waika_sigma)

def print_pool(pools):
    #team_list = ['JDG', 'BLG', 'LNG', 'WBG', 'GEN', 'T1', 'KT', 'DK', 'WK1', 'WK2', 'WK3', 'Wk4', 'WK5', 'Wk6', 'WK7', 'WK8']
    for i in range(round_cnt):
        print('{}胜{}负晋级淘汰赛队伍有'.format(round_cnt, i), end='')
        print(','.join(team_list[i] for i in pools[round_cnt][i]))

def get_scores(baozhong):
    global dk_mu
    JDG, GEN, BLG, T1, LNG, KT, WBG, DK, WK1, WK2, WK3, Wk4, WK5, Wk6, WK7, WK8 = \
        team().jdg, team().gen, team().blg, team().t1, team().lng, team().kt, team().wbg, team().dk, \
            team().waika, team().waika, team().waika, team().waika, team().waika, team().waika, team().waika, team().waika
    dk_mu += baozhong
    return [JDG, BLG, LNG, WBG, GEN, T1, KT, DK, WK1, WK2, WK3, Wk4, WK5, Wk6, WK7, WK8]

def predict(print_log=True, return_baqiang=False, baozhong=0):
    global dk_mu
    dk_mu = 94
    for i in range(experiment_cnt):
        # print('This is {}st experiment!!!'.format(i+1))

        # print('JDG:{:.3f},GEN:{:.3f},BLG:{:.3f},T1:{:.3f},LNG:{:.3f},KT:{:.3f},WBG:{:.3f},DK:{:.3f},waika:{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}'
        #       .format(JDG, GEN, BLG, T1, LNG, KT, WBG, DK, WK1, WK2, WK3, Wk4, WK5, Wk6, WK7, WK8))

        win_cnt = [0]*16
        lose_cnt = [0]*16

        #抽签
        group = [[0, 8, 12],
                 [1, 9, 13],
                 [2, 10, 14],
                 [3, 11, 15]]
        lck = [4, 5, 6, 7]
        require = False
        while not require:
            require = True
            random.shuffle(lck)
            if any(lck[i]-group[i][0] == 4 for i in range(4)):
                require = False
        for i in range(4):
            group[i].append(lck[i])
            random.shuffle(group[i])
        if print_log:
            for i in range(4):
                print('第{}组的队伍有：{}'.format(i+1, ','.join(team_list[x] for x in group[i])))

        #排赛程
        scores = get_scores(baozhong)

        for i in range(4):
            a, b = group[i][0], group[i][1]
            if scores[a] > scores[b]:
                win_cnt[a] += 1
                lose_cnt[b] += 1
            else:
                win_cnt[b] += 1
                lose_cnt[a] += 1
            c, d = group[i][2], group[i][3]
            if scores[c] > scores[d]:
                win_cnt[c] += 1
                lose_cnt[d] += 1
            else:
                win_cnt[d] += 1
                lose_cnt[c] += 1

        scores = get_scores(baozhong)
        for i in range(4):
            a, b = group[i][0], group[i][2]
            if scores[a] > scores[b]:
                win_cnt[a] += 1
                lose_cnt[b] += 1
            else:
                win_cnt[b] += 1
                lose_cnt[a] += 1
            c, d = group[i][1], group[i][3]
            if scores[c] > scores[d]:
                win_cnt[c] += 1
                lose_cnt[d] += 1
            else:
                win_cnt[d] += 1
                lose_cnt[c] += 1

        scores = get_scores(baozhong)
        for i in range(4):
            a, b = group[i][0], group[i][3]
            if scores[a] > scores[b]:
                win_cnt[a] += 1
                lose_cnt[b] += 1
            else:
                win_cnt[b] += 1
                lose_cnt[a] += 1
            c, d = group[i][1], group[i][2]
            if scores[c] > scores[d]:
                win_cnt[c] += 1
                lose_cnt[d] += 1
            else:
                win_cnt[d] += 1
                lose_cnt[c] += 1

        scores = get_scores(baozhong)

        for i in range(4):
            a, b = group[i][0], group[i][1]
            if scores[a] > scores[b]:
                win_cnt[a] += 1
                lose_cnt[b] += 1
            else:
                win_cnt[b] += 1
                lose_cnt[a] += 1
            c, d = group[i][2], group[i][3]
            if scores[c] > scores[d]:
                win_cnt[c] += 1
                lose_cnt[d] += 1
            else:
                win_cnt[d] += 1
                lose_cnt[c] += 1

        scores = get_scores(baozhong)
        for i in range(4):
            a, b = group[i][0], group[i][2]
            if scores[a] > scores[b]:
                win_cnt[a] += 1
                lose_cnt[b] += 1
            else:
                win_cnt[b] += 1
                lose_cnt[a] += 1
            c, d = group[i][1], group[i][3]
            if scores[c] > scores[d]:
                win_cnt[c] += 1
                lose_cnt[d] += 1
            else:
                win_cnt[d] += 1
                lose_cnt[c] += 1

        scores = get_scores(baozhong)
        for i in range(4):
            a, b = group[i][0], group[i][3]
            if scores[a] > scores[b]:
                win_cnt[a] += 1
                lose_cnt[b] += 1
            else:
                win_cnt[b] += 1
                lose_cnt[a] += 1
            c, d = group[i][1], group[i][2]
            if scores[c] > scores[d]:
                win_cnt[c] += 1
                lose_cnt[d] += 1
            else:
                win_cnt[d] += 1
                lose_cnt[c] += 1

        #是否需要加赛
        scores = get_scores(baozhong)

        pool1 = []
        pool2 = []
        for i in range(4):
            #sorted(group[i], key=lambda x: -win_cnt[i])
            group[i].sort(key=lambda x: -win_cnt[x])
            win_cnt_sort = list(win_cnt[x] for x in group[i])
            if win_cnt_sort[0] == 6 and win_cnt_sort[1] == win_cnt_sort[2] and win_cnt_sort[1] == win_cnt_sort[3]:
                pool1.append(group[i][0])
                a, b, c = group[i][1], group[i][2], group[i][3]
                temp = sorted([a, b, c], key=lambda x: -scores[x])
                pool2.append(temp[0])
            elif win_cnt_sort[0] == 6 and win_cnt_sort[1] == win_cnt_sort[2]:
                pool1.append(group[i][0])
                a, b = group[i][1], group[i][2]
                temp = sorted([a, b], key=lambda x: -scores[x])
                pool2.append(temp[0])
            elif win_cnt_sort[0] == 5 and win_cnt_sort[1] == 5 or (win_cnt_sort[0] == 4 and win_cnt_sort[1] == 4 and win_cnt_sort[2] != 4):
                a, b = group[i][0], group[i][1]
                temp = sorted([a, b], key=lambda x: -scores[x])
                pool1.append(temp[0])
                pool2.append(temp[1])
            elif win_cnt_sort[0] == 4 and win_cnt_sort[1] == 4 and win_cnt_sort[2] == 4:
                pool1.append(group[i][0])
                a, b, c = group[i][0], group[i][1], group[i][2]
                temp = sorted([a,b,c], key=lambda x: -scores[x])
                pool1.append(temp[0])
                pool2.append(temp[1])
            elif win_cnt_sort[0] == 3 and win_cnt_sort[1] == 3 and win_cnt_sort[2] == 3 and win_cnt_sort[3] == 3:
                a, b, c, d = group[i]
                temp = sorted([a, b, c, d], key=lambda x: -scores[x])
                pool1.append(temp[0])
                pool2.append(temp[1])
            else:
                pool1.append(group[i][0])
                pool2.append(group[i][1])

        # 八强抽签，半区规避
        guibi = {}
        for i in range(4):
            guibi[pool1[i]] = pool2[i]
            guibi[pool2[i]] = pool1[i]
        pool20 = pool2[:]
        random.shuffle(pool1)
        random.shuffle(pool20)
        pool2 = [-1]*4
        for i in range(4):
            if i == 0 or i == 1:
                gb = guibi[pool20[i]]
                if pool1[0] == gb or pool1[1] == gb:
                    if pool2[2] != -1:
                        pool2[3] = pool20[i]
                    else:
                        pool2[2] = pool20[i]
                else:
                    if pool2[0] != -1:
                        pool2[1] = pool20[i]
                    else:
                        pool2[0] = pool20[i]
            else:
                gb = guibi[pool20[i]]
                if pool1[0] == gb or pool1[1] == gb:
                    if pool2[2] != -1:
                        pool2[3] = pool20[i]
                    else:
                        pool2[2] = pool20[i]
                else:
                    if pool2[0] != -1:
                        pool2[1] = pool20[i]
                    else:
                        pool2[0] = pool20[i]

        baqiang = []
        baqiang.extend(pool1)
        baqiang.extend(pool2)
        if return_baqiang:
            return [team_list[i] for i in baqiang]
        if print_log:
            print('八强抽签结果是', end='\n')
            print(','.join(team_list[i] for i in pool1))
            print(','.join(team_list[i] for i in pool2))

        sample1 = pool1[:]
        sample2 = pool2[:]

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
            print(','.join(team_list[i] for i in siqiang1 + siqiang2))

        # 四强赛
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
            print('晋级总决赛的队伍是', end='')
            print(','.join(team_list[i] for i in zongjuesai))

        # 总决赛
        scores = get_scores(baozhong)
        # print('dk实力为', dk_mu)
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








