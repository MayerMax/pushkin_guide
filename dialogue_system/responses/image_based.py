from dialogue_system.responses.abstract import AbstractResponse


class SingleImageResponse(AbstractResponse):
    def __init__(self, is_finished: bool = True, is_successful: bool = False, text: str = '',
                 img_url: str = '', img_description: str = '', img_local_path: str = ''):
        super().__init__(is_finished, is_successful, text)
        self._img_url = img_url
        self._img_local_path = img_local_path
        self._img_description = img_description

    def to_key_value_format(self):
        return {
            'text': self._text,
            'img_url': self._img_url,
            'img_local_path': self._img_local_path,
            'img_description': self._img_description
        }

    def __repr__(self):
        return str(self.to_key_value_format())
