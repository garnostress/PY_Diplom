from ya_disk import YaDisk
import requests
import json
from tqdm import tqdm


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, user_id, count=5, offset=0):
        self.user_id = user_id
        self.count = count
        self.offset = offset
        self.params = {
            'access_token': token,
            'v': '5.131'
        }
        self.photos = None

    def get_user_photos(self):
        get_photo_url = self.url + 'photos.get'
        get_photo_params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': self.count,
            'offset': self.offset
        }
        r = requests.get(get_photo_url, params={
            **self.params, **get_photo_params}).json()
        return r

    def get_name_list(self):
        pic_likes = []
        pic_date = []
        self.photos = self.get_user_photos()['response']['items']
        for name in self.photos:
            pic_likes.append(str(name['likes']['count']))
            pic_date.append(str(name['date']))
        idx = [i for i, x in enumerate(pic_likes) if x in filter(
            lambda x: pic_likes.count(x) > 1, set(pic_likes))]
        for i in idx:
            old_index = pic_likes.pop(i)
            new_index = old_index + '_' + pic_date[i]
            pic_likes.insert(i, new_index)
        return pic_likes

    def count_photos(self):
        count = self.get_user_photos()['response']['count']
        return count

    def get_photo_size(self):
        size_type = []
        for photo in self.photos:
            size_type.append(photo['sizes'][-1]['type'])
        return size_type

    def get_url(self):
        file_url = []
        for files in self.photos:
            file_url.append(files['sizes'][-1]['url'])
        return file_url

    def download_photo(self):
        photo_list = []
        name_photo = self.get_name_list()
        size = self.get_photo_size()
        all_dict = dict(zip(name_photo, size))
        file_name = []
        for key, value in all_dict.items():
            file_name.append(key + '{}'.format('.jpg'))
            file_name_2 = key + '{}'.format('.jpg')
            photo_dict = {'File name': file_name_2, 'sizes': value}
            photo_list.append(photo_dict)
        with open('Photos_list.json', 'w') as file:
            json.dump(photo_list, file)
        return file_name

    def upload_photos_ya(self, token):
        target_path = input('Введите имя директории для сохранения файлов:\n')
        upload_ya = YaDisk(token=token)
        upload_ya.create_path(target_path)
        key_name = self.download_photo()
        url = self.get_url()
        all_dict = dict(zip(key_name, url))
        for key, value in tqdm(all_dict.items(), ascii=True, desc='Загрузка файлов на Яндекс Диск'):
            get_url = requests.get(value).content
            get_name = key
            upload_ya.upload_file_to_disk(get_url, get_name, target_path)