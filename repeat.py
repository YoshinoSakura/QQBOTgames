#this is an repeat machine

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

    elif content == repeat:
        if norepeat == 'F':
            bot.SendTo(contact, content)
    
        else:
            repeat = content
            norepeat = 'F'


