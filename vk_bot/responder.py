from dataclasses import dataclass
from typing import Optional

from vk_bot.preprocess import PreprocessedRequest


@dataclass
class VkResponse:
    user_id: int
    text: Optional[str]
    image_url: Optional[str]


def get_response(request: PreprocessedRequest) -> VkResponse:
    texts = [request.source_text, request.audio_message_text]
    request_text = '\n'.join([text for text in texts if text])
    request_text = request_text or None
    return VkResponse(text=request_text, image_url=request.image_url, user_id=request.user_id)
