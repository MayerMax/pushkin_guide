import json

with open('./data/objects.json', 'r') as f:
    data = json.load(f)
#
data_as_list = [data[key] for key in data]
new_objects = []
for element in data_as_list:
    new_object = {}
    if element['authors']:
        new_object['about_author'] = {'name': element['authors']['1']['ru']}

    elif element['collectors']:
        new_object['about_author'] = {'name': element['collectors']['1']['ru']}

    new_object['annotation'] = element['annotation']['ru'] if element['annotation']['ru'] else 'empty'
    new_object['audioguide'] = element['audioguide']['ru'] if element['audioguide']['ru'] else 'empty'
    new_object['building'] = element['building'] if 'building' in element and element['building'] else 'empty'
    new_object['cast'] = element['cast'] if element['cast'] else 'empty'

    if type(element['country']) == dict:
        new_object['country'] = element['country']['ru'] if element['country']['ru'] else 'empty'
    else:
        new_object['country'] = element['country']

    new_object['department'] = element['department'] if element['department'] else 'empty'
    new_object['from'] = element['from']['ru'] if element['from']['ru'] else 'empty'
    new_object['get_year'] = element['get_year'] if element['get_year'] else 'empty'

    if element['gallery']:
        new_object['img'] = element['gallery']['1']['id01']

    new_object['graphics_type'] = element['graphics_type']['ru'] if element['graphics_type'] and element['graphics_type']['ru'] else 'empty'
    new_object['hall'] = element['hall'] if 'hall' in element and element['hall'] else 'empty'
    new_object['material'] = element['material']['ru'] if element['material']['ru'] else 'empty'
    new_object['art_name'] = element['name']['ru'] if element['name']['ru'] else 'empty'
    new_object['get_year'] = element['get_year'] if element['get_year'] else 'empty'
    new_object['period_text'] = element['period']['text'] if element['period']['text'] else 'empty'
    new_object['show_in_collection'] = element['show_in_collection']
    new_object['show_in_hall'] = element['show_in_hall']
    new_object['size'] = element['size']
    new_object['text'] = element['text']['ru']
    new_object['type'] = element['type']['ru']
    new_object['year'] = element['year']

    new_objects.append(new_object)

# print(set([x['from'] for x in new_objects]))

# print([x['graphics_type'] for x in new_objects if x['graphics_type'] != 'empty' ][:10])

from elasticsearch import Elasticsearch, helpers
# #
es = Elasticsearch()
# #
index = helpers.bulk(es, new_objects, index='collection-index', doc_type='people')
