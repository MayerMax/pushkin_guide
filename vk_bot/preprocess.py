from typing import Optional
from dataclasses import dataclass

import requests


@dataclass
class PreprocessedRequest:
    user_id: int
    source_text: Optional[str]
    audio_message_text: Optional[str]
    image_url: Optional[str]


def get_source_text(message_data) -> Optional[str]:
    return message_data["text"] if 'text' in message_data and message_data["text"] else None


def get_text_from_speech(ogg_url) -> Optional[str]:
    pass


def get_audio_text(message_data) -> Optional[str]:
    for attachment in message_data['attachments']:
        if 'type' in attachment and not attachment['type'] == 'audio_message':
            continue
        ogg_url = attachment['audio_message']['link_ogg']
        text = get_text_from_speech(ogg_url)
        if text:
            return text
    return None


def get_image_url(message_data) -> Optional[str]:
    for attachment in message_data['attachments']:
        if 'type' in attachment and not attachment['type'] == 'photo':
            continue
        try:
            images = attachment['photo']['sizes']
            images.sort(key=lambda image: image['type'])
            return images[-1]
        except (KeyError, IndexError):
            continue
    return None


def get_user_id(message_data) -> str:
    return message_data['from_id']


def preprocess_message(message_data) -> PreprocessedRequest:
    return PreprocessedRequest(
        user_id=get_user_id(message_data),
        source_text=get_source_text(message_data),
        audio_message_text=get_audio_text(message_data),
        image_url=get_image_url(message_data)
    )
