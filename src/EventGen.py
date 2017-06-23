import hashlib
import json
import os
import random
import sys
from datetime import datetime

IN_FILE = os.path.join(os.getcwd(), 'input/input.txt')


def generate_event():
    """
    Called by generate_events to generate random event data, formatted in accordance
        to project schema definition.
    """
    event = {}

    # Randomly pick an event type.
    event_type = random.choice(['CUSTOMER', 'ORDER', 'IMAGE', 'SITE_VISIT'])

    # Create 10 random user_names
    user_name = 'user' + str(random.choice(range(1, 10)))

    # Create user_name hash; take only first 12 digits of a one-way hash
    user_hash = hashlib.sha1(user_name.encode('utf-8')).hexdigest()[:12]

    # Generate a random ISO-formatted date-time string
    year = 2017
    month = 6
    day = random.randint(1, 7)  # Will only look at one week
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    sec = random.randint(0, 59)
    date = str(datetime(year, month, day, hour, minute, sec).isoformat()) + 'Z'
    event['event_time'] = date

    # Handle each event_type
    if event_type is 'CUSTOMER':
        event['key'] = user_hash
        event['type'] = 'CUSTOMER'
        event['verb'] = random.choice(['NEW', 'UPDATE'])
        event['last_name'] = random.choice(['Peter', 'West', 'Lucy', None])
        event['adr_city'] = random.choice(['Middletown', 'Portland',
                                           'Lockhaven', None])
        event['adr_state'] = random.choice(['CA', 'MD', 'NJ', None])
    elif event_type is 'SITE_VISIT':
        event['key'] = user_hash
        event['type'] = 'SITE_VISIT'
        event['verb'] = 'NEW'
        event['customer_id'] = user_hash
    elif event_type is 'IMAGE':
        event['key'] = user_hash
        event['type'] = 'IMAGE'
        event['verb'] = 'UPLOAD'
        event['customer_id'] = user_hash
        event['camera_make'] = random.choice(['Nokia', 'Kodak'])
    elif event_type is 'ORDER':
        event['key'] = user_hash
        event['type'] = 'ORDER'
        event['verb'] = random.choice(['NEW', 'UPDATE'])
        event['customer_id'] = user_hash
        event['total_amount'] = str(random.randint(1, 10000)) + " USD"
    return event


def generate_events(number_events=1):
    """
    Given a number_events, generates a number of events and writes to json
        string representation of those events to file.
    """

    batch = []
    for i in range(number_events):
        generated_event = generate_event()
        batch.append(generated_event)
    batch = json.dumps(batch)
    loaded_batch = json.loads(batch)
    with open(IN_FILE, 'w') as f:
        json.dump(loaded_batch, f)


def main():
    # Set number_events to generate a number of events.
    generate_events(number_events=int(sys.argv[1]))

if __name__ == "__main__":
    main()