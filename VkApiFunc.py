
import vk_api
import csv


def getFirstMessageId(session_api, user_id: int) -> int:
    data = (session_api.messages.getHistory(
        count=1,
        user_id=user_id,
        rev=1
    ))
    return data['items'][0]['id']


def getLastMessageId(session_api, user_id: int) -> int:
    data = (session_api.messages.getHistory(
        count=1,
        user_id=user_id,
        rev=0
    ))
    return data['items'][0]['id']


def getMessageCount(session_api, user_id: int) -> int:
    data = (session_api.messages.getHistory(
        count=0,
        user_id=user_id
    ))
    return data['count']


def getMessageExternalId(session_api, user_id: int, internal_id: int, start_message_id: int) -> int:

    for i in range(getMessageCount(session_api, user_id)//200+1):

        history = (session_api.messages.getHistory(
            count=200 if internal_id > 199 else internal_id,
            user_id=user_id,
            start_message_id=start_message_id
        ))
        internal_id -= 199
        start_message_id = history['items'][-1]['id']
        history['items'].pop(-1)


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



token = 'vk1.a.Y8fU3ok8PPILm-8uIbSFwxE8PKflDK7behEcdmzu1Dd_dvQsOMemusSYmHvUKR6DiUpPeF3FpjnP_lxqtEi3r24v9elK8y3jMfPr1K_cT5AyYnEdhhuMpK2LVFzsMHb1MaFi6-haCewTm_Wt8kA8kC9GLD3r5vnpwbCiJOaXlXJPAj9gjaW437W_tOFsEFwLDkLyZ9I68sGk3vLw3HSyOQ'
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
    #293536875
    #381832378
    #464241833

user_id = 2000000096
Parse(session_api, user_id, getLastMessageId(session_api, user_id), 1000000000)



