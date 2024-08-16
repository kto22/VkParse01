
import multiprocessing
import vk_api
import csv
import os


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


def messageGeter(token: str, user_id: int, process_id, start_message_internal_id: int) -> None:
    vk_session = vk_api.VkApi(token=token)
    session_api = vk_session.get_api()

    start_message_id = getMessageByInternalId(session_api, user_id, start_message_internal_id)['id']

    if not os.path.isdir('CSV_temp'):
        os.mkdir('CSV_temp')

    with open(f"CSV_temp/{process_id}_file.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")

        history = (session_api.messages.getHistory(
            count=200,
            user_id=user_id,
            start_message_id=start_message_id
        ))

        for c in range(200):
            i = history['items'][c]
            message = ''.join(i['text'].splitlines())
            id = i['conversation_message_id']
            user = i['from_id']

            writer.writerow([user, message, id])
            if id <= start_message_internal_id-199:
                break

    print(f'the process {process_id} has completed its work!')


def Parse(token: str, user_id: int, start_message_internal_id: int, count: int) -> None:
    vk_session = vk_api.VkApi(token=token)
    session_api = vk_session.get_api()

    message_count = getMessageCount(session_api, user_id)
    if message_count < count:
        count = message_count+1

    for process_id in range(count//200+1):
        multiprocessing.Process(target=messageGeter, args=(token, user_id, process_id, start_message_internal_id)).start()
        print(f'the process {process_id} has started its work!')
        count -= 200
        start_message_internal_id -= 200

    print("All processes are running!")


# -------------------------TESTS--------------------------------------------------

if __name__=='__main__':

    token = ''


    user_id = 468941965

    Parse(token, user_id, 5000, 3990)
