from collections import defaultdict
from typing import Tuple, List
from navigation.models import Place


class RouteBuilderError(Exception):
    pass


class RouteBuilder:
    def __init__(self, neighbors: List[Tuple[Place, Place]]):
        self._places, self._neighbors = [], defaultdict(list)
        for place_1, place_2 in neighbors:
            try:
                index_1 = self._places.index(place_1)
            except ValueError:
                self._places.append(place_1)
                index_1 = len(self._places) - 1

            try:
                index_2 = self._places.index(place_2)
            except ValueError:
                self._places.append(place_2)
                index_2 = len(self._places) - 1

            self._neighbors[index_1].append(index_2)
            self._neighbors[index_2].append(index_1)

    def _get_bfs_result(self, from_place: Place, to_place: Place):
        queue = [(self._places.index(from_place), -1)]
        parent, is_visited = [-1] * len(self._places), [False] * len(self._places)
        while len(queue) > 0:
            place_index, parent_index = queue.pop(0)
            if is_visited[place_index]:
                continue
            is_visited[place_index] = True
            parent[place_index] = parent_index
            queue.extend((index, place_index) for index in self._neighbors[place_index])

            if self._places[place_index] == to_place:
                return place_index, parent
        return None, None

    def get_nearest_route(self, from_place: Place, to_place: Place) -> List[Place]:
        """without cycles implementation"""

        if from_place not in self._places:
            raise ValueError('from_place not in index')
        if to_place not in self._places:
            raise ValueError('to_place not in index')

        place_index, parent = self._get_bfs_result(from_place, to_place)
        if place_index is None:
            raise RouteBuilderError('there is no possible route')

        route = []
        while place_index != -1:
            route.append(self._places[place_index])
            place_index = parent[place_index]
        return list(reversed(route))
