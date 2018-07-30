import copy
import random

# CodenamesCN.1.5+.txt文件所在目录
file_path = r'C:\Users\fanxu\Desktop\CodenamesCN.1.5+.txt'

# Version: 2.1
# 更新内容：
# 修复了关于检测线索是否违规机制的一个bug

def onQQMessage(bot, contact, member, content):
    if bot.isMe(contact, member):
        # 忽略自己的发言
        pass
    elif member is None:
        # 忽略私聊内容
        pass
    elif content == '-help':
        bot.SendTo(contact, '指令：\n'
                            '-start  开始游戏\n'
                            '-end    结束游戏\n'
                            '-list   显示玩家\n'
                            '-team   显示分组\n'
                            '-check  查看当前解题情况\n'
                            '-hint   查看当前线索及次数\n'
                            '-pass   放弃一次')
    # 暂时停用-stop指令
    # elif content == '-stop':
    #    bot.SendTo(contact, 'QQ机器人已关闭')
    #    bot.Stop()
    elif content == '-start':
        operator(bot, contact, member, content, 'startGame')
    elif content == '-end':
        operator(bot, contact, member, content, 'endGame')
    elif content == '-list':
        operator(bot, contact, member, content, 'showGamer')
    elif content == '-team':
        operator(bot, contact, member, content, 'showTeam')
    elif content == '-check':
        operator(bot, contact, member, content, 'showCard')
    elif content == '-hint':
        operator(bot, contact, member, content, 'showHint')
    elif content == '1':
        operator(bot, contact, member, content, 'addGamer')
    elif content == '0':
        operator(bot, contact, member, content, 'runGame')
    else:
        operator(bot, contact, member, content, 'handleMessage')


defaultTable = ['A'] * 9 + ['B'] * 8 + ['N'] * 7 + ['X']
defaultStatus = {'isStarted': False, 'isRunning': False, 'gamers': [], 'team A': [], 'team B': [], 'leader A': '',
                 'leader B': '', 'codes': [], 'table': defaultTable[:], 'confirmed': [], 'map': [], 'round': 'A',
                 'winner': '', 'hint A': ['', 0], 'hint B': ['', 0], 'characters': []}
with open(file_path, 'r') as f:
    codeList = f.read().split(',')
gameStatus = copy.deepcopy(defaultStatus)


# 初始化gameStatus
def initialize():
    global gameStatus
    gameStatus = copy.deepcopy(defaultStatus)


def operator(bot, contact, member, content, cmd):
    if cmd == 'startGame':
        if gameStatus['isStarted']:
            bot.SendTo(contact, '游戏已开始')
        else:
            bot.SendTo(contact, '游戏开始')
            gameStatus['isStarted'] = True
            bot.SendTo(contact, '回复“1”进行报名，回复“0”截止报名')
    elif cmd == 'endGame':
        if not gameStatus['isStarted']:
            bot.SendTo(contact, '游戏未开始，回复“-start”开始游戏')
        elif gameStatus['isRunning']:
            bot.SendTo(contact, '游戏结束')
            bot.SendTo(contact, drawMap())
            initialize()
        else:
            bot.SendTo(contact, '游戏结束')
            initialize()
    elif cmd == 'addGamer':
        if not gameStatus['isStarted']:
            bot.SendTo(contact, '游戏未开始，回复“-start”开始游戏')
        elif gameStatus['isRunning']:
            bot.SendTo(contact, '游戏进行中，无法报名')
        else:
            if member.name in gameStatus['gamers']:
                bot.SendTo(contact, '%s已报名' % member.name)
            else:
                gameStatus['gamers'].append(member.name)
                bot.SendTo(contact, '%s报名成功' % member.name)
    elif cmd == 'runGame':
        if not gameStatus['isStarted']:
            bot.SendTo(contact, '游戏未开始，回复“-start”开始游戏')
        elif gameStatus['isRunning']:
            bot.SendTo(contact, '游戏进行中')
        else:
            if len(gameStatus['gamers']) < 4:
                bot.SendTo(contact, '人数不足,已有%d人报名' % len(gameStatus['gamers']))
            elif len(gameStatus['gamers']) >= 4:
                bot.SendTo(contact, '报名结束，共%d人' % len(gameStatus['gamers']))
                buildTeam(bot, contact)
                gameStatus['isRunning'] = True
                firstRound(bot, contact)
    elif cmd == 'showTeam':
        if not gameStatus['isStarted']:
            bot.SendTo(contact, '游戏未开始，回复“-start”开始游戏')
        elif gameStatus['isRunning']:
            bot.SendTo(contact, gameStatus['leader A'] + 'A组：' + '、'.join(gameStatus['team A']) + '\n'
                       + gameStatus['leader B'] + 'B组：' + '、'.join(gameStatus['team B']))
        else:
            bot.SendTo(contact, '未分组')
    elif cmd == 'showGamer':
        if not gameStatus['isStarted']:
            bot.SendTo(contact, '游戏未开始，回复“-start”开始游戏')
        else:
            if gameStatus['gamers']:
                bot.SendTo(contact, '参与玩家：' + '、'.join(gameStatus['gamers']) + '，共%d人' % len(gameStatus['gamers']))
            else:
                bot.SendTo(contact, '无')
    elif cmd == 'handleMessage':
        if content == '':
            # 忽略图片信息
            pass
        elif gameStatus['isRunning']:
            if getRole(member) == 'other':
                # 忽略非玩家发言
                pass
            elif getRole(member) in ('leader A', 'leader B'):
                if content[-1].isnumeric() and not content.isnumeric():
                    # 若队长发言以数字结尾且非全数字，则将其识别为发布线索
                    operator(bot, contact, member, content, 'leaderIssue')
            elif getRole(member) in ('team A', 'team B'):
                if content[-2:] == '确认':
                    # 若队员发言以“确认”结尾，则将其识别为确认代号
                    operator(bot, contact, member, content, 'memberConfirm')
                elif content == '-pass':
                    # 若队员发言为“-pass”，则轮换回合
                    operator(bot, contact, member, content, 'passRound')
    elif cmd == 'leaderIssue':
        if getRole(member) == 'leader A' and gameStatus['round'] == 'A' and gameStatus['hint A'][1] == 0:
            pass
        elif getRole(member) == 'leader B' and gameStatus['round'] == 'B' and gameStatus['hint B'][1] == 0:
            pass
        else:
            # 可判负
            return
        clue = list(content)
        last = clue.pop()
        chance = ''
        while last.isnumeric():
            chance = last + chance
            last = clue.pop()
        if last != ' ':
            clue.append(last)
        clue = ''.join(clue)
        if isCharacterFoul(clue):
            bot.SendTo(contact, '%s队线索违规' % gameStatus['round'])
            # 可判负
            operator(bot, contact, member, content, 'endGame')
            return
        if gameStatus['round'] == 'A':
            gameStatus['hint A'] = [clue, (int(chance) + 1)]
            bot.SendTo(contact, 'A队线索：%s，剩余%d次' % tuple(gameStatus['hint A']))
        elif gameStatus['round'] == 'B':
            gameStatus['hint B'] = [clue, (int(chance) + 1)]
            bot.SendTo(contact, 'B队线索：%s，剩余%d次' % tuple(gameStatus['hint B']))
    elif cmd == 'memberConfirm':
        if getRole(member) == 'team A' and gameStatus['round'] == 'A' and gameStatus['hint A'][1] > 0:
            pass
        elif getRole(member) == 'team B' and gameStatus['round'] == 'B' and gameStatus['hint B'][1] > 0:
            pass
        else:
            # 可提醒
            return
        suppose = content[:-2].strip()
        if suppose in gameStatus['codes']:
            if suppose in gameStatus['confirmed']:
                bot.SendTo(contact, '该代号已公布，回复“-check”查看')
            else:
                gameStatus['confirmed'].append(suppose)
                # 从违规汉字列表中去除确认代号的汉字
                for character in suppose:
                    gameStatus['characters'].remove(character)
                bot.SendTo(contact, suppose + ' ' + gameStatus['table'][gameStatus['codes'].index(suppose)])
                if isGameOver():
                    bot.SendTo(contact, '%s队获胜' % gameStatus['winner'])
                    game(bot, contact, member, content, 'endGame')
                    return
                if gameStatus['round'] == 'A':
                    gameStatus['hint A'][1] += -1
                    if gameStatus['table'][gameStatus['codes'].index(suppose)] != 'A':
                        switchRound(bot, contact)
                    elif gameStatus['hint A'][1] == 0:
                        bot.SendTo(contact, '线索次数用完，请A队提供新线索')
                elif gameStatus['round'] == 'B':
                    gameStatus['hint B'][1] += -1
                    if gameStatus['table'][gameStatus['codes'].index(suppose)] != 'B':
                        switchRound(bot, contact)
                    elif gameStatus['hint B'][1] == 0:
                        bot.SendTo(contact, '线索次数用完，请B队提供新线索')
        else:
            bot.SendTo(contact, '该代号不存在')
    elif cmd == 'passRound':
        if getRole(member) == 'team A' and gameStatus['hint A'][1] > 0 and gameStatus['round'] == 'A':
            gameStatus['hint A'][1] += -1
            if gameStatus['hint A'][1] == 0:
                bot.SendTo(contact, '线索次数用完，请A队准备新线索')
            switchRound(bot, contact)
        elif getRole(member) == 'team B' and gameStatus['hint B'][1] > 0 and gameStatus['round'] == 'B':
            gameStatus['hint B'][1] += -1
            if gameStatus['hint B'][1] == 0:
                bot.SendTo(contact, '线索次数用完，请B队准备新线索')
            switchRound(bot, contact)
        else:
            # 可提醒
            pass
    elif cmd == 'showCard':
        bot.SendTo(contact, drawCard())
    elif cmd == 'showHint':
        hints = 'A队线索：%s，剩余%d次' % tuple(gameStatus['hint A']) + '\n' + \
                'B队线索：%s，剩余%d次' % tuple(gameStatus['hint B'])
        bot.SendTo(contact, hints)


# 回合轮换
def switchRound(bot, contact):
    bot.SendTo(contact, '对方回合开始')
    if gameStatus['round'] == 'A':
        gameStatus['round'] = 'B'
        if gameStatus['hint B'][1] > 0:
            bot.SendTo(contact, 'B队线索：%s，剩余%d次' % tuple(gameStatus['hint B']))
        else:
            bot.SendTo(contact, 'B队提供新线索')
    elif gameStatus['round'] == 'B':
        gameStatus['round'] = 'A'
        if gameStatus['hint A'][1] > 0:
            bot.SendTo(contact, 'A队线索：%s，剩余%d次' % tuple(gameStatus['hint A']))
        else:
            bot.SendTo(contact, 'A队提供新线索')


# 检查游戏是否结束
def isGameOver():
    a = b = 0
    for i in gameStatus['confirmed']:
        camp = gameStatus['table'][gameStatus['codes'].index(i)]
        if camp == 'X':
            # 可判负
            if gameStatus['round'] == 'A':
                gameStatus['winner'] = 'B'
            elif gameStatus['round'] == 'B':
                gameStatus['winner'] = 'A'
            return True
        elif camp == 'A':
            a += 1
        elif camp == 'B':
            b += 1
    if a == 9:
        gameStatus['winner'] = 'A'
        return True
    elif b == 8:
        gameStatus['winner'] = 'B'
        return True
    else:
        return False


# 识别线索是否包含违规汉字
def isCharacterFoul(clue):
    for character in clue:
        if character in gameStatus['characters']:
            return True
    return False


# 识别发言者身份
def getRole(member):
    name = member.name
    if name == gameStatus['leader A']:
        return 'leader A'
    elif name == gameStatus['leader B']:
        return 'leader B'
    elif name in gameStatus['team A']:
        return 'team A'
    elif name in gameStatus['team B']:
        return 'team B'
    else:
        return 'other'


# 第一回合开始
def firstRound(bot, contact):
    bot.SendTo(contact, '生成代号...')
    buildCodeMap()
    bot.SendTo(contact, '发送代号卡...')
    bot.SendTo(contact, drawCard())
    bot.SendTo(contact, '发送解题卡...')
    # 查找队长uin并私聊发送解题卡
    group = bot.List('group', '行动代码游戏群')[0]
    bot.Update(group)
    groupMember = bot.List(group)
    bot.Update('buddy')
    for i in groupMember:
        if i.name in (gameStatus['leader A'], gameStatus['leader B']):
            leader = bot.List('buddy', 'uin=%s' % i.uin)
            bot.SendTo(leader[0], drawMap())
    bot.SendTo(contact, '完毕')
    bot.SendTo(contact, 'A组先开始回合')


# 生成地图
def buildCodeMap():
    codes = random.sample(codeList, 25)
    random.shuffle(codes)
    gameStatus['codes'] = codes
    table = copy.deepcopy(defaultTable)
    random.shuffle(table)
    gameStatus['table'] = table
    map = zip(table, codes)
    gameStatus['map'] = map
    for code in codes:
        gameStatus['characters'] += list(code)


# 绘制解题卡
def drawMap():
    map = copy.deepcopy(gameStatus['map'])
    box = [' '.join(i).center(5) for i in map]
    msg = '-' * 31 + '\n' + \
          '|'.join(box[0:5]) + '\n' + \
          '-' * 31 + '\n' + \
          '|'.join(box[5:10]) + '\n' + \
          '-' * 31 + '\n' + \
          '|'.join(box[10:15]) + '\n' + \
          '-' * 31 + '\n' + \
          '|'.join(box[15:20]) + '\n' + \
          '-' * 31 + '\n' + \
          '|'.join(box[20:25]) + '\n' + \
          '-' * 31
    return msg


# 绘制代号卡
def drawCard():
    map = copy.deepcopy(gameStatus['map'])
    box = [i[1] for i in map]
    for c in range(25):
        if box[c] in gameStatus['confirmed']:
            box[c] = gameStatus['table'][c] + ' ' + box[c]
    box = [x.center(5) for x in box]
    msg = '-' * 31 + '\n' + \
          '|'.join(box[0:5]) + '\n' + \
          '-' * 31 + '\n' + \
          '|'.join(box[5:10]) + '\n' + \
          '-' * 31 + '\n' + \
          '|'.join(box[10:15]) + '\n' + \
          '-' * 31 + '\n' + \
          '|'.join(box[15:20]) + '\n' + \
          '-' * 31 + '\n' + \
          '|'.join(box[20:25]) + '\n' + \
          '-' * 31
    return msg


# 随机分组
def buildTeam(bot, contact):
    bot.SendTo(contact, '开始分组...')
    num = len(gameStatus['gamers'])
    if num % 2 == 0:
        a = num / 2
    else:
        a = (num + 1) / 2
    team_a = random.sample(gameStatus['gamers'], int(a))
    team_b = gameStatus['gamers'][:]
    for i in team_a:
        team_b.remove(i)
    leader_a = random.choice(team_a)
    leader_b = random.choice(team_b)
    team_a.remove(leader_a)
    team_b.remove(leader_b)
    gameStatus['leader A'], gameStatus['team A'] = leader_a, team_a
    gameStatus['leader B'], gameStatus['team B'] = leader_b, team_b
    bot.SendTo(contact, leader_a + 'A组：' + '、'.join(team_a) + '\n' + leader_b + 'B组：' + '、'.join(team_b))
