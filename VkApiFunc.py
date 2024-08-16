
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


def getMessageByInternalId(session_api, user_id: int, internal_id: int) -> int:

    data = session_api.messages.getByConversationMessageId(
        peer_id=user_id,
        conversation_message_ids=internal_id
    )
    return data['items'][0]


def Parse(session_api, user_id: int, start_message_id: int, count: int) -> None:

    with open(f"CSV/{user_id}_file.csv", "w", newline="", encoding="utf-8") as csvfile:
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

