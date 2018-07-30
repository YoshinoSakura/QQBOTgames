#print('你真是一头胖居居！')
import random , re
repeat = 'initial'
norepeat = 'F'
blacklist = []


# ====================游戏版本=======================
ver= """
    v0.3.2
    """



# ====================接收部分=======================
def onQQMessage(bot,contact,member,content):
    global repeat , norepeat , blocklist
    
    if bot.isMe(contact, member): #如果已经复读过就不在复读
        if content == repeat:
            norepeat = 'T'
        else:
            pass
    
    elif content == '': #忽略图片信息
        pass

    elif contact in blacklist:
        pass
    
    elif content == '-hello':
        bot.SendTo(contact,'雷猴啊!')
    
    elif content == '-help':
        bot.SendTo(contact,'帮助: \n'
                   '-start 开始游戏 \n'
                   '-end 结束游戏 \n'
                   '-gj 干艽 \n'
                   '-rule 查看规则\n')
    
    elif content == '-start':
        processor(bot, contact, member, content, 'gamestart')
    
    elif content == '-end':
        processor(bot, contact, member, content, 'gameend')
    
    elif content == '-rule':
        bot.SendTo(contact, '请自行百度 阿瓦隆')
    
    elif content == '-ver':
        bot.SendTo(contact, ver)

    elif content == '-blacklist':
        if blacklist == []:
            bot.SendTo(contact, '现在没有人被拉黑了')
        else:
            bot.SendTo(contact, '%s' % blacklist)

    elif '-bladd' in content:
        blacklist.append(content[7:])
        bot.SendTo(contact, '成功将%s加入到黑名单!' % content[7:])

    elif '-bldel' in content:
        if
    
    elif '-game' in content:
        gprocessor(bot, contact, member, content)

    elif content == '-gj':
        bot.SendTo(contact, 'wtmgj!')

    elif content == '-goo':
        bot.SendTo(contact, '不干昍,不干昍')

    elif content == '-gwls':
        bot.SendTo(contact, '干自己!')

    elif content == '-gtata':
        bot.SendTo(contact, '我tm干爆tata!')

    elif content == '-g2b':
        bot.SendTo(contact, '学姐会伤心的')

    elif content == '-gzy':
        bot.SendTo(contact, 'van様')

    elif content == repeat:
        if norepeat == 'F':
            bot.SendTo(contact, content)
        
    else:
        repeat = content
        norepeat = 'F'


# ====================缺省值定义=======================
gamememberslist = {}
#defaultgamemembers = []
gamestatus = 'Idle'
# Idle:空闲; Waiting:等待报名中; Running:分配中; Capswitching:队长选择顺序中; Chatting:聊天中; Capselecting:队长选择出征人员中; Chatvoting:出征名单投票中; Conquervoting:出征投票中;

gamemembersrole = {}
gamemembersnumber = {}



#默认角色
defaultroles = [[0] , [1] , [2] , [3] , [4] , ['Merlin','Percival','Loyale','Morgana','Assassin'] , ['Merlin','Percival','Loyale','Loyale','Morgana','Assassin'] , ['Merlin','Percival','Loyale','Loyale','Morgana','Oberyn','Assassin'] , ['Merlin','Percival','Loyale','Loyale','Loyale','Morgana','Assassin','Lackey'] ,  ['Merlin','Percival','Loyale','Loyale','Loyale','Loyale','Mordred','Morgana','Assassin'] , ['Merlin','Percival','Loyale','Loyale','Loyale','Loyale','Mordred','Morgana','Oberyn','Assassin'] , [11]]



#默认轮数
defaultrounds = [[0] , [1] , [2] , [3] , [4] , [[2,3,2,3,3],[2,3,2,3,3]] , [[2,3,4,3,4],[2,3,4,3,4]] , [[2,3,3,4,4],[2,3,3,3,4]] , [[3,4,4,5,5],[3,4,4,4,5]] , [[3,4,5,5,6],[3,3,5,4,6]] , [[4,5,5,6,6],[4,4,5,5,6]] , [11]]





# ====================游戏外消息处理器=======================
def processor(bot, contact, member, content, command):
    global gamestatus
    
    if command == 'gamestart':
        if gamestatus == 'Idle':
            gamestatus = 'Waiting'
            bot.SendTo(contact, '游戏已开启,回复-gamehelp查看游戏帮助') #开始游戏

    elif command == 'gameend':
        bot.SendTo(contact, '游戏已关闭！') #结束游戏

    else:
        pass



# ====================游戏中消息处理器=======================
def gprocessor(bot, contact, member, content):
    global gamestatus , gamememberslist , gamemembersrole , gamemembersnumber , defaultrounds , chatround , missionround , chatseq , chatcount , currentchat , currentcap , currentmission , currentmissionnum ,  chatvote , missionvote , votecount , succount , failcount , losecount ,roundrules
    
    if content == '-gamehelp':
        bot.SendTo(contact, '游戏帮助: \n'
                   '-gamejoin 报名游戏\n'
                   '-gamege 鸽了\n'
                   '-gamechange 更改游戏配置\n'
                   '-gamestart 结束报名并开始游戏\n'
                   '-gamepass 跳过自己的发言\n'
                   '-gamecheck 检查游戏进行状态\n'
                   '-gamevote 检查投票\n'
                   '-gamerole (请私聊发送)查看自己的身份')
    
    
    
    elif content == '-gamejoin': #报名游戏
        if gamestatus == 'Idle':
            bot.SendTo(contact, '能不能先开一局游戏')
        elif not gamestatus == 'Waiting':
            bot.SendTo(contact, '大家正在玩儿呢,下一把再来吧')
        else:
            if member.nick in gamememberslist:
                bot.SendTo(contact, '%s已经报过名了' % member.nick)
            else:
                gamememberslist[member.nick] = [member , 0 , 'UnassignedRole']
                bot.SendTo(contact, '%s成功加入了战斗' % member.nick)



    elif content == '-gamege': #溜了溜了
        if gamestatus == 'Idle':
            bot.SendTo(contact, '请先打开游戏再ge')
        elif not gamestatus == 'Waiting':
            bot.SendTo(contact, '鸽你麻痹，打完这一把再干你')
        else:
            if not member.nick in gamememberslist:
                bot.SendTo(contact, '%s你先报名再鸽好不好' % member.nick)
            else:
                gamememberslist.pop(member.nick)
                bot.SendTo(contact, '%s鸽了,干%s!' % (member.nick , member.nick))



    elif content == '-gamechange': #自定义阵容
        bot.SendTo(contact, '这个功能还在开发中QAQ')
        
        
        
    elif content == '-gamestart': #停止报名
        if gamestatus == 'Busy':
            bot.SendTo(contact, '已经开了一把啦')
        elif gamestatus == 'Idle':
            bot.SendTo(contact, '请先召集一桌人再开始游戏')
        elif gamestatus == 'Waiting':
            if len(gamememberslist) < 5:
                bot.SendTo(contact, '游戏人数不足5人，无法开始')
            elif len(gamememberslist) > 10:
                bot.SendTo(contact, '游戏人数多于10人，无法开始')
            else:
                #分配号码和身份
                numberassign()
                roleassign()
                
                #初始化游戏数值
                chatround , missionround , chatseq , chatcount = 1 , 1 , 1 , 0
                currentmission ,currentmissionnum = [] , []
                chatvote = {}
                missionvote = {}
                votecount = 0
                succount , failcount , losecount = 0 , 0 , 0
                currentchat , currentcap = gamemembersnumber[1] , gamemembersnumber[1]
                    
                #for tempname in gamememberslist:      #改天再来钻研如何不回复就私聊发送
                    #tempqc = bot.List('buddy','tempname')
                    #contact.ctype = 'buddy'
                    #checkrole(bot, contact, tempqc, content)
                    #checknumber(bot, contact, tempqc, content)
                    #checknumber(bot, contact, member, content)

                roundrules = defaultrounds[len(gamememberslist)] #读取当前游戏规则
                
                bot.SendTo(contact, '请私聊发送-gamerole来查看自己的身份') #开始游戏
                bot.SendTo(contact, '下面是第%d轮出征的第%d次决策投票,请队长%s选择发言顺序:'
                               '发送-gamewxl自己先发言,发送-gamewzh自己最后发言' % (missionround , chatround , currentcap))



    elif content == '-gamewxl' or content == '-gamewzh': #队长选择发言顺序
        if not member.nick == currentcap:
            bot.SendTo(contact, '你哪只眼睛看到你是队长了?')
        else:
            if content == '-gamewxl':
                chatseq = chatseqcheck(chatseq)
                bot.SendTo(contact, '队长已选择自己发言,请%d号玩家%s发言。发送-gamepass结束发言' % (chatseq , gamemembersnumber[chatseq]))
            elif content == '-gamewzh':
                chatseq = chatseq + 1
                chatseq = chatseqcheck(chatseq)
                currentchat = gamemembersnumber[chatseq]
                bot.SendTo(contact, '队长已选择下家发言,请%d号玩家%s发言。发送-gamepass结束发言' % (chatseq , gamemembersnumber[chatseq]))



    elif content == '-gamepass': #结束发言
        if not member.nick == currentchat:
            bot.SendTo(contact, '不是你发言你闭zui!')
            
        elif member.nick == currentchat:
            chatseq = chatseq + 1
            chatseq = chatseqcheck(chatseq)
            chatcount = chatcount + 1
                
            if chatcount < len(gamememberslist): #判断是否所有人都发言
                currentchat = gamemembersnumber[chatseq]
                bot.SendTo(contact, '上个玩家发言已结束,现在是%d号玩家%s发言。发送-gamepass结束发言' % (chatseq , gamemembersnumber[chatseq]))
                
            elif chatcount >= len(gamememberslist):
                bot.SendTo(contact, '所有玩家发言结束,请队长指定出征的成员,本次需要指定%d名成员,需要%d个成功' % (roundrules[0][missionround - 1] , roundrules[1][missionround - 1]))
                bot.SendTo(contact,'请队长发送-gamemis [编号][编号](玩家编号不用加中括号,用空格来隔开)来指定本次任务的执行人')
                chatcount = 0



    elif '-gamemis' in content: #队长指定出征人员
        if not member.nick == currentcap:
            bot.SendTo(contact, '你又哪只眼睛看到你是队长了?')
        else:
            currentmissionnum = re.findall(r'(\w*[0-9]+)\w*',content)
            for temp in currentmissionnum:
                currentmission.append(gamemembersnumber[int(temp)])
                bot.SendTo(contact, '当前拟定出征的是%s,请在群里回复-gameac来支持,回复-gamedn来反对' % currentmission)
                chatvoteac = chatvotedn = 0 #重制投票计数



    elif content == '-gameac' or content == '-gamedn': #聊天投票
        if not contact.ctype == 'group':
            bot.SendTo(contact, '请勿私聊你的决定')
        elif not member.nick in gamememberslist:
            bot.SendTo(contact, '请不要瞎凑热闹')
        else:
            chatvote['第%d次出征%d轮讨论' % (missionround , chatround)] = {}
            if member.nick in chatvote['第%d次出征%d轮讨论' % (missionround , chatround)]:
                bot.SendTo(contact, '谁又在重复投票?')
            else:
                if content == '-gameac':
                    chatvote['第%d次出征%d轮讨论' % (missionround , chatround)][member.nick] = '同意'
                    chatvoteac = chatvoteac + 1
                elif content == '-gamedn':
                    chatvote['第%d次出征%d轮讨论' % (missionround , chatround)][member.nick] = '反对'
                    chatvotedn = chatvotedn + 1
                    #聊天投票判断
                if len(chatvote['第%d次出征%d轮讨论' % (missionround , chatround)]) >= len(gamememberslist):
                    missionvotesu = missionvotedn = 0 #重置任务投票
                        
                    if chatvoteac > chatvotedn: #投票成功
                        chatvote['第%d次出征%d轮讨论' % (missionround , chatround)]['result'] = '执行'
                        bot.SendTo(contact, '所有人投票已完成,本次出征即将执行,等待选定玩家出征')
                        bot.SendTo(contact, '请出征的玩家私聊回复决定,发送-gamesu成功,发送-gamefa失败')
                    
                    elif chatvoteac <= chatvotedn: #投票失败
                        chatvote['第%d次出征%d轮讨论 % (missionround , chatround)']['result'] = '流局'
                        bot.SendTo(contact, '所有人投票已完成,本次出征即将流局')
                        losecount = losecount + 1
                            
                        if losecount > 5: #判断是否过多流局
                            bot.SendTo(contact, '本次征兵流局次数过多(超过5次),该次出征直接失败!')
                            failcount = failcount + 1
                            chatround = 1
                            missionround = missionround + 1
                                
                            if failjudge(succount,failcount) == 'evilwin': #是否结束判断
                                bot.SendTo(contact, '游戏结束,邪恶方胜利')
                                gamestatus = 'Idle'
                                gamememberslist = {}

                            elif failjudge(succount,failcount) == 'justicewin':
                                bot.SendTo(contact, '游戏结束,正义方胜利')
                                gamestatus = 'Idle'
                                gamememberslist = {}

                            elif failjudge(succount,failcount) == 'assassinexist':
                                bot.SendTo(contact, '游戏结束,等待刺客拔刀!请阿萨辛大人发送-gamekill [玩家编号](编号不用带中括号)刺杀心目中的梅林')
                            
                        elif losecount <= 5: #新开一轮讨论
                            chatround = chatround + 1
                            bot.SendTo(contact, '下面是第%d轮出征的第%d次决策投票,请队长选择发言顺序:'
                                           '发送-gamewxl自己先发言,发送-gamewzh自己最后发言' % (missionround , chatround))



    elif content == '-gamesu' or content == '-gamedn': #出征投票
        if not contact.ctype == 'buddy':
            bot.SendTo(contact, '你是想大家知道你是坏蛋吗?')
        elif not member.nick in currentmission:
            bot.SendTo(contact, '你哪只眼睛看到队长选你了?')
        else:
            if member.nick in missionvote['第%d次出征' % missionround]:
                bot.SendTo(contact, '请不要重复投票!')
            else:
                if content == '-gamesu':
                    missionvote['第%d次出征' % missionround][member.nick] = '成功'
                    missionvotesu = missionvotesu + 1
                elif content == '-gamedn':
                    missionvote['第%d次出征' % missionround][member.nick] = '失败'
                    missionvotedn = missionvotedn + 1
                    #任务投票判断
                if len(missionvote['第%d次出征' % missionround]) >= len(currentmission):
                    if missionvotesu >= roundrules[1][missionround - 1]:
                        missionvote['第%d次出征' % missionround]['result'] = '成功'
                        bot.SendTo(contact, '所有人投票已完成,本次出征成功')
                        succount =succount + 1
                        
                    elif missionvotesu < roundrules[1][missionround - 1]:
                        missionvote['第%d次出征' % missionround]['result'] = '失败'
                        failcount =failcount + 1
                        
                        if failjudge(succount,failcount) == 'evilwin': #是否结束判断
                            bot.SendTo(contact, '游戏结束,邪恶方胜利')
                            gamestatus = 'Idle'
                            gamememberslist = {}

                        elif failjudge(succount,failcount) == 'justicewin':
                            bot.SendTo(contact, '游戏结束,正义方胜利')
                            gamestatus = 'Idle'
                            gamememberslist = {}
                        
                        elif failjudge(succount,failcount) == 'assassinexist':
                            bot.SendTo(contact, '游戏结束,等待刺客拔刀!请阿萨辛大人发送-gamekill [玩家编号](编号不用带中括号)刺杀心目中的梅林')
                        
                    #新一轮出征
                    missionround = missionround + 1
                    chatround = 1
                    bot.SendTo(contact, '即将开始第%d轮出征' % missionround)
                    currentcap = newcap(currentcap)
                    bot.SendTo(contact, '下面是第%d轮出征的第%d次决策投票,请队长%s选择发言顺序:'
                                   '发送-gamewxl自己先发言,发送-gamewzh自己最后发言' % (missionround , currentcap , chatround))



    elif '-gamekill' in content:
        if not gamememberslist[member.nick][2] == 'Assassin':
            bot.SendTo(contact, '你真的是刺客么')
            
        else:
            kill = re.findall(r'(\w*[0-9]+)\w*',content)
            kille = int(kill[0])
            killed = gamemembersnumber[kille]
                
            if gamememberslist[killed][2] == 'Merlin':
                bot.SendTo(contact, '刺客成功终结梅林,邪恶方胜利!')
                gamestatus = 'Idle'
                gamememberslist = {}
                
            elif not gamememberslist[killed][2] == 'Merlin':
                bot.SendTo(contact, '刺客杀错了人,正义方胜利!')
                gamestatus = 'Idle'
                gamememberslist = {}



    elif content == '-gamecheck':
        bot.SendTo(contact, '开发ing')

    

    elif content == '-gamevote':
        bot.SendTo(contact, '依旧开发ing')



    elif content == '-gamerole':
        checkrole(bot, contact, member, content)



    else:
        bot.SendTo(contact, '致命错误!请告诉oo并干oo!')




# ====================游戏玩家操作=======================





# ====================角色和分配操作=======================
def rolechange():
    pass



def roleassign(): #角色分配
    global roassign , gamememberslist , gamemembersrole , defaultroles
    
    roassign = defaultroles[len(gamememberslist)]
    random.shuffle(roassign)
    
    i0 = 0
    for tempname in gamememberslist:
        gamememberslist[tempname][2] = roassign[i0]
        gamemembersrole[roassign[i0]] = tempname
        i0 = i0 + 1



def numberassign(): #号码分配
    global numberassign , gamememberslist , gamemembersrole
    
    numassign=list(range(len(gamememberslist)))
    random.shuffle(numassign)
    
    i0 = 0
    for tempname in gamememberslist:
        gamememberslist[tempname][1] = numassign[i0] + 1
        gamemembersnumber[numassign[i0] + 1] = tempname
        i0 = i0 + 1



#告知角色信息
def checkrole(bot, contact, member, content):
    global gamememberslist ,roassign
    
    if contact.ctype == 'buddy' and contact.nick in gamememberslist: #检查是不是私聊
        tempqc = bot.List('buddy' , contact.nick)
        if tempqc:
            bot.SendTo(tempqc[0], '你的身份是%s' % gamememberslist[contact.nick][2])
            
            if gamememberslist[contact.nick][2] == 'Merlin':
                merlinlist = []
                if 'Oberyn' in roassign:
                    merlinlist.append(gamemembersrole['Oberyn'])
                if 'Morgana' in roassign:
                    merlinlist.append(gamemembersrole['Morgana'])
                if 'Assassin' in roassign:
                    merlinlist.append(gamemembersrole['Assassin'])
                if 'Lackey' in roassign:
                    merlinlist.append(gamemembersrole['Lackey'])
                random.shuffle(merlinlist)
                bot.SendTo(tempqc[0] , '玩家%s是大坏淫' % merlinlist)
            
            if gamememberslist[contact.nick][2] == 'Percival':
                percivalist = [gamemembersrole['Morgana'] , gamemembersrole['Merlin']]
                random.shuffle(percivalist)
                bot.SendTo(tempqc[0] , '玩家%s是绝世双雄' % percivalist)
            
            if gamememberslist[contact.nick][2] == 'Loyale':
                pass
            
            if gamememberslist[contact.nick][2] == 'Mordred':
                mordredlist = []
                if 'Morgana' in roassign:
                    mordredlist.append(gamemembersrole['Morgana'])
                if 'Assassin' in roassign:
                    mordredlist.append(gamemembersrole['Assassin'])
                if 'Lackey' in roassign:
                    mordredlist.append(gamemembersrole['Lackey'])
                random.shuffle(mordredlist)
                bot.SendTo(tempqc[0], '玩家%s和里一样是大坏淫' % mordredlist)
            
            if gamememberslist[contact.nick][2] == 'Morgana':
                morganalist = []
                if 'Mordred' in roassign:
                    morganalist.append(gamemembersrole['Mordred'])
                if 'Assassin' in roassign:
                    morganalist.append(gamemembersrole['Assassin'])
                if 'Lackey' in roassign:
                    morganalist.append(gamemembersrole['Lackey'])
                random.shuffle(morganalist)
                bot.SendTo(tempqc[0], '玩家%s和里一样是大坏淫' % morganalist)
            
            if gamememberslist[contact.nick][2] == 'Oberyn':
                pass
            
            if gamememberslist[contact.nick][2] == 'Assassin':
                assassinlist = []
                if 'Mordred' in roassign:
                    assassinlist.append(gamemembersrole['Mordred'])
                if 'Morgana' in roassign:
                    assassinlist.append(gamemembersrole['Morgana'])
                if 'Lackey' in roassign:
                    assassinlist.append(gamemembersrole['Lackey'])
                random.shuffle(assassinlist)
                bot.SendTo(tempqc[0], '玩家%s和里一样是大坏淫' % assassinlist)
            
            if gamememberslist[contact.nick][2] == 'Lackey':
                lackeylist = []
                if 'Mordred' in roassign:
                    lackeylist.append(gamemembersrole['Mordred'])
                if 'Assassin' in roassign:
                    lackeylist.append(gamemembersrole['Assassin'])
                if 'Morgana' in roassign:
                    lackeylist.append(gamemembersrole['Morgana'])
                random.shuffle(lackeylist)
                bot.SendTo(tempqc[0], '玩家%s和里一样是大坏淫' % lackeylist)



def checknumber(bot, contact, member, content):
    global gamememberslist
    
    if contact.ctype == 'buddy' and member.nick in gamememberslist: #私下问编号
        tempqc = bot.List('buddy' , member.nick)
        if tempqc:
            bot.SendTo(tempqc[0] , '你的编号是%d号' % gamememberslist[member.nick][1])

    elif contact.ctype == 'group': #群中问编号
        for tempname in gamememberslist:
            bot.SendTo(contact , '玩家%s的编号是%d' % (gamememberslist[tempname] , gamememberslist[tempname][1]))





# ====================游戏主体阶段=======================
def chatseqcheck(seqnum): #序列调整
    global gamememberslist
    
    while seqnum > len(gamememberslist):
        seqnum = seqnum - len(gamememberslist)
    while seqnum < 1:
        seqnum = seqnum + len(gamememberslist)
    return seqnum



def newcap(curcap):
    global gamemembersnumber , gamememberslist
    
    tempnum1 = gamemembersnumber[curcap] + 1
    tempnum2 = chatseqcheck(tempnum1)
    curcap = gamememberslist[tempnum2][1]
    return curcap



def assassincheck(): #刺客判断
    global gamestatus , gamemembersrole
    
    if not 'Assassin' in gamemembersrole:
        gamestatus = 'Idle'
        return 'justicewin'
    
    elif 'Assassin' in gamemembersrole:
        return 'assassinexist'



def failjudge(suc,fail): #出征胜负局数判断
    if suc >= 3 and fail <= 2:
        return assassincheck()
    
    elif suc < 3 and fail > 2:
        return 'evilwin'





# ====================识别玩家身份=======================
def getRole(member):
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


















