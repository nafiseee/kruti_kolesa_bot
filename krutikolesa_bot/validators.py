import re
def name_validate(message):
    pattern = r'^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$'
    return bool(re.match(pattern, message.text))
def phone_validate(message):
    pattern = r'^8\d{10}$'
    return bool(re.match(pattern, message.text))
def act_validate(message):
    pattern = r'[0-9]+'
    return bool(re.match(pattern, message.text))
def model_validate(message):
    return message.text in ["Шаркусь монстр 15","Шаркусь монстр 20","Мингто монстр 15","Монстр про","Крути 15"]
def id_validate(message):
    return act_validate(message)
def iot_validate(message):
    return act_validate(message)
