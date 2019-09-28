from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.text_based import SingleTextResponse


class AboutArtistAction(AbstractAction):
    recognized_types = [TextQuery]

    def activation_response(self, initial_query: object) -> ActivationResponse:
        pass

    def reply(self, query: TextQuery = None) -> SingleTextResponse:
        pass