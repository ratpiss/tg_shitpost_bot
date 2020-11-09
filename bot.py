import telebot
import random
from time import localtime, strftime, sleep
import creds
from PIL import Image, ImageFilter


class shitposter():
    def __init__(self,user_id,first_msg_time):
        self.user_id = user_id
        self.shitpost_count = 0
        self.first_msg_time = first_msg_time

shitposters = {}
token = creds.get_token()
bot = telebot.TeleBot(token)
selfname = 'синдром'
commands = ['добавь', 'монетка','выбор','помощь']

def you_talking_to_me(msg):
    if msg[0].lower() == selfname or msg[0].lower() == f'{selfname},':
        return True
    else:
        return False

@bot.message_handler(content_types = ['text'])
def reply(message):
    dt = strftime("%d.%m.%Y %H:%M:%S", localtime())
    print(dt + ' / ' +str(message.from_user.username) + ' in chat ' + str(message.chat.id) + ':' + str(message.text))
    text = message.text.split() #Разбиение текста сообщения на слова для анализа
    if you_talking_to_me(text):
        if len(text) == 1 or text[1] not in commands: #Просто обращение к боту
            with open('./phrases.txt', encoding='utf-8') as f:
                phrases = f.readlines()
            phrase = random.choice(phrases)
            bot.send_message(message.chat.id, phrase)
            print(f'-'+phrase)
        elif 'добавь' in text[1] and len(text)>2: #Добавление новой фразы
            phrase = ' '.join(text[2:])
            with open('./phrases.txt','a', encoding='utf-8') as f:
                f.write(phrase+'\n')
            response = f"{message.from_user.first_name}, я добавил {' '.join(text[2:])}"
            bot.send_message(message.chat.id,response)
            print(f'-'+response)
        elif 'монетка' in text[1]: #Подбрасывание монетки
            coin = ['Орел', 'Решка']
            response = random.choice(coin)
            bot.send_message(message.chat.id,response)
            print(f'-'+response)
        elif 'выбор' in text[1]: #Выбор между n вариантов
            if len(text) >= 5:
                text = ' '.join(text[2:])
                text = text.split('или')
                options = []
                for option in text:
                    options.append(option)
                response = random.choice(options)
                bot.send_message(message.chat.id,response)
                print(f'-'+response)
            else:
                response = 'Пример использования команды:\nСиндром выбор А или Б\nБот выберет случайный вариант из представленных\nВариантов может быть 2 или больше'
                bot.send_message(message.chat.id, response)
                print(f'-'+response)
        elif 'помощь' in text[1]: #/help
            with open('./help.txt', encoding = 'utf-8') as help:
                bot.send_message(message.chat.id,help.read())

    #Обработка шитпостеров
    if not message.from_user.id in shitposters: #если новый шитпостер
        shitposters[message.from_user.id] = shitposter(message.from_user.id, message.date) #создать шитпостера
    else:
        user = shitposters[message.from_user.id]
        if message.date - user.first_msg_time > 180:
            user.first_msg_time = message.date
            user.shitpost_count = 0
        if user.shitpost_count >= 7:
            with open('./phrases.txt', encoding='utf-8') as f:
                phrases = f.readlines()
            phrase = random.choice(phrases)
            bot.send_message(message.chat.id, phrase)
            user.shitpost_count = 0
            dt = strftime("%d.%m.%Y %H:%M:%S", localtime())
            print(dt + ' / ' +str(message.from_user.username) + ' shitposted in chat #' + str(message.chat.id))
        user.shitpost_count += 1

""" @bot.message_handler(content_types = ['photo'])
def ph_handler(message):
    
    print(message)
    ph = open(message.photo.file_id)
    bot.send_photo(message.chat.id, ph) """

if __name__ == "__main__":
    while True:
        try:
            print('Bot program started')
            bot.polling()
        except Exception as err:
            sleep(10)
            print('-'*50)
            print('Error: {}'.format(err))
            print(strftime("%d.%m.%Y %H:%M:%S", localtime()))
            pass