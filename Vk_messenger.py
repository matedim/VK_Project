# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import pprint
from urllib.parse import parse_qs
import webbrowser
import pickle
from datetime import datetime, timedelta
import vk
import time

# id of vk.com application
APP_ID = 5208517
# file, where auth data is saved
AUTH_FILE = '.auth_data'
# chars to exclude from filename
FORBIDDEN_CHARS = '/\\\?%*:|"<>!'

def get_saved_auth_params():
    access_token = None
    user_id = None
    try:
        with open(AUTH_FILE, 'rb') as pkl_file:
            token = pickle.load(pkl_file)
            expires = pickle.load(pkl_file)
            uid = pickle.load(pkl_file)
        if datetime.now() < expires:
            access_token = token
            user_id = uid
    except IOError:
        pass
    return access_token, user_id


def save_auth_params(access_token, expires_in, user_id):
    expires = datetime.now() + timedelta(seconds=int(expires_in))
    with open(AUTH_FILE, 'wb') as output:
        pickle.dump(access_token, output)
        pickle.dump(expires, output)
        pickle.dump(user_id, output)


def get_auth_params():
    auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                "&scope=wall,messages&redirect_uri=http://oauth.vk.com/blank.html"
                "&display=page&response_type=token".format(app_id=APP_ID))
    webbrowser.open_new_tab(auth_url)
    redirected_url = input("Paste here url you were redirected:\n")
    aup = parse_qs(redirected_url)
    aup['access_token'] = aup.pop(
        'https://oauth.vk.com/blank.html#access_token')
    save_auth_params(aup['access_token'][0], aup['expires_in'][0],
                     aup['user_id'][0])
    return aup['access_token'][0], aup['user_id'][0]


def get_api(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session)

def send_message(api, user_id, message, **kwargs):
    data_dict = {
        'user_id': user_id,
        'message': message,
    }
    data_dict.update(**kwargs)
    return api.messages.send(**data_dict)

def main():
    access_token, _ = get_saved_auth_params()
    if not access_token or not _:
        access_token, _ = get_auth_params()
    api = get_api(access_token)

#    users = [116131,652052,2639223,3638433,4277345,4471099,4701070,5096881,5534930,5716736,5786013,6255215,6316678,6491137,6519645,6586776,6633308,6803703,6804410,6913681,6955033,7010042,7082793,7373702,7516998,7517188,7816136,8205372,8272472,8310942,8435975,8527240,8818174,8916741,9069133,9146405,9801504,10018958,11314739,11491656,11621461,11653178,12140392,12186925,12244932,12529049,12939252,13106215,13562236,14281058,14397424,14573033,14580155,15666129,16122936,16418362,16490614,17909912,18036182,18283630,18292006,18698610,19670833,19784035,19957771,21149860,21317219,22395117,23442063,24212012,24540571,25454545,25866372,26785616,26942418,27190369,31109934,31981655,32703825,34499670,34534408,35237716,36799226,37098373,38103246,42102592,44584689,44869069,46500299,47193010,49677709,51816726,52222133,54125854,56696566,59566124,63824164,64874227,65358451,65707364,72114814,73002405,73241151,81011258,84567573,90383602,90833240,91178765,91428162,91845765,95237578,95349560,96108912,97776321,99644583,100732098,109040718,111078410,127640702,133975511,135006352,140057093,140676812,146506268,156296159,156859106,158912338,160583871,162057866,162854687,164597447,165092089,166690110,171806845,196420483,196522863,198737347,201020089,232109823,242769097,245779090,258143312,322607438]
    users = [153597,22395117]
    user_text = "Всего вам хорошего самого лучшего \nУдачи во всём и счастливого случая\nПусть будут приятными ваши заботы,\nХорошие чувства приносит работа.\nПускай не несет Новый год огорчения,\nА только отличного вам настроения!"
    user_teg = " #поздравьдрузей"
    for user_id in users:
        print("User ", user_id)
        res = send_message(api, user_id=user_id, message=user_text + user_teg)
        time.sleep(1)
        print(res)

main()
