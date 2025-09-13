import re
from electro_works import electro_works
from mechanical_works import mechanical_works
def name_validate(text):
    pattern = r'^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$'
    return bool(re.match(pattern, text))
def phone_validate(text):
    pattern = r'^8\d{10}$'
    return bool(re.match(pattern, text))
def act_validate(text):
    pattern = r'[0-9]+$'
    return bool(re.match(pattern, text))
def model_validate(text):
    return text in ["Шаркусь монстр 15","Шаркусь монстр 20","Мингто монстр 20","Монстр про","Крути 15"]
def id_validate(text):
    return act_validate(text)
def iot_validate(text):
    return act_validate(text)
def bycycle_type_validate(text):
    return text in ['Механика','Электро']
def work_is_true(text):
    for i in electro_works.values():
        if text in i:
            return True
    return False
