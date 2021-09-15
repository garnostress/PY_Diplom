from VK import VK

HELP = """
Программа скачивает фото из Вконтакте и сохраняет их на Yandex.диск в указанную папку
для начала работы Вам необходимо:
1. Ввести  команду "id"
2. Ввести свой token VK
3. Ввести свой токен Яндекс Диска
4. Ввести id пользователя
5. Нажать "Enter"

После загрузки в каталоге появиться файл 'Photos_list' с названием и размером фотографии

Список доступных команд:
help - справка по программе
id -  ввести id профиля
exit - команда выхода из программы"""

print('Программа скачивания фотографий из VK.com на Yandex.disk\n'
      'справка по программе: help\n')
stop = False
while not stop:
    command = input("Введите команду:\n")
    if command == "help":
        print(HELP)
    elif command == "id":
        user_token_vk = input('Введите token VK:\n')
        user_id_input = input('Введите id пользователя:№\n')
        down_vk = VK(token=user_token_vk, user_id=user_id_input)
        print(f'У пользователя {user_id_input} количество фотографий в профиле: {down_vk.count_photos()}\n')
        count_photo = int(input('Введите количество фотографий для скачивания:\n'))
        user_token_ya = input('Введите token YandexDisk:\n')
        down_vk = VK(token=user_token_vk, user_id=user_id_input, count=count_photo)
        down_vk.upload_photos_ya(user_token_ya)
    elif command == "exit":
        print("Спасибо за использование программы")
        stop = True
    else:
        print("Неизвестная команда")