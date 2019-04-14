import random

import requests

url = 'https://api.vk.com/method/'
token = '2eb84bfe03f4e9390ddca83932d7d2d0c86c96066f59a4e4c92930e183b5f46fb5dcbd9376bf8b81f6248'  # todo remove from vk
ver = 5.95


def postIMG(ar):
    img = ar[0]
    num = ar[1]

    method = 'photos.getMessagesUploadServer'
    param = dict(peer_id=0,
                 access_token=token,
                 v=ver)
    r = requests.get(url + method,
                     params=param)
    ans = r.json()

    f = open('temp.jpg', 'wb')
    f.write(img)
    f.close()
    r = requests.post(ans['response']['upload_url'],
                      files=dict(photo=open('temp.jpg', 'rb')))
    ans = r.json()

    method = 'photos.saveMessagesPhoto'  # +server, photo, hash
    param = dict(server=ans['server'],
                 photo=ans['photo'],
                 hash=ans['hash'],
                 access_token=token,
                 v=ver)
    r = requests.get(url + method,
                     params=param)
    ans = r.json()

    param = dict(user_id='15524226',
                 random_id=random.randint(10000, 1000000000000),
                 message=f'Купон {num}',
                 attachment='photo' + str(ans['response'][0]['owner_id']) + '_' + str(ans['response'][0]['id']),
                 access_token=token,
                 v=ver)
    method = 'messages.send'
    r = requests.get(url + method,
                     params=param)
    ans = r.json()

    # attachment медиавложения к личному сообщению, перечисленные через запятую.Каждое прикрепление представлено в
    # формате: typeOwner_id_Media_id


if __name__ == '__main__':
    postIMG()
