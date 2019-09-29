import json
import os
from typing import Dict, Union, List

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.queries.image import ImageQuery
from dialogue_system.responses.text_based import SingleTextResponse, SingleTextWithFactAttachments
from dialogue_system.responses.image_based import SingleImageResponse
from slots.slot import Slot
from navigation.route_builder import RouteBuilder, RouteBuilderError
from navigation.data.main_floor_1 import NEIGHBOR_PLACES, HALLS
from navigation.models import Place
from navigation.representer import draw_route_on_image


class InsideNavigationAction(AbstractAction):
    PREVIOUS_LOCATION_LOG_PATH = os.path.join('data', 'previous_location_log.json')
    MAP_IMAGE_PATH = os.path.join('navigation', 'data', 'main_floor_1.jpg')
    SAVE_IMAGE_PATH = os.path.join('navigation', 'data', 'route.jpg')
    recognized_types = [TextQuery, ImageQuery]
    triggering_phrases = ['как пройти', 'как найти', 'где картина', 'где зал', 'как дойти', 'хочу пойти',
                          'хочу посмотреть', 'хочу найти', 'как попасть']

    FALLBACK_RESPONSE = SingleTextResponse(is_finished=True,
                                     is_successful=True,
                                     text='Извините, на данный момент я не могу вам помочь с поиском. Но скоро я научусь!')

    @classmethod
    def _get_previous_location(cls, user_id):
        with open(cls.PREVIOUS_LOCATION_LOG_PATH) as f:
            log = json.load(f)
            if user_id in log:
                return log[user_id]

    @classmethod
    def _log_previous_location(cls, user_id, location):
        with open(cls.PREVIOUS_LOCATION_LOG_PATH, 'r') as f:
            log = json.load(f)
            log[user_id] = location
        with open(cls.PREVIOUS_LOCATION_LOG_PATH, 'w', encoding='utf8') as f:
            json.dump(log, f)

    @classmethod
    def _find_corresponding_hall(cls, hall_title):
        for hall in HALLS:
            if hall_title == hall.area.title:
                return hall

    @classmethod
    def _generate_route_text_description(cls, route: List[Place]) -> str:
        description = ['Следуйте моим указаниям!']
        description.append(f'Из зала "{route[0].area.title}" пройдите в зал "{route[1].area.title}".')
        for place in route[2:]:
            description.append(f'Далее - "{place.area.title}"')
        return ' '.join(description)

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        for phrase in cls.triggering_phrases:
            if phrase in initial_query.lower():
                return ActivationResponse(intent_detected=True)

    @classmethod
    def reply(cls, slots: Dict[Slot, str], user_id=None) -> Union[SingleTextWithFactAttachments, SingleTextResponse]:
        hall = slots.get(Slot.HallName)

        if not hall:
            yield cls.FALLBACK_RESPONSE

        previous_location = cls._get_previous_location(user_id)
        previous_location_changed = False

        if previous_location:
            query, slots = yield SingleTextResponse(is_finished=False,
                                             is_successful=True,
                                             text=f'Скажите, находитесь ли вы сейчас в холле "{previous_location}"?')
            if query not in ['да', 'верно', 'ага']:
                previous_location_changed = True

        if previous_location_changed or not previous_location:
            _, slots = yield SingleTextResponse(is_finished=False,
                                             is_successful=True,
                                             text='Пожалуйста, уточните, в каком холле вы сейчас находитесь.')
            previous_location = slots.get(Slot.HallName)
            if not previous_location:
                yield cls.FALLBACK_RESPONSE

        route_builder = RouteBuilder(NEIGHBOR_PLACES)
        from_place = cls._find_corresponding_hall(previous_location)
        to_place = cls._find_corresponding_hall(hall)
        cls._log_previous_location(user_id=user_id, location=hall)
        try:
            route = route_builder.get_nearest_route(from_place=from_place, to_place= to_place)
            if len(route) == 1:
                yield SingleTextResponse(is_finished=True,
                                         is_successful=True,
                                         text='Вы уже на месте!')
            if len(route) <= 3:
                yield SingleTextResponse(is_finished=True,
                                         is_successful=True,
                                         text=cls._generate_route_text_description(route))
            else:
                draw_route_on_image(image_path=cls.MAP_IMAGE_PATH,
                                    route=route,
                                    save_img_path=cls.SAVE_IMAGE_PATH)
                yield SingleImageResponse(is_finished=True,
                                          is_successful=True,
                                          img_local_path=cls.SAVE_IMAGE_PATH,
                                          text='Следуйте проложенному маршруту!')
        except (ValueError, RouteBuilderError):
            yield cls.FALLBACK_RESPONSE
