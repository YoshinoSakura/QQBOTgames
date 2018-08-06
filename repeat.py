#this is an repeat machine
import random , time




#==========初始定义==========
sleeptime = 1
repeat = 'initial'
norepeat = 'F'
repeatblacklist = []


def onQQMessage(bot, contact, member, content):
    global repeat , norepeat , repeatblacklist

    if bot.isMe(contact, member): #如果已经复读过就不在复读
        if content == repeat:
            norepeat = 'T'
        else:
            pass

    elif content == '': #忽略图片信息
        pass
    
    elif contact in repeatblacklist:
        pass

    elif content == '-roll':
        temp = int(random.random() * 100)
        sleepsend(bot, contact, '%s随机到%d点!' % (member.nick , temp))


    elif content == repeat:
        if norepeat == 'F':
            bot.SendTo(contact, content)
    
    else:
        repeat = content
        norepeat = 'F'





#==========定义==========
def sleepsend(bot, contact, content):
    global sleeptime

    time.sleep(1)
    bot.SendTo(contact, content)


