import vk_api, time, dotenv, os

# - подключение к сессии вк -
dotenv.load_dotenv(dotenv_path="./VK_TOKEN.env")
vk_token = os.getenv("VK_TOKEN")
vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()

# - создание списка id друзей -
def createFriendList():
    friends = vk.friends.get()["items"]
    friends.append(228986289) # ~ костыль по личной необходимости ~
    friends.append(426884182) # ~ костыль по личной необходимости ~
    return friends

# - удаление диалога по id собеседника -
def deleteDialog(dialog_user_id):
    vk.messages.deleteConversation(peer_id=dialog_user_id)

# - проверка входит ли собеседник в список друзей -
def isItFriend(dialog_user_id, friend_id_list):
    return True if dialog_user_id in friend_id_list else False

# - проверка является ли диалог групповым -
def isItGroup(dialog_type):
    return True if dialog_type == "chat" else False

dialogs = vk.messages.getConversations(count=200)["items"] # список диалогов (не более 200)
dialogs_count = len(dialogs) # вероятнее всего равен 200, но так правильно :)

friend_id_list = createFriendList()

# - перебор 200 диалогов -
for i in range(dialogs_count):
    dialog_user_id = dialogs[i]['conversation']['peer']['id'] # id собеседника в диалоге
    dialog_type = dialogs[i]['conversation']['peer']['type'] # тип диалога

    # - скип группового диалога -
    if isItGroup(dialog_type) == True: 
        print(f"{i + 1} |  skip  | Групповой чат {dialog_user_id} пропущен")
        sec = 0
        continue

    # - удаление диалога -
    if isItFriend(dialog_user_id, friend_id_list) == False:
        deleteDialog(dialog_user_id)
        print(f"{i + 1} | delete | Диалог с {dialog_user_id} удалён успешно")
        sec = 1
    # - скип диалога с друзьями -
    else: 
        sec = 0
        print(f"{i + 1} |  skip  | Диалог не удалён, {dialog_user_id} ваш друг")

    time.sleep(sec) # динамический таймаут между запросами