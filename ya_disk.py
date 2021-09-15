import requests


class YaDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_path(self, dir_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources/"
        params = {
            'path': dir_name
        }
        response = requests.put(url=url, params=params, headers=self.get_headers())
        return response.json()

    def _get_upload_link(self, disk_file_path: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, f, file_name: str, dir_name=None):
        if dir_name is not None and isinstance(dir_name, str):
            target_path = f'{dir_name}/{file_name}'
        else:
            target_path = file_name
        href = self._get_upload_link(disk_file_path=target_path).get("href", "")
        requests.put(href, files={'file': f})