from io import BytesIO
from PIL import Image
from geocode import *
from distance import lonlat_distance
import argparse

address_default = 'тольятти проспект Степана Разина 41'

parser = argparse.ArgumentParser()
parser.add_argument('address', nargs='?')
args = parser.parse_args()
if args.address:
    toponym_to_find = args.address
else:
    print(f'Выбран адрес по умолчанию: {address_default}')
    toponym_to_find = address_default

ll_one = get_ll(toponym_to_find)
search_params = {
    "text": "аптека",
    "lang": "ru_RU",
    "ll": f'{ll_one[0]},{ll_one[1]}',
    "type": "biz"
}
response_geosearch = get_org(search_params)
properties = response_geosearch.json()['features'][0]['properties']
address = properties['CompanyMetaData']['address']
name = properties['CompanyMetaData']['name']
hours = properties['CompanyMetaData']['Hours']['text']

ll_two = response_geosearch.json()['features'][0]['geometry']['coordinates']
label_one = f'{ll_one[0]},{ll_one[1]},pm2al'
label_two = f'{ll_two[0]},{ll_two[1]},pm2bl'
labels = f'{label_one}~{label_two}'

map_params = {
    'pt': labels
}
snippet = (f'Сниппет:\n'
           f'    Название - {name}\n'
           f'    Адрес - {address}\n'
           f'    Время работы - {hours}\n'
           f'    Расстоние - {round(lonlat_distance(ll_one, ll_two))} м.')
print(snippet)

response_static = get_map(map_params)
im = BytesIO(response_static.content)
opened_image = Image.open(im)
opened_image.show()
