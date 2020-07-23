import requests
from pprintpp import pprint as pp
import time
from tqdm import tqdm
import json


# запрашиваем ввод id пользователя vk
profile_id = '552934290'  # input('Введите id пользователя: ')
# токены
ya_token = input('Введите token янедкс.диска: ')
vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
photos_limit = 10 # int(input('Введите количество фотографий: '))

def vk_api_photo(profile_id, photos_limit, vk_token, ya_token):
    yandex_add_folder(ya_token, profile_id)
    request = requests.get('https://api.vk.com/method/photos.get',
                           params={
                               'owner_id': profile_id,
                               'album_id': 'profile',
                               'extended': '1',
                               'count': photos_limit,
                               'v': '5.21',
                               'access_token': vk_token
                           })
    request = request.json()
    size = 0
    sizemax = ''

    for item in tqdm(request['response']['items']):
        f_name = item['likes']['count']
        for count in item:
            if 'photo' in count:
                if size < int(count.replace('photo_', '')):
                    size = int(count.replace('photo_', ''))
                    sizemax = count
        yandex_post(f_name, ya_token, item[sizemax], profile_id)
        json_creator(f_name, size, profile_id)

def yandex_add_folder(ya_token, profile_id):
    resp = requests.put('https://cloud-api.yandex.net:443/v1/disk/resources',
                        params = {
                            'path': profile_id
                        }, headers= {'Authorization': ya_token})
    
def yandex_post(f_name, ya_token, upload_url, profile_id):
    resp = requests.post('https://cloud-api.yandex.net:443/v1/disk/resources/upload',
                        params={
                            'path': f'{profile_id}/{f_name}',
                            'url': upload_url
                        }, headers={'Authorization': ya_token})

def json_creator(f_name, size, result):
    d = {
        'file_name': f_name,
        'size': size,
    }

    with open(f'{result}.json', "a") as f:
        json.dump(d, f)


vk_api_photo(profile_id, photos_limit, vk_token, ya_token)
