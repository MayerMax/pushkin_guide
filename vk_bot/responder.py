import threading
from typing import Optional
from dataclasses import dataclass

from dialogue_system.manager import DialogueManager
from dialogue_system.queries.text_based import TextQuery
from vk_bot.preprocess import PreprocessedRequest


DM = DialogueManager()
LOCK_1 = threading.Lock()
LOCK_2 = threading.Lock()


@dataclass
class VkResponse:
    user_id: int
    text: Optional[str]
    image_url: Optional[str]


def get_response(request: PreprocessedRequest) -> VkResponse:
    texts = [request.source_text, request.audio_message_text]
    request_text = '\n'.join([text for text in texts if text])
    request_text = request_text or None
    if not request_text:
        return VkResponse(text=None, image_url=None, user_id=request.user_id)

    LOCK_1.acquire()
    try:
        LOCK_2.acquire()
        try:
            response = DM.reply(str(request.user_id), TextQuery(request_text))
            response_text = response.to_key_value_format()['text']
            return VkResponse(text=response_text, image_url=request.image_url, user_id=request.user_id)
        except:
            LOCK_2.release()
    except:
        LOCK_1.release()
    return VkResponse(text=None, image_url=None, user_id=request.user_id)
