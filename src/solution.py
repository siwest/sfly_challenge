import os
import json
from pprint import pprint
import random
import hashlib
from datetime import datetime
import random

SAMPLE_IN_FILE = os.path.join(os.getcwd(), 'sample_input/events.txt')
IN_FILE = os.path.join(os.getcwd(), 'input/input.txt')
OUT_FILE = os.path.join(os.getcwd(), 'output/output.txt')
D = {}


def GenEvent():
    event = {}
    event_type = random.choice(['CUSTOMER', 'ORDER', 'IMAGE', 'SITE_VISIT'])
    user_name = 'user' + str(random.choice(range(1, 10)))
    uhash = hashlib.sha1(user_name.encode('utf-8')).hexdigest()[:12]

    year = 2017
    month = 6
    day = random.randint(1, 7)  # Will only look at one week
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    sec = random.randint(0, 59)
    date = str(datetime(year, month, day, hour, minute, sec).isoformat()) + 'Z'
    event['event_time'] = date

    if event_type is 'CUSTOMER':
        event['key'] = uhash
        event['type'] = 'CUSTOMER'
        event['verb'] = random.choice(['NEW', 'UPDATE'])
        event['last_name'] = random.choice(['Peter', 'West', 'Lucy', None])
        event['adr_city'] = random.choice(['Middletown', 'Portland',
                                           'Lockhaven', None])
        event['adr_state'] = random.choice(['CA', 'MD', 'NJ', None])
    elif event_type is 'SITE_VISIT':
        event['key'] = uhash
        event['type'] = 'SITE_VISIT'
        event['verb'] = 'NEW'
        event['customer_id'] = uhash
    elif event_type is 'IMAGE':
        event['key'] = uhash
        event['type'] = 'IMAGE'
        event['verb'] = 'UPLOAD'
        event['customer_id'] = uhash
        event['camera_make'] = random.choice(['Nokia', 'Kodak'])
    elif event_type is 'ORDER':
        event['key'] = uhash
        event['type'] = 'ORDER'
        event['verb'] = random.choice(['NEW', 'UPDATE'])
        event['customer_id'] = uhash
        event['total_amount'] = str(random.randint(1, 10000)) + " USD"
    return event


def GenEvents(number_events=1):
    batch = []
    for i in range(number_events):
        generated_event = GenEvent()
        batch.append(generated_event)
    batch = json.dumps(batch)
    loaded_batch = json.loads(batch)
    with open(IN_FILE, 'w') as f:
        json.dump(loaded_batch, f)


def Ingest(e, D):
    '''
    Given event e, update data D
    '''
    event_type = e['type']
    del e['type']
    if 'CUSTOMER' == event_type:
        cust_id = e['key']
        del e['key']
    else:
        cust_id = e['customer_id']
        del e['customer_id']

    if cust_id not in D:
        D[cust_id] = {event_type: [e]}
    else:
        if event_type not in D[cust_id]:
            D[cust_id][event_type] = [e]
        else:
            D[cust_id][event_type].append(e)
    return D


def TopXSimpleLTVCustomers(x, D):
    '''
    Return the top x customers with the highest Simple Lifetime Value from
    data D.
    A simple LTV can be calculated using the following equation: 52(a) x t.
    Where a is the average customer value per week (customer expenditures per
        visit (USD) x number of site visits per week) and t is the average
        customer lifespan. The average lifespan for Shutterfly is 10 years.
    '''

    ltv_cust_list = []
    for cust_id, record in D.items():
        sum_expenditures = 0
        sum_visits = 0

        if 'ORDER' in record:
            for order in record['ORDER']:
                sum_expenditures += float(order['total_amount']
                                          .replace(" USD", ""))
        if 'SITE_VISIT' in record:
            sum_visits += len(record['SITE_VISIT'])

        try:
            a = sum_expenditures / sum_visits
        except ZeroDivisionError:  # In an ideal world, not supposed to happen
            a = 1
        ltv = format(52 * a * 10, '0.2f')
        ltv_cust_list.append([str(cust_id), ltv])

    sorted_ltv_cust_list = sorted(ltv_cust_list,
                                  key=lambda k: float(k[1]),
                                  reverse=True)[:x]
    output = []
    for elem in sorted_ltv_cust_list:
        output.append({elem[0]: elem[1]})

    output = json.dumps(output, indent=4)
    with open(OUT_FILE, 'w') as f:
        f.write(output)


def main():
    GenEvents(number_events=100)
    with open(IN_FILE) as f:
        batch = json.load(f)
    for e in batch:
        Ingest(e, D)

    TopXSimpleLTVCustomers(5, D)


if __name__ == "__main__":
    main()
