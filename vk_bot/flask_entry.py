import pprint
import requests
import random

from flask import Flask, request
from vk_bot.secret import API_TOKEN, CONFIRMATION_LINE
from vk_bot.preprocess import preprocess_message
from vk_bot.responder import get_response, VkResponse


def send_text_msg(text: str, user_id: int):
    params = {
        'v': '5.101',
        'message': text,
        'user_id': user_id,
        'peer_id': user_id,
        'access_token': API_TOKEN,
        'random_id': random.randint(10000, 1000000000000)
    }
    x = requests.post(f"https://api.vk.com/method/messages.send?", data=params)
    pprint.pprint(x.json())


def send_msg_with_img(text: str, img_url: str):
    server_for_img = requests.post(f"https://api.vk.com/method/photos.getMessagesUploadServer?",
                                   data={'peer_id': 53245164, 'access_token': API_TOKEN, 'v': '5.101'})
    pprint.pprint(server_for_img.json())
    # requests.post(f"https://api.vk.com/method/photos.getMessagesUploadServer?")


def send_message(response: VkResponse):
    if response.image_url:
        pass
    if response.text:
        send_text_msg(response.text, response.user_id)


def handle_user_message(json_data) -> str:
    message_data = json_data['object']
    preprocessed_request = preprocess_message(message_data)
    response = get_response(preprocessed_request)
    send_message(response)

    return r'ok'


TYPE_HANDLERS = {
    'confirmation': lambda json_data: CONFIRMATION_LINE,
    'message_new': handle_user_message,
}


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def entry():
        json_data = request.json
        try:
            handler = TYPE_HANDLERS.get(json_data.get('type'))
            if handler:
                response_text = handler(json_data)
                return response_text

            print(f'unknown request type: {json_data.get("type")}')
        except Exception as e:
            print(f'Exception is occured: {e}')
        return r'ok'

    return app


def run(host: str = '0.0.0.0', port: int = 80, is_debug=False):
    app = create_app()
    app.debug = is_debug
    app.run(host=host, port=port)


if __name__ == '__main__':
    send_text_msg('ыф', 53245164)
    # run()
