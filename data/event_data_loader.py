import json

with open('events.json', 'r') as f:
    data = json.load(f)
#
data_as_list = [data[key] for key in data]
new_objects = []

for element in data_as_list:
    new_object = {'event_name': element['name']['ru'],
                  'img': element['img_header']['pc'] if element['img_header']['pc'] else element['img_header']['mob'],
                  'price': element['price']['ru'],
                  'extra_img': element['circ_img']['id01'] if 'circ_img' in element else '',
                  'text': element['text']['ru'], 'type': element['type']['ru'], 'dateBegin': element['dateBegin'],
                  'dateEnd': element['dateEnd'], 'halls': element['halls']['ru']}
    new_objects.append(new_object)

# print(new_objects[2])

from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()
index = helpers.bulk(es, new_objects, index='event-index', doc_type='event-events')
