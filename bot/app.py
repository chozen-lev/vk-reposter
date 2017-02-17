from flask import Flask, request
import telebot
import requests
import io
import os
from threading import Thread
from config import config, lang
import unidecode

app = Flask(__name__)

bot = telebot.TeleBot(config['telegram_token'])
bot.remove_webhook()
bot.set_webhook(url=config['heroku_url'] + '/updates/tg')

TG_DOC_MAXSIZE = 52428800
last_update_id = 0

@bot.message_handler(commands=['list'])
def get_list(message):
    list = ''
    for group in config['groups']:
        if message.chat.id in config['groups'][group]['chats']:
            list += '\n- [' + config['groups'][group]['name'] + '](https://vk.com/club' + str(group) + ')'
    bot.send_message(message.chat.id, list, parse_mode = 'markdown')

@app.route('/updates/tg', methods=['POST'])
def getTGUpdates():
    global last_update_id
    message_json = request.get_json()

    if message_json['update_id'] > last_update_id:
        bot.process_new_updates([telebot.types.Update.de_json(message_json)])
        last_update_id = message_json['update_id']
        return 'ok', 200

    return '!', 200

@app.route('/updates/vk', methods=['POST'])
def getVKUpdates():
    message_json = request.get_json()

    if message_json['type'] == 'confirmation':
        return config['groups'][message_json['group_id']]['vk_conformation_token'], 200
    elif message_json['secret'] == config['groups'][message_json['group_id']]['vk_secret_key']:
        thr = Thread(target = VKUpdates_handler, args = [message_json])
        thr.start()
        return 'ok', 200

    return '!', 200

def VKUpdates_handler(message_json):
    if message_json['type'] == 'wall_post_new':
        for chat in config['groups'][message_json['group_id']]['chats']:
            bot.send_message(chat, lang[config['groups'][message_json['group_id']]['chats'][chat]['lang']]['wall_post_new'].format(config['groups'][message_json['group_id']]['name'], '(https://vk.com/club' + str(message_json['group_id']) + '?w=wall-' + str(message_json['group_id']) + '_' + str(message_json['object']['id']) + ')'), parse_mode = 'markdown')
            
            if message_json['object']['text']:
                bot.send_message(chat, message_json['object']['text'], disable_notification=True)

            if 'attachments' in message_json['object']:
                for attachment in message_json['object']['attachments']:
                    if attachment['type'] == 'photo':
                        bot.send_chat_action(chat, 'upload_photo')

                        url = attachment['photo']['photo_75']
                        if 'photo_2560' in attachment['photo']:
                            url = attachment['photo']['photo_2560']
                        elif 'photo_1280' in attachment['photo']:
                            url = attachment['photo']['photo_1280']
                        elif 'photo_807' in attachment['photo']:
                            url = attachment['photo']['photo_807']
                        elif 'photo_604' in attachment['photo']:
                            url = attachment['photo']['photo_604']
                        elif 'photo_130' in attachment['photo']:
                            url = attachment['photo']['photo_130']

                        bot.send_photo(chat, url, disable_notification=True)
                    elif attachment['type'] == 'doc':
                        bot.send_chat_action(chat, 'upload_document')
                        if attachment['doc']['size'] < TG_DOC_MAXSIZE:
                            data = requests.get(attachment['doc']['url']).content
                            thing = io.BytesIO(data)
                            thing.name = unidecode.unidecode(attachment['doc']['title'])
                            
                            bot.send_document(chat, thing, disable_notification=True)
                        else:
                            size = attachment['doc']['size']

                            if size > 1024:
                                size = size / 1024.0
                                if size > 1024:
                                    size = size / 1024.0
                                    size = ' (%.1f MB)' % size
                                else:
                                    size = ' (%.1f KB)' % size
                            else:
                                size = ' (%d B)' % size

                            bot.send_message(chat, '[' + attachment['doc']['title'] + '](' + attachment['doc']['url'] + ')' + size, parse_mode = 'markdown', disable_web_page_preview=True, disable_notification=True)
                    elif attachment['type'] == 'audio':
                        bot.send_chat_action(chat, 'upload_audio')
                        bot.send_audio(chat, attachment['audio']['url'], disable_notification=True)
                    elif attachment['type'] == 'video':
                        bot.send_message(chat, '[' + attachment['video']['title'] + '](https://vk.com/video' + str(attachment['video']['owner_id']) + '_' + str(attachment['video']['id']) + ')', parse_mode = 'markdown', disable_notification=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))