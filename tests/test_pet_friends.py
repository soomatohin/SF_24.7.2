from api import PetFriends
from settings import valid_email, valid_password
import random
import os

pf = PetFriends()


def test_api_key_get(email=valid_email, password=valid_password):
    """Проверка на статус запроса == 200 при запросе API ключа и в ответе присутствует ключ 'key'"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_pet_get_list(pet_filter='my_pets'):
    """Проверка статуса запроса и самого списка своих питомцев (может быть пустым, но списком)"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, pet_filter)

    assert status == 200

    if not isinstance(result['pets'], list):
        raise Exception("Элемент 'pets' не является списком.")

    assert len(result['pets']) >= 0


def test_pet_add(name='Стеклокотамбус', animal_type='Стеклокот',
                 age='8', pet_photo='images/glasscat.jpg'):
    """Проверка на корректное добавление питомца и изменения длины списка после добавления
    (в сравнении со списком перед добавлением)"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    list_len_save = len(result['pets'])

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
    list_len_save += 1

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert len(result['pets']) == list_len_save


def test_pet_update_first(name='Ужаскот', animal_type='Ужастик', age='5'):
    """Проверка обновления информации первого в свиспе своего питомца, длина списка питомцев при этом не должна меняться"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    list_len_save = len(result['pets'])

    temp, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют.")

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert len(result['pets']) == list_len_save


def test_pet_update_photo_any(pet_photo='images/cursecat.jpg'):
    """Проверка обновления фотографии случайного своего питомца, длина списка питомцев при этом не должна меняться"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    list_len_save = len(result['pets'])

    temp, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = pf.add_pet_photo(auth_key, random.choice(my_pets['pets'])['id'], pet_photo)

        assert status == 200
    else:
        raise Exception("Питомцы отсутствуют.")

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert len(my_pets['pets']) == list_len_save


def test_pet_delete_first():
    """Проверка удаления первого в списке своих питомцев (длина списка питомцев должна сократиться)"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    list_len_save = len(result['pets'])

    temp, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        raise Exception("Питомцы отсутствуют.")
    else:
        pet_id = my_pets['pets'][0]['id']
        status, temp = pf.delete_pet(auth_key, pet_id)
        assert status == 200
        list_len_save -= 1

    temp, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    assert pet_id not in my_pets.values()
    assert len(my_pets['pets']) == list_len_save


def test_pet_add_simple(name='Великолепнокот', animal_type='Магнификант',
                 age='9'):
    """Проверка на корректное добавление питомца и изменения длины списка после добавления
    (в сравнении со списком перед добавлением)"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    list_len_save = len(result['pets'])

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    list_len_save += 1

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert len(result['pets']) == list_len_save


def test_pet_update_photo_first(pet_photo='images/magnificat.jpg'):
    """Проверка обновления информации питомца, длина списка питомцев при этом не должна меняться"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    list_len_save = len(result['pets'])

    temp, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
    else:
        raise Exception("Питомцы отсутствуют.")

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert len(my_pets['pets']) == list_len_save


def test_pet_delete_any():
    """Проверка удаления случайного своего питомца в списке (длина списка питомцев должна сократиться)"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    list_len_save = len(result['pets'])

    temp, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        raise Exception("Питомцы отсутствуют.")
    else:
        pet_id = random.choice(my_pets['pets'])['id']
        status, temp = pf.delete_pet(auth_key, pet_id)
        assert status == 200
        list_len_save -= 1

    temp, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert pet_id not in my_pets.values()
    assert len(my_pets['pets']) == list_len_save


def test_api_key_get_inv_pswrd(email=valid_email):
    """Проверка статуса запроса ключа с некорректным паролём"""

    password = '1234567890'
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_api_key_get_no_pswrd(email=valid_email):
    """Проверка статуса запроса ключа без пароля"""

    password = None
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_api_key_get_inv_email(password=valid_password):
    """Проверка статуса запроса ключа с некорректным email"""

    email = 'abc'
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_api_key_get_no_email(password=valid_password):
    """Проверка статуса запроса ключа без email"""

    email = None
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_pet_get_list_no_key(pet_filter='my_pets'):
    """Проверка статуса запроса списка своих питомцев при отсутствующем auth_key"""

    auth_key = {'key': None}
    status, result = pf.get_list_of_pets(auth_key, pet_filter)

    assert status == 403


def test_pet_get_list_inv_key(pet_filter='my_pets'):
    """Проверка статуса запроса списка своих питомцев при некорректном auth_key"""

    auth_key = {'key': '12345678-9ABC-DEF0-1234-56789ABCDEF0'}
    status, result = pf.get_list_of_pets(auth_key, pet_filter)

    assert status == 403

def test_pet_add_inv_name(name=None, animal_type='Некто',
                 age='9', pet_photo='images/glasscat.jpg'):
    """Проверка на добавление питомца с некорректным именем (тип None) и неизменностью длины списка после этого действия
    (в сравнении со списком перед добавлением)"""

    temp, auth_key = pf.get_api_key(valid_email, valid_password)

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    list_len_save = len(result['pets'])

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

    temp, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert len(result['pets']) == list_len_save