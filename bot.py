import toml
import os
import random

from vkbottle import API, user
from vkbottle.user import User, Message, run_multibot
from vkbottle.exception_factory import VKAPIError

with open("config.toml", "r", encoding="utf-8") as f:
    if "token1" in os.environ and "token2" in os.environ:
        config = dict(os.environ)
        for key, value in toml.load(f).items():
            if key not in config:
                config[key] = value
    else:
        config = toml.load(f)

user = User()

@user.on.message(action = "chat_kick_user")
async def send_message(message: Message):
    try:
        if message.peer_id == 2000000000 + int(config["chat_id1"]):
            await message.ctx_api.messages.add_chat_user(
            chat_id=int(config["chat_id1"]),
            user_id=int(config["user_id1"])
            )
        elif message.peer_id == 2000000000 + int(config["chat_id2"]):
            await message.ctx_api.messages.add_chat_user(
                chat_id=int(config["chat_id2"]),
                user_id=int(config["user_id2"])
            )
    except VKAPIError[14]:
        await send_message(message)
    except VKAPIError:
        print("")

if __name__ == "__main__":
    run_multibot(user, apis=(API(config["token1"]), API(config["token2"])))
