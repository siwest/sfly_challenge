import os
import json
from pprint import pprint

SAMPLE_IN_FILE = os.path.join(os.getcwd(), 'sample_input/events.txt')
IN_FILE = os.path.join(os.getcwd(), 'input/input.txt')
OUT_FILE = os.path.join(os.getcwd(), 'output/output.txt')
D = {}


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

        a = sum_expenditures / sum_visits
        ltv = format(52 * a * 10, '0.2f')
        ltv_cust_list.append([cust_id, ltv])

    sorted_ltv_cust_list = (sorted(ltv_cust_list,
                                   key=lambda x: x[1],
                                   reverse=True))[:x]
    return sorted_ltv_cust_list


def main():
    with open(SAMPLE_IN_FILE) as f:
        batch = json.load(f)

    for e in batch:
        Ingest(e, D)
    pprint(D)

    for customer in TopXSimpleLTVCustomers(10, D):
        print(customer)

if __name__ == "__main__":
    main()
