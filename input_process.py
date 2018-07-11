import json

def process_price(price_str):
    if price_str == 'Negotiable':
        return -1
    price_str = price_str.replace("Rs", "").strip().strip(".").replace(",", "")
    return int(price_str)



with open('houses.json') as f:
    data = json.load(f)

processed_houses = []

for h in data:
    h['price'] = process_price(h['price'])

with open('houses_processed.json', 'w') as f:
    json.dump(data, f)
