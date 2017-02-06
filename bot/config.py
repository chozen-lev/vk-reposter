config = {
    # heroku
    'heroku_url': '<heroku url address>', # e.g https://mybot.herokuapp.com

    # telegram
    'telegram_token': '<telegram bot token>', # token given by botfather

    'groups': {
        123456789: { # group id 
            'vk_conformation_token': '<conformation token>', # conformation string which is specified in Callback API
            'vk_secret_key': '<secret key>', # secret key that you specified in Callback API
            'chats': [
                {
                    'tg_chat_id': -123456789, # telegram chat id
                    'lang': 'ua' # language that will be used in that chat 
                }
                # here may be a few chats
            ]
        }
        # here may be a few groups
    }
}

lang = {
    'ua': {
        'start_message': 'Я дублюю записи з груп соціальної мережі Вконтакті.',
        'wall_post_new': 'В групі опубліковано [новий запис]{}'
    },
    'ru': {
        'start_message': 'Я дублирую записи с групп социальной сети Вконтакте.',
        'wall_post_new': 'В группе опубликована [новая запись]{}'
    }
}