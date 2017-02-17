config = {
    # heroku
    'heroku_url': '<heroku url address>', # e.g https://mybot.herokuapp.com

    # telegram
    'telegram_token': '<telegram bot token>', # token given by botfather

    'groups': {
        123456789: { # group id 
            'vk_conformation_token': '<conformation token>', # conformation string which is specified in Callback API
            'vk_secret_key': '<secret key>', # secret key that you specified in Callback API
            'name': '<group name>', # vk group name
            'chats': {
                -123456789 { # telegram chat id
                    'lang': 'ru' # language that will be used in that chat 
                }
                # here may be a few chats
        }
        # here may be a few groups
    }
}

lang = {
    'ua': {
        'wall_post_new': 'В групі {0} опубліковано [новий запис]{1}'
    },
    'ru': {
        'wall_post_new': 'В группе {0} опубликована [новая запись]{1}'
    }
}