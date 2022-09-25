import toml
import os
import asyncio

from vkbottle import API
from vkbottle.exception_factory import VKAPIError
from vkbottle.user import User, Message, run_multibot

with open("config.toml", "r", encoding="utf-8") as f:
    if "token" in os.environ:
        config = dict(os.environ)
        for key, value in toml.load(f).items():
            if key not in config:
                config[key] = value
    else:
        config = toml.load(f)

user = User()
member_id_list = []

@user.on.chat_message(action = "chat_kick_user")
async def add_chat_user(message: Message):
    for i in range(0, len(member_id_list)):
        try:
            await message.ctx_api.messages.add_chat_user(chat_id=(message.peer_id - 2000000000), user_id=member_id_list[i])
            break
        except VKAPIError[15]:
            pass
        except VKAPIError[9]:
            print("Flood control")
            break
        except VKAPIError as e:
            print(e)
            pass

############################### Настройка перед запуском ######################################################

async def api_from_config(apies):
    global member_id_list
    for i in range(0, len(config["token"])):
        apies.append(API(config["token"][i]))
        member_id_list.append(int(dict(await User(config["token"][i]).api.account.get_profile_info())['id']))

if __name__ == "__main__":
    apies = []
    api_climer = asyncio.get_event_loop()
    api_climer.run_until_complete(api_from_config(apies))
    run_multibot(user, apis=(apies))
