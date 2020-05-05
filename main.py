import vk_api, random
import _sqlite3

vk_session = vk_api.VkApi(token="ed9a4f317e0cd49a9e9e6aa03061048583ef8f13a8a37bcfd3ff6531fe108d1d3f1f9ec517aca586cb74c")

from vk_api.longpoll import VkLongPoll, VkEventType

longpool = VkLongPoll(vk_session)

vk = vk_session.get_api()

conn  = _sqlite3.connect("db.db")
c = conn.cursor()

def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True

def register_new_user(user_id):
    c.execute("INSERT into users (user_id, state) VALUES (%d, '')" % user_id)
    conn.commit()
    c.execute("INSERT into user_info (user_id, user_wish) VALUES (%d, 0)" % user_id)
    conn.commit()

def get_user_wish(user_id):
    c.execute("SELECT user_wish FROM user_info WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]

def set_user_wish(user_id, user_wish):
    c.execute("UPDATE user_info SET user_wish = %d WHERE user_id = %d" % (user_wish, user_id))
    conn.commit()


while True:
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            if not check_if_exists(event.user_id):
                register_new_user(event.user_id)

            if event.text.lower()=="привет":
                vk.messages.send(
                    user_id = event.user_id,
                    message = "Привет",
                    keyboard = open("keyboard.json", "r", encoding= "UTF-8").read(),
                    random_id = random.randint(0,1000000000)
                )

            elif event.text.lower()=="регистрация":
                if get_user_wish(event.user_id) == 0:
                    set_user_wish(event.user_id,1)
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Вы успешно зарегистрированы",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(0, 1000000000)
                    )
                else:
                    set_user_wish(event.user_id,0)
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Вы успешно удалены из бд",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(0, 1000000000)
                    )

            elif event.text.lower()=="ссылка":
                if get_user_wish(event.user_id) == 1:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Держи ссылку",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(0, 1000000000)
                    )
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Вы не зарегистрированы, напишите команду 'Регистрация'",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(0, 1000000000)
                    )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Моя твоя не понимать",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random.randint(0, 1000000000)
                )
