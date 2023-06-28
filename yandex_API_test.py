import pytest
import requests
import time


# "Получаем токены из файла"
with open('yandex_token.txt', 'r') as file_object:
    token_yd = file_object.readline().strip()

new_folder = 'Some_folder'


# "Объявляем тестируемую функцию (метод create_folder в классе YaUploader)"
class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
        }

    def create_folder(self, folder_name):
        """Создает папку на Yandex Disc. Выводит сообщение о результате работы"""

        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        path = folder_name
        fields = {
            'Resource': 'name,path,size'
        }
        request = {"path": path, "fields": fields}
        response = requests.put(upload_url, headers=self.headers, params=request)
        if response.status_code == 201:
            print(f'Folder {path} successfully created\n')
        elif response.status_code == 409:
            print('Folder already exists\n')
        else:
            print('Unexpected failure during folder creation occurred\n')
        time.sleep(0.33)
        return response


# "Создаем представителя класса"
uploader = YaUploader(token_yd)

# "Тестируем (тесты в одном модуле с функцией, чтобы не "плодить сущностей")"
"""NB!: plugin pytest-dependency is required.
        for more info, visit: https://pypi.org/project/pytest-dependency/
        installation: pip install pytest-dependency"""


@pytest.mark.dependency(name='connection')
def test_check_connection():
    assert uploader.create_folder(new_folder).status_code not in [400, 401],\
        'Connection failed!'


@pytest.mark.dependency(depends=['connection'])
@pytest.mark.xfail(uploader.create_folder(new_folder).status_code not in [200, 201],
                   reason="Folder exists or API reports error")
def test_create_folder():
    assert uploader.create_folder(new_folder).status_code in [200, 201], \
        f'{uploader.create_folder(new_folder).json()["message"]}'


@pytest.mark.dependency(depends=['connection'])
@pytest.mark.xfail(uploader.create_folder(new_folder).status_code not in [409],
                   reason="Status - ok! New folder is being created")
def test_check_folder_name_duplication():
    assert uploader.create_folder(new_folder).status_code in [409], \
        f'{uploader.create_folder(new_folder).json()["message"]}'


@pytest.mark.dependency(depends=['connection'])
def test_check_folder_existence(folder_name=new_folder):
    headers = uploader.headers
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    path = folder_name
    fields = {
        'Resource': 'name,path,size'
    }
    request = {"path": path, "fields": fields}
    response = requests.get(upload_url, headers=headers, params=request)
    assert response.status_code == 200, 'Folder not found!'


@pytest.mark.dependency(depends=['connection'])
@pytest.mark.xfail(uploader.create_folder(new_folder).status_code not in [403, 404, 406, 413, 423, 429, 503, 507],
                   reason="No critical errors occurs")
def test_check_for_critical_faults_response():
    assert uploader.create_folder(new_folder).status_code in [403, 404, 406, 413, 423, 429, 503, 507], \
        f'{uploader.create_folder(new_folder).json()["message"]}'
