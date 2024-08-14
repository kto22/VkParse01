
import multiprocessing
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


def messageGeter(token: str, user_id: int, process_id, start_message_internal_id: int) -> None:
    vk_session = vk_api.VkApi(token=token)
    session_api = vk_session.get_api()

    start_message_id = session_api.messages.getByConversationMessageId(
        peer_id=user_id,
        conversation_message_ids=start_message_internal_id
    )['items'][0]['id']

    with open(f"{process_id}_file.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")

        history = (session_api.messages.getHistory(
            count=200,
            user_id=user_id,
            start_message_id=start_message_id
        ))

        for i in history['items']:
            message = i['text']
            id = i['conversation_message_id']
            user = i['from_id']

            writer.writerow([user, message, id])
    print(f'the process {process_id} has completed its work!')


def Parse(token: str, user_id: int, start_message_internal_id: int, count: int) -> None:
    vk_session = vk_api.VkApi(token=token)
    session_api = vk_session.get_api()

    message_count = getMessageCount(session_api, user_id)
    if message_count < count:
        count = message_count+1

    for process_id in range(count//199+1):
        multiprocessing.Process(target=messageGeter, args=(token, user_id, process_id, start_message_internal_id)).start()
        print(f'the process {process_id} has started its work!')
        count -= 200
        start_message_internal_id -= 200

    print("Parsing done!")


# -------------------------TESTS--------------------------------------------------

if __name__=='__main__':

    token = 'vk1.a.wdpsVDI88ySXSzQCQj9OhUOlzS4Ose9WHIxONT9HSE5b0oPkJ14WWChydSav7rSud645gRoPaqqj5162efTUvl1idfLlcKPRUA2xyZWy5_j31UzcyVx15hkFAH9WpUxmcokmZA0XF1LV9hWYH4Lj1Zqjx3MnYR2zlV_5IA6qoQrRwP6YxHEB5iXUnA4mQvz7k-OMz46HwfZUI_U8pbKFvg'

    # 293536875
    # 381832378
    # 464241833
    # 473379248
    # 2000000096

    user_id = 468941965
    # print(getMessageCount(session_api, user_id))
    # a = getMessageExternalId(session_api, user_id, 428)
    # print(a)

    Parse(token, user_id, 1800, 1591)
