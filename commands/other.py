def gtm(message):
    if message.text:
        print('Пользователь {}, @{}, {} написал: {}'.format(message.from_user.id, message.from_user.username, message.from_user.first_name, message.text))
    elif message.photo:
        print('Пользователь {}, @{}, {} отправил фото: {}'.format(message.from_user.id, message.from_user.username, message.from_user.first_name, message.photo[0].file_id))
    elif message.sticker:
        print('Пользователь {}, @{}, {} отправил стикер: {}'.format(message.from_user.id, message.from_user.username, message.from_user.first_name, message.sticker.emoji))
    elif message.location:
        print('Пользователь {}, @{}, {} отправил локацию'.format(message.from_user.id, message.from_user.username, message.from_user.first_name))

def isempty(list: list or tuple, index: int):
    try:
        trash = list[index]
        return False
    except:
        return True

def isint(obj):
    try:
        int(obj)
        return True
    except:
        return False

def time(time: str):
    time.replace('Z', '')
    timesplit = time.split('T')
    date = timesplit[0].split('-')
    time = timesplit[1].split(':')
    year = date[0]
    month = date[1]
    day = date[2]
    hour = time[0]
    minute = time[1]
    second = time[2]
    datetime = {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'min': minute,
        'sec': second
    }
    return datetime

print("Cogs | other.py is ready")