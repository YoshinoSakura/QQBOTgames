#that's bad
import time, random , math , copy


#----------初始文件定义----------

repeat = 'initial'
norepeat = 'F'
blacklist = []
helpfile = '''-gan [名字] 打包一个群友'''

helpfile2 = '''
    -gan [名字] 打包一个群友
    -ammu [类型] 切换弹药,ap为穿甲弹,he为高爆弹
    -buy [ID] 剁手
    -check 查看自己的状态
    -check [名字] 查看一个人的状态
    -equip [ID] 装备仓库里的物品
    -fire [名字] 炮击一个群友，消耗弹药
    -list 查看当前正在战场的群友
    -rep 查看自己的仓库
    -shield 回港
    -shop 查看商店
    -start 新群友入next door
    -tor [名字] 雷击一个群友，消耗鱼雷
    -unequip [ID] 卸下装备
    
    '''

#----------初始数据定义----------
users = [{'ID':0 , 'name':'default' , 'money':0 , 'level':1 , 'exp':0 , 'type':'JORIC' , 'basicmaxhealth':20 , 'maxhealth':20 , 'health':20 , 'fireavailable':True , 'basicfire':1 , 'fire':1 , 'basicaccuracy':1 , 'accuracy':1 , 'basicevade':1 , 'evade':1 , 'basicarmor':1 , 'armor':1 , 'basicluck':1 , 'luck':1 , 'status':'Idle' , 'firebuff':0 , 'defbuff':0 , 'torbuff':0 , 'basicfirecd':300 , 'firecd':300 , 'basictorcd':600 , 'torcd':600 , 'toravailable':True , 'basictor':1 , 'tor':1 , 'fireready':time.time() , 'torready':time.time() , 'recoverready':time.time() , 'basicrecovercd':1200 , 'recovercd':1200} , ]




#----------主体程序----------
def onQQMessage(bot, contact, member, content):
    global repeat , norepeat , blacklist



    if bot.isMe(contact, member): #如果已经复读过就不在复读
        if content == repeat:
            norepeat = 'T'
        else:
            pass



    elif content == '': #忽略图片信息
        pass



    elif member.nick in blacklist: #忽略黑名单信息
        pass



    elif '-gan' in content:
        sleepsend(bot , contact, '打包%s' % content[5:])



    elif '-end' in content:
        sleepsend(bot , contact, '你在说你[emoji]呢')



    elif content == '-check':
        tempid = returnid(member.nick)
        sleepsend(bot , contact, '%s生命值为%d/%d' % (member.nick , users[tempid]['health'] , users[tempid]['maxhealth']))



    elif '-fire' in content: #炮击
        tempattid = returnid(member.nick)
        tempdefid = returnid(content[6:])
        checkstatus(content[6:])
        checkstatus(member.nick)
        
        
        if users[tempattid]['status'] != 'Idle': #检查攻击方是否在战场
            sleepsend(bot, contact, '你不在战斗状态!')
            return
        
        if checkexist(content[6:]): #检查目标是否存在
            
            if users[tempattid]['fireavailable'] == 'False':
                sleepsend(bot , contact, '你没有主♂炮!')
            

            if users[tempdefid]['status'] == 'Idle': #检查目标是否可以攻击
                pass

            else:
                sleepsend(bot , contact, '%s不在战斗状态!' % content[6:])
                return



            if users[tempdefid]['type'] == 'SS':
                sleepsend(bot , contact, '你打不了潜艇的,放弃吧')
                return

            
            
            if checkfirecd(member.nick) == 0:
                users[tempattid]['fireready'] = time.time() + users[tempattid]['firecd'] #重新计算冷却
                tempresult = firedamage(tempattid , tempdefid)
            
                if tempresult == ['miss']:
                    sleepsend(bot , contact, '%s并未击中%s!辣鸡!' % (member.nick , content[6:]))
            
                else:
                    users[tempdefid]['health'] = users[tempdefid]['health'] - tempresult[0] #计算伤害
                    if tempresult[1] == 10:
                        sleepsend(bot , contact , '%s击中了%s的弹药库,造成%d点伤害!!!' % (member.nick , content[6:] ,tempresult[0]))
                    elif tempresult[1] == 3:
                        sleepsend(bot , contact , '%s击中了%s的舰桥,造成%d点伤害!' % (member.nick , content[6:] ,tempresult[0]))
                    elif tempresult[1] == 1.25:
                        sleepsend(bot , contact , '%s击中了%s的副炮塔,造成%d点伤害!' % (member.nick , content[6:] ,tempresult[0]))
                    else:
                        sleepsend(bot , contact , '%s击中了%s,造成%d点伤害!' % (member.nick , content[6:] ,tempresult[0]))
        

        
                    if users[tempdefid]['health'] < 1: #检查是否击沉
                        users[tempdefid]['status'] = 'Recover'
                        users[tempdefid]['recoverready'] = time.time() + users[tempdefid]['recovercd']
                        sleepsend(bot , contact, '%s被击沉!' % content[6:])

            elif checkfirecd(member.nick) > 0:
                sleepsend(bot , contact, '%s的主炮还在装填中' % member.nick)
        
        


        else:
            sleepsend(bot , contact, '你所打包的用户不存在!')



    elif content == '-help':
        sleepsend(bot , contact, helpfile)



    elif 'ammu' in content:
        pass



    elif content == '-roll':
        tnumber = random.random()
        tnumber = int(tnumber * 100)
        sleepsend(bot , contact, '%s随机到%d点!' % (member, tnumber))



    elif '-start' in content:
        if checkexist(member.nick):
            sleepsend(bot , contact, '%s你已经是一名boy next door了' % member.nick)
        
        else:
            if content[7:] in ['BB' , 'BC' , 'DD' , 'awesome' , 'CL' , 'CA' , 'CV' , 'SS' , 'CVL']:
                register(member.nick, content[7:])
                sleepsend(bot , contact, '%s成功加入新日暮里!' % member.nick)

            elif content[7:]:
                sleepsend(bot , contact , '请输入有效类型')
                    
            else:
                sleepsend(bot , contact , '请输入-start [舰船类型]来获取初始舰船')
                



    elif '-tor' in content: #雷击
        tempattid = returnid(member.nick)
        tempdefid = returnid(content[5:])
        checkstatus(content[5:])
        checkstatus(member.nick)
        
        
        if users[tempattid]['status'] != 'Idle': #检查攻击方是否在战场
            sleepsend(bot, contact, '你不在战斗状态!')
            return
        
        if checkexist(content[5:]):
            
            if users[tempattid]['toravailable'] == 'False':
                sleepsend(bot , contact, '你没有大♂鱼♂雷!')
            

            if users[tempdefid]['status'] == 'Idle': #检查目标是否可以攻击
                pass
            
            else:
                sleepsend(bot , contact, '%s不在战斗状态!' % content[5:])
                return
            
            if checktorcd(member.nick) == 0:
                tempresult = tordamage(tempattid, tempdefid)
                
                if tempresult == ['miss']:
                    users[tempattid]['torready'] = time.time() + users[tempattid]['torcd'] #重新计算冷却
                    sleepsend(bot , contact, '%s并未击中%s!辣鸡!' % (member.nick , content[5:]))
                
                else:
                    users[tempdefid]['health'] = users[tempdefid]['health'] - tempresult[0] #计算伤害
                    
                    if tempresult[1] == 10:
                        sleepsend(bot , contact , '%s击中了%s的油箱,造成%d点伤害!!!' % (member.nick , content[5:] ,tempresult[0]))
                    elif tempresult[1] == 3:
                        sleepsend(bot , contact , '%s击中了%s的方向舵,造成%d点伤害!' % (member.nick , content[5:] ,tempresult[0]))
                    elif tempresult[1] == 1.25:
                        sleepsend(bot , contact , '%s击穿了%s的水密舱,造成%d点伤害!' % (member.nick , content[5:] ,tempresult[0]))
                    else:
                        sleepsend(bot , contact , '%s击中了%s,造成%d点伤害!' % (member.nick , content[5:] ,tempresult[0]))
    
    

                    if users[tempdefid]['health'] < 1: #检查是否击沉
                        users[tempdefid]['status'] = 'Recover'
                        users[tempdefid]['recoverready'] = time.time() + users[tempdefid]['recovercd']
                        sleepsend(bot , contact, '%s被击沉!' % content[5:])
            
            elif checktorcd(member.nick) > 0:
                sleepsend(bot , contact, '%s的鱼雷还在装填中' % member.nick)




        else:
            sleepsend(bot , contact, '你所打包的用户不存在!')



    elif content == '-debug':
        sleepsend(bot, contact, '%s' % users)
    



    elif content == repeat:
        if norepeat == 'F':
            sleepsend(bot , contact, content)
    
        else:
            repeat = content
            norepeat = 'F'




#----------游戏内容定义----------

def sleepsend(bot, cta, cte): #延迟回复防封号
    time.sleep(1)
    bot.SendTo(cta, cte)





def checkexist(name): #检查用户是否存在
    global users
    
    tempid = 0
    for things in users:
        if name == users[tempid]['name']:
            return True
        tempid = tempid + 1
    return False





def register(name, type): #新注册
    global users

    templen = len(users)
    tempuser = copy.deepcopy(users[0])
    users.append(tempuser) #创建新用户
    users[templen]['ID'] = templen
    users[templen]['name'] = name

    if type == 'BB':
        users[templen]['type'] = 'BB'
        users[templen]['basicmaxhealth'] = 200
        users[templen]['maxhealth'] = 200
        users[templen]['health'] = 200
        users[templen]['fireavailable'] = True
        users[templen]['basicfire'] = 80
        users[templen]['fire'] = 80
        users[templen]['basicfirecd'] = 300
        users[templen]['firecd'] = 30
        users[templen]['basicaccuracy'] = 10
        users[templen]['accuracy'] = 10
        users[templen]['basicevade'] = 2
        users[templen]['evade'] = 2
        users[templen]['basicarmor'] = 10
        users[templen]['armor'] = 10
        users[templen]['basicluck'] = 3
        users[templen]['luck'] = 3
        users[templen]['basictorcd'] = 0
        users[templen]['torcd'] = 0
        users[templen]['toravailable'] = False
        users[templen]['basictor'] = 0
        users[templen]['tor'] = 0
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 600
        users[templen]['recovercd'] = 60
        

    elif type == 'BC':
        users[templen]['type'] = 'BC'
        users[templen]['basicmaxhealth'] = 120
        users[templen]['maxhealth'] = 120
        users[templen]['health'] = 120
        users[templen]['fireavailable'] = True
        users[templen]['basicfire'] = 55
        users[templen]['fire'] = 55
        users[templen]['basicfirecd'] = 180
        users[templen]['firecd'] = 18
        users[templen]['basicaccuracy'] = 9
        users[templen]['accuracy'] = 9
        users[templen]['basicevade'] = 3
        users[templen]['evade'] = 3
        users[templen]['basicarmor'] = 6
        users[templen]['armor'] = 6
        users[templen]['basicluck'] = 7
        users[templen]['luck'] = 7
        users[templen]['basictorcd'] = 0
        users[templen]['torcd'] = 0
        users[templen]['toravailable'] = False
        users[templen]['basictor'] = 0
        users[templen]['tor'] = 0
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 400
        users[templen]['recovercd'] = 40


    elif type == 'CA':
        users[templen]['type'] = 'CA'
        users[templen]['basicmaxhealth'] = 80
        users[templen]['maxhealth'] = 80
        users[templen]['health'] = 80
        users[templen]['fireavailable'] = True
        users[templen]['basicfire'] = 35
        users[templen]['fire'] = 35
        users[templen]['basicfirecd'] = 80
        users[templen]['firecd'] = 8
        users[templen]['basicaccuracy'] = 10
        users[templen]['accuracy'] = 10
        users[templen]['basicevade'] = 4
        users[templen]['evade'] = 4
        users[templen]['basicarmor'] = 5
        users[templen]['armor'] = 5
        users[templen]['basicluck'] = 1
        users[templen]['luck'] = 1
        users[templen]['basictorcd'] = 0
        users[templen]['torcd'] = 0
        users[templen]['toravailable'] = False
        users[templen]['basictor'] = 0
        users[templen]['tor'] = 0
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 300
        users[templen]['recovercd'] = 30


    elif type == 'CL':
        users[templen]['type'] = 'CL'
        users[templen]['basicmaxhealth'] = 50
        users[templen]['maxhealth'] = 50
        users[templen]['health'] = 50
        users[templen]['fireavailable'] = True
        users[templen]['basicfire'] = 15
        users[templen]['fire'] = 15
        users[templen]['basicfirecd'] = 60
        users[templen]['firecd'] = 6
        users[templen]['basicaccuracy'] = 10
        users[templen]['accuracy'] = 10
        users[templen]['basicevade'] = 6
        users[templen]['evade'] = 6
        users[templen]['basicarmor'] = 3
        users[templen]['armor'] = 3
        users[templen]['basicluck'] = 5
        users[templen]['luck'] = 5
        users[templen]['basictorcd'] = 600
        users[templen]['torcd'] = 60
        users[templen]['toravailable'] = True
        users[templen]['basictor'] = 150
        users[templen]['tor'] = 150
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 200
        users[templen]['recovercd'] = 20


    elif type == 'DD':
        users[templen]['type'] = 'DD'
        users[templen]['basicmaxhealth'] = 30
        users[templen]['maxhealth'] = 30
        users[templen]['health'] = 30
        users[templen]['fireavailable'] = True
        users[templen]['basicfire'] = 8
        users[templen]['fire'] = 8
        users[templen]['basicfirecd'] = 30
        users[templen]['firecd'] = 3
        users[templen]['basicaccuracy'] = 11
        users[templen]['accuracy'] = 11
        users[templen]['basicevade'] = 8
        users[templen]['evade'] = 8
        users[templen]['basicarmor'] = 2
        users[templen]['armor'] = 2
        users[templen]['basicluck'] = 6
        users[templen]['luck'] = 6
        users[templen]['basictorcd'] = 300
        users[templen]['torcd'] = 30
        users[templen]['toravailable'] = True
        users[templen]['basictor'] = 120
        users[templen]['tor'] = 120
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 150
        users[templen]['recovercd'] = 15


    elif type == 'SS':
        users[templen]['type'] = 'SS'
        users[templen]['basicmaxhealth'] = 15
        users[templen]['maxhealth'] = 15
        users[templen]['health'] = 15
        users[templen]['fireavailable'] = False
        users[templen]['basicfire'] = 0
        users[templen]['fire'] = 0
        users[templen]['basicfirecd'] = 0
        users[templen]['firecd'] = 0
        users[templen]['basicaccuracy'] = 8
        users[templen]['accuracy'] = 8
        users[templen]['basicevade'] = 4
        users[templen]['evade'] = 4
        users[templen]['basicarmor'] = 1
        users[templen]['armor'] = 1
        users[templen]['basicluck'] = 1
        users[templen]['luck'] = 1
        users[templen]['basictorcd'] = 400
        users[templen]['torcd'] = 40
        users[templen]['toravailable'] = True
        users[templen]['basictor'] = 200
        users[templen]['tor'] = 200
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 150
        users[templen]['recovercd'] = 15


    elif type == 'CV':
        users[templen]['type'] = 'CV'
        users[templen]['basicmaxhealth'] = 150
        users[templen]['maxhealth'] = 150
        users[templen]['health'] = 150
        users[templen]['fireavailable'] = False
        users[templen]['basicfire'] = 80
        users[templen]['fire'] = 80
        users[templen]['basicfirecd'] = 300
        users[templen]['firecd'] = 30
        users[templen]['basicaccuracy'] = 12
        users[templen]['accuracy'] = 12
        users[templen]['basicevade'] = 6
        users[templen]['evade'] = 6
        users[templen]['basicarmor'] = 6
        users[templen]['armor'] = 6
        users[templen]['basicluck'] = 6
        users[templen]['luck'] = 6
        users[templen]['basictorcd'] = 0
        users[templen]['torcd'] = 0
        users[templen]['toravailable'] = False
        users[templen]['basictor'] = 0
        users[templen]['tor'] = 0
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 400
        users[templen]['recovercd'] = 40


    elif type == 'CVL':
        users[templen]['type'] = 'CVL'
        users[templen]['basicmaxhealth'] = 75
        users[templen]['maxhealth'] = 75
        users[templen]['health'] = 75
        users[templen]['fireavailable'] = False
        users[templen]['basicfire'] = 80
        users[templen]['fire'] = 80
        users[templen]['basicfirecd'] = 300
        users[templen]['firecd'] = 30
        users[templen]['basicaccuracy'] = 15
        users[templen]['accuracy'] = 15
        users[templen]['basicevade'] = 6
        users[templen]['evade'] = 6
        users[templen]['basicarmor'] = 3
        users[templen]['armor'] = 3
        users[templen]['basicluck'] = 2
        users[templen]['luck'] = 2
        users[templen]['basictorcd'] = 0
        users[templen]['torcd'] = 0
        users[templen]['toravailable'] = False
        users[templen]['basictor'] = 0
        users[templen]['tor'] = 0
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 200
        users[templen]['recovercd'] = 20


    elif type == 'awesome':
        users[templen]['type'] = 'awesome'
        users[templen]['basicmaxhealth'] = 1
        users[templen]['maxhealth'] = 1
        users[templen]['health'] = 1
        users[templen]['fireavailable'] = True
        users[templen]['basicfire'] = 0
        users[templen]['fire'] = 0
        users[templen]['basicfirecd'] = 20
        users[templen]['firecd'] = 2
        users[templen]['basicaccuracy'] = 66
        users[templen]['accuracy'] = 66
        users[templen]['basicevade'] = 0
        users[templen]['evade'] = 0
        users[templen]['basicarmor'] = 0
        users[templen]['armor'] = 0
        users[templen]['basicluck'] = 66
        users[templen]['luck'] = 66
        users[templen]['basictorcd'] = 1800
        users[templen]['torcd'] = 180
        users[templen]['toravailable'] = True
        users[templen]['basictor'] = 4396
        users[templen]['tor'] = 4396
        users[templen]['fireready'] = users[templen]['torready'] = users[templen]['recoverready'] = time.time()
        users[templen]['basicrecovercd'] = 10
        users[templen]['recovercd'] = 1







def returnid(name): #反查编号
    global users

    tempid = 0
    for things in users:
        if name == users[tempid]['name']:
            return tempid
        tempid = tempid + 1
    return -1





def checkstatus(name): #检查用户是否恢复
    global users
    
    if users[returnid(name)]['status'] == 'Recover':
        if time.time() >= users[returnid(name)]['recoverready']:
            users[returnid(name)]['health'] = users[returnid(name)]['maxhealth']
            users[returnid(name)]['status'] = 'Idle'





def checkfirecd(name): #检查主炮cd
    global users

    if time.time() < users[returnid(name)]['fireready']:
        return int(users[returnid(name)]['fireready'] - time.time())

    else:
        return 0





def checktorcd(name): #检查鱼雷cd
    global users
    
    if time.time() < users[returnid(name)]['torready']:
        return int(users[returnid(name)]['torready'] - time.time())
    
    else:
        return 0





def firedamage(attid,defid):
    global users
    
    temprandom1 , temprandom2 , temprandom3 = random.random() , random.random() , random.random()
    tempchance = users[attid]['accuracy'] - users[defid]['evade']
    templuck = users[attid]['luck'] - users[defid]['luck']

    if tempchance > 0:
        if tempchance/(tempchance + 4) > temprandom1: #计算命中
            lucka = 1
            
            if users[attid]['luck'] / 5 /(users[attid]['luck'] + 8) > temprandom2: #计算暴击
                lucka = 10
            elif users[attid]['luck']/ 3 /(users[attid]['luck'] + 8) > temprandom2:
                lucka = 3
            elif users[attid]['luck']/(users[attid]['luck'] + 8) > temprandom2:
                lucka = 1.25
                      
            return [int(users[attid]['fire'] * (20/(users[defid]['armor']+20)) * lucka * (users[attid]['firebuff'] + 1) * (1 - users[defid]['defbuff']) * ((temprandom3/2 + 0.75))) , lucka]

        else:
            return['miss']
            

    else:
        return ['miss']




def tordamage(attid,defid):
    global users
    
    temprandom1 , temprandom2 , temprandom3 = random.random() , random.random() , random.random()
    tempchance = users[attid]['accuracy'] - users[defid]['evade']
    templuck = users[attid]['luck'] - users[defid]['luck']
    
    if tempchance > 0:
        if tempchance/(tempchance + 4) > temprandom1: #计算命中
            lucka = 1
            if users[attid]['luck']/ 5 / (users[attid]['luck'] + 8) > temprandom2 : #计算暴击
                lucka = 10
            elif users[attid]['luck']/ 3 /(users[attid]['luck'] + 8) > temprandom2 :
                lucka = 3
            elif users[attid]['luck']/(users[attid]['luck'] + 8) > temprandom2 :
                lucka = 1.25
            
            return [int(users[attid]['tor'] * (40/(users[defid]['armor']+40)) * lucka * (users[attid]['torbuff'] + 1) * (1 - users[defid]['defbuff']) * ((temprandom3 - 0.5)/5 + 1)) , lucka]

        else:
            return['miss']


    else:
        return ['miss']

                      
                      
                      
                      
                      
                      
                      
