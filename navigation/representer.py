import abc
from typing import List, Any, Tuple
from navigation.models import Place
from PIL import Image, ImageDraw

from navigation.route_builder import RouteBuilder
from navigation.data.main_floor_1 import NEIGHBOR_PLACES, entrance, hall_6
import math

ANGLE = math.pi / 4


def draw_arrow(draw_obj: ImageDraw.Draw,
               start: Tuple[int, int],
               end: Tuple[int, int],
               mustache_length: int = 10,
               width: int = 2,
               color: Tuple[int, int, int] = (0, 0, 255)) -> ImageDraw.Draw:
    draw_obj.line([start, end],  fill=color, width=width)
    # draw_obj.line([
    #     (end[0] + (mustache_length * math.cos(ANGLE)), (end[1] + mustache_length * math.sin(ANGLE))),
    #     end,
    #     ((end[0] - mustache_length * math.cos(ANGLE)), (end[1] + mustache_length * math.sin(ANGLE))),
    # ],  fill=color, width=width)
    return draw_obj


def draw_route_on_image(image_path: str, route: List[Place], save_img_path: str):
    im = Image.open(image_path)
    d = ImageDraw.Draw(im)
    for end_index in range(1, len(route)):
        start = route[end_index - 1].image_point_coordinates.to_tuple()
        end = route[end_index].image_point_coordinates.to_tuple()
        d = draw_arrow(d, start, end)
    im.save(save_img_path)


if __name__ == '__main__':
    rb = RouteBuilder(NEIGHBOR_PLACES)
    draw_route_on_image(r"C:\Users\Максим\git\pushkin_guide\navigation\data\main_floor_1.jpg",
                        rb.get_nearest_route(hall_6, entrance),
                        'drawn_grid.png')
