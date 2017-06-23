import json
import os

IN_FILE = os.path.join(os.getcwd(), 'input/input.txt')
OUT_FILE = os.path.join(os.getcwd(), 'output/output.txt')
D = {}


def ingest(e, d):
    """
    Given event e, update data d
    """
    event_type = e['type']
    if 'CUSTOMER' == event_type:
        customer_id = e['key']
    else:
        customer_id = e['customer_id']

    if customer_id not in d:
        d[customer_id] = {event_type: [e]}
    else:
        if event_type not in d[customer_id]:
            d[customer_id][event_type] = [e]
        else:
            d[customer_id][event_type].append(e)
    return d


def top_x_simple_ltv_customers(x, d):
    """
    Return the top x customers with the highest Simple Lifetime Value from
        data D. A simple LTV can be calculated using the following equation:
        52(a) x t. Where a is the average customer value per week (customer
        expenditures per visit (USD) x number of site visits per week) and
        t is the average customer lifespan. The average lifespan for
        Shutterfly is 10 years.
    """

    ltv_customer_list = []  # ltv_customer_list is list of [customer_id, ltv] pairs
    for customer_id, record in d.items():
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
        except ZeroDivisionError:  # In an ideal world, not supposed to happen.
            a = 1

        ltv = format(52 * a * 10, '0.2f')  # Format to 2 decimal places.
        ltv_customer_list.append([str(customer_id), ltv])

    # Sort by item at index=1 (ltv) in list [customer_id, ltv].
    sorted_ltv_customer_list = sorted(ltv_customer_list,
                                      key=lambda k: float(k[1]),
                                      reverse=True)[:x]
    output = []
    for elem in sorted_ltv_customer_list:
        output.append({elem[0]: elem[1]})

    output = json.dumps(output, indent=4)
    with open(OUT_FILE, 'w') as f:
        f.write(output)


def main():
    with open(IN_FILE) as f:
        batch = json.load(f)
    # Read each record in batch, and ingest into D.
    for e in batch:
        ingest(e, D)

    top_x_simple_ltv_customers(10, D)


if __name__ == "__main__":
    main()
