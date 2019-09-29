from navigation.models import ImagePointCoordinates, Place, Hall
from navigation.route_builder import RouteBuilder


main_museum = 'Главное здание'
entrance = Place(
    museum=main_museum,
    floor=1,
    area='Вход',
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=440, y=330),
)
hall_1 = Place(
    museum=main_museum,
    floor=1,
    area=Hall(number='1', title='Искусство Древнего Египта'),
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=320, y=400),
)
hall_2 = Place(
    museum=main_museum,
    floor=1,
    area=Hall(number='2', title='Искусство Древнего Ближнего Востока'),
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=250, y=340),
)
hall_3 = Place(
    museum=main_museum,
    floor=1,
    area=Hall(number='3', title='Древняя Троя и раскопки Г. Шлимана'),
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=170, y=265),
)
hall_4 = Place(
    museum=main_museum,
    floor=1,
    area=Hall(number='4', title='Античное искусство. Кипр. Древняя Греция. Этрурия. Древний Рим'),
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=95, y=210),
)
hall_5 = Place(
    museum=main_museum,
    floor=1,
    area=Hall(number='5', title='Искусство Северного Причерноморья'),
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=38, y=150),
)
hall_6 = Place(
    museum=main_museum,
    floor=1,
    area=Hall(number='6', title='Эллинистический и римский Египет, коптское искусство'),
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=212, y=243),
)
intermediate_point_1 = Place(
    museum=main_museum,
    floor=1,
    area='intermediate_point_1',
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=305, y=200),
)
hall_7 = Place(
    museum=main_museum,
    floor=1,
    area=Hall(number='27', title='Византийское искусство. Искусство Италии XIII-XVI веков'),
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=276, y=160),
)
intermediate_point_2 = Place(
    museum=main_museum,
    floor=1,
    area='intermediate_point_2',
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=330, y=280),
)

hall_14 = Place(
    museum=main_museum,
    floor=1,
    area=Hall(number='14', title='Греческий дворик'),
    object=None,
    image_point_coordinates=ImagePointCoordinates(x=270, y=300),
)

HALLS = [hall_1, hall_2, hall_3, hall_4, hall_5, hall_6, hall_7, hall_14]

NEIGHBOR_PLACES = [
    (entrance, hall_1),
    (hall_2, hall_1),
    (hall_2, hall_3),
    (hall_4, hall_3),
    (hall_4, hall_5),
    (hall_3, hall_6),
    (intermediate_point_1, hall_6),
    (intermediate_point_1, hall_7),
    (intermediate_point_2, intermediate_point_1),
    (intermediate_point_2, hall_14),
    (intermediate_point_2, entrance),
]
