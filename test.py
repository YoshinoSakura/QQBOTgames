#that's bad
import time


#----------初始数据定义----------

def onQQMessage(bot, contact, member, content):
    if bot.isMe(contact, member): #如果已经复读过就不在复读
        pass

    elif content == '': #忽略图片信息
        pass
    
    elif '1' in content:
        bot.SendTo(contact, '1')

    elif '2' in content:
        time.sleep(10)
        bot.SendTo(contact, '2')






