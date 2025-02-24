import pprint
from io import BytesIO
from PIL import Image
from geocode import *
import argparse

address_default = 'тольятти проспект Степана Разина 41'

# argparse
parser = argparse.ArgumentParser()
parser.add_argument('address', nargs='?')
args = parser.parse_args()
if args.address:
    toponym_to_find = args.address
else:
    print(f'Выбран адрес по умолчанию: {address_default}')
    toponym_to_find = address_default

# main
ll_by_set_address = get_ll(toponym_to_find)
search_params = {
    "text": "аптека",
    "lang": "ru_RU",
    "ll": f'{ll_by_set_address[0]},{ll_by_set_address[1]}',
    "type": "biz"
}
response_geosearch = get_org(search_params)
features_from_search = response_geosearch.json()['features']
labels = [f'{ll_by_set_address[0]},{ll_by_set_address[1]},pm2al']

for i in range(10):
    properties = features_from_search[i]['properties']
    try:
        hours = properties['CompanyMetaData']['Hours']['text']
    except Exception:
        color = 'gr'
    else:
        if 'круглосуточно' in hours:
            color = 'gn'
        else:
            color = 'bl'
    ll_pharmacy = features_from_search[i]['geometry']['coordinates']
    label = f'{ll_pharmacy[0]},{ll_pharmacy[1]},pm{color}s'
    labels.append(label)
    # print(label) # log

    snippet = (f'Сниппет:    Время работы - {hours}')
    # print(snippet, '\n') # log

map_params = {
    'pt': '~'.join(labels)
}
response_static = get_map(map_params)
im = BytesIO(response_static.content)
opened_image = Image.open(im)
opened_image.show()
