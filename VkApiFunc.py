
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
    count = getMessageCount(session_api, user_id)

    if 1 > internal_id:
        print('[!] Error. internal_id must be > 0. First message_id was returned')
        return getFirstMessage(session_api, user_id)['id']
    if count < internal_id:
        print('[!] Error. internal_id must be <= message_count. Last message_id was returned')
        return getLastMessage(session_api, user_id)['id']

    for c in range(count//200+1):

        history = (session_api.messages.getHistory(
            count=200,
            user_id=user_id,
            start_message_id=start_message_id
        ))
        start_message_id = history['items'][-1]['id']

        for i in history['items']:
            if i['conversation_message_id'] == internal_id:
                return i['id']


def Parse(session_api, user_id: int, start_message_id: int, count: int) -> None:


    with open(f"{user_id}_file.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(['user', 'message', 'in_msg_id'])

        message_count = getMessageCount(session_api, user_id)
        if message_count < count:
            count = message_count+1

        for c in range(count//199+1):

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

    print("Done") 

