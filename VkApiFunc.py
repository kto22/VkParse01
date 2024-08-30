
import multiprocessing
import vk_api
import csv
import os
from CSVFunctions import repeatDelete, repeatCount


class VkParser:
    __slots__ = ("token", "user_id", "session_api")

    def __init__(self, token: str, user_id: int) -> None:
        self.user_id = user_id
        self.token = token
        vk_session = vk_api.VkApi(token=token)
        session_api = vk_session.get_api()
        self.session_api = session_api

    def getFirstMessage(self) -> int:
        data = (self.session_api.messages.getHistory(
            count=1,
            user_id=self.user_id,
            rev=1
        ))
        return data['items'][0]

    def getLastMessage(self) -> int:
        data = (self.session_api.messages.getHistory(
            count=1,
            user_id=self.user_id,
            rev=0
        ))
        return data['items'][0]

    def getMessageCount(self) -> int:
        data = (self.session_api.messages.getHistory(
            count=0,
            user_id=self.user_id
        ))
        return data['count']

    def getMessageExternalId(self, start_message_internal_id: int) -> int:
        data = self.session_api.messages.getByConversationMessageId(
            peer_id=self.user_id,
            conversation_message_ids=start_message_internal_id
        )
        return data['items'][0]['id']



    def Parse(self, start_message_internal_id: int, count: int) -> None:

        message_count = self.getMessageCount()
        if message_count < count:
            count = message_count + 1
        for process_id in range(count // 200 + 1):


            ParseProcess(process_id, self.token, self.user_id, start_message_internal_id).start()

            """multiprocessing.Process(target=getMessages, args=(self.token,
                                                              self.user_id,
                                                              process_id,
                                                              start_message_internal_id)).start()"""

            print(f'the process {process_id} has started its work!')
            count -= 200
            start_message_internal_id -= 200

        print("All processes are running!")


'''
def getMessages(token, user_id, process_id, start_message_internal_id) -> None:
    vk_session = vk_api.VkApi(token=token)
    session_api = vk_session.get_api()

    if not os.path.isdir('CSV_temp'):
        os.mkdir('CSV_temp')

    with open(f"CSV_temp/{process_id}_file.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        iter_count = 200
        while True:
            try:
                data = session_api.messages.getByConversationMessageId(
                    peer_id=user_id,
                    conversation_message_ids=start_message_internal_id
                )
                message_id = data['items'][0]['id']
                break
            except:
                start_message_internal_id -= 1
                iter_count-=1

        history = (session_api.messages.getHistory(
            count=iter_count,
            user_id=user_id,
            start_message_id=message_id
        ))

        for c in range(200):
            i = history['items'][c]
            message = ''.join(i['text'].splitlines())
            id = i['conversation_message_id']
            user = i['from_id']

            writer.writerow([user, message, id])

    print(f'the process {process_id} has completed its work!')
'''


class ParseProcess(multiprocessing.Process):
    __slots__ = ("process_id", "token", "user_id", "start_message_internal_id")
    def __init__(self, process_id: int, token: str, user_id: int, start_message_internal_id: int):
        super().__init__()
        self.process_id = process_id
        self.token = token
        self.user_id = user_id
        self.start_message_internal_id = start_message_internal_id

    def run(self) -> None:
        vk_session = vk_api.VkApi(token=self.token)
        session_api = vk_session.get_api()

        if not os.path.isdir('CSV_temp'):
            os.mkdir('CSV_temp')

        with open(f"CSV_temp/{self.process_id}_file.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            iter_count = 200
            while True:
                try:
                    data = session_api.messages.getByConversationMessageId(
                        peer_id=self.user_id,
                        conversation_message_ids=self.start_message_internal_id
                    )
                    message_id = data['items'][0]['id']
                    break
                except:
                    self.start_message_internal_id -= 1
                    iter_count -= 1

                    print(f'bebra{self.process_id}-----------------------------------------------------------')

            history = (session_api.messages.getHistory(
                count=iter_count,
                user_id=self.user_id,
                start_message_id=message_id
            ))

            for c in range(iter_count):
                i = history['items'][c]
                message = ''.join(i['text'].splitlines())
                id = i['conversation_message_id']
                user = i['from_id']
                if id <= self.start_message_internal_id-200:
                    break
                writer.writerow([user, message, id])

        repeatDelete(self.process_id, 200-iter_count)
        print(f'the process {self.process_id} has completed its work!')


# -------------------------TESTS--------------------------------------------------

if __name__ == '__main__':

    token = ''


    user_id = 263703091

    parse_vk = VkParser(token, user_id)
    parse_vk.Parse(61000, 59999)
    print(parse_vk.getMessageCount())
