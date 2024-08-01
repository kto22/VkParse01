
import vk_api
import csv



def getFirstMessage(session_api, user_id: int) -> int:
    data = (session_api.messages.getHistory(
        count=1,
        user_id=user_id,
        rev=1
    ))
    return data['items'][0]


def getLastMessage(session_api, user_id: int) -> int:
    data = (session_api.messages.getHistory(
        count=1,
        user_id=user_id,
        rev=0
    ))
    return data['items'][0]


def getMessageCount(session_api, user_id: int) -> int:
    data = (session_api.messages.getHistory(
        count=0,
        user_id=user_id
    ))
    return data['count']


def getMessageExternalId(session_api, user_id: int, internal_id: int) -> int:

    start_message_id = getLastMessage(session_api, user_id)['id']
    count = internal_id

    for c in range(getMessageCount(session_api, user_id)//200+1):

        history = (session_api.messages.getHistory(
            count=200 if count > 199 else count,
            user_id=user_id,
            start_message_id=start_message_id
        ))
        count -= 199
        start_message_id = history['items'][-1]['id']
        history['items'].pop(-1)

        for i in history['items']:
            if i['conversation_message_id']==internal_id:
                return i['id']
    return 0


def Parse(session_api, user_id: int, start_message_id: int, count: int) -> None:


    with open(f"{user_id}_file.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(['user', 'message', 'in_msg_id'])

        message_count = getMessageCount(session_api, user_id)
        if message_count < count:
            count = message_count+1

        for c in range(count//200+1):

            history = (session_api.messages.getHistory(
                count=200 if count > 199 else count,
                user_id=user_id,
                start_message_id=start_message_id
            ))

            count -= 199
            start_message_id = history['items'][-1]['id']

            last_item = history['items'][-1]
            history['items'].pop(-1)


            for i in history['items']:

                message = i['text']
                id = i['conversation_message_id']
                user = i['from_id']

                writer.writerow([user, message, id])

        message = last_item['text']
        id = last_item['conversation_message_id']
        user = last_item['from_id']
        writer.writerow([user, message, id])

    print("Done!")


# -------------------------TESTS--------------------------------------------------

token = 'vk1.a.6kRn17RcZyO5gIVW9sVx8bjPr5nU1P7G2kEin1T0Y8u3fJVmQmq4xGwUnZIoQmJwLuQQDYT4YzzKeb7vuoaBBE-LRSAeY8PL0TPp18SSbM39eErT6SY3yZO6-aPBTZjn_5WU7u-T3d4KnxcuVW0PJbWYI9xgiz0NSry8eG6ZUeuJRaHpUgzwpaZpvfld2bcInc8cBLzEfSI5L8Ur_DIzKA'

vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
    #293536875
    #381832378
    #464241833

user_id = 381832378

a = getMessageExternalId(session_api, user_id, 196)
print(a)
#Parse(session_api, user_id, getLastMessage(session_api, user_id)['id'], 1000000000)



