import requests

temp = 'https://api.vk.com/method/{method}?{param}&access_token={token}&v={ver}'

token = '2eb84bfe03f4e9390ddca83932d7d2d0c86c96066f59a4e4c92930e183b5f46fb5dcbd9376bf8b81f6248'
ver = 5.95


def postIMG():
    method = 'photos.getMessagesUploadServer'
    param = '1'
    q = temp.format(method=method, param=param, token=token, ver=ver)
    r = requests.get(q)
    ans = r.json()

    r = requests.post(ans['response']['upload_url'], files=dict(photo=open('out.jpg', 'rb')))
    ans = r.json()

    method = 'photos.saveMessagesPhoto' # +server, photo, hash
    q = temp.format(method=method, param=param, token=token, ver=ver)
    r = requests.get(q)
    ans = r.json()

    method = 'messages.send'
    ### attachment медиавложения к личному сообщению, перечисленные через запятую.Каждое прикрепление представлено в формате: typeowner_id_media_id


if __name__ == '__main__':
    postIMG()
