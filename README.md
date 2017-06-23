The original problem statement can be found here: https://github.com/sflydwh/code-challenge


### Problem Statement, reduced:

The goal of this project is to:

1. Create event data in accordance with a data schema given in the problem statement. 
2. Define a function ingest(e, d) to ingest event data (e) and update data structure (d).
3. Define a function top_x_simple_ltv_customers(x, d) to return the Lifetime Value (“LTV”) of the top x customers based on data in d.
4. Call functions to produce output.


### Assumptions about the Problem:

- We don't know how much input data we need to generate. The function GenEvents called in main() has the keyword argument 'number_events' which can be set to generate a number of random events.
- New Customer Update Rule: For simplicity, New or Update verbs are treated as the same create or update instruction. There's no check to ensure a record exists before it is updated. Some exception handling is needed.
- We don't know how records will ultimately be sorted by future calling analytics functions, so we leave the event records categorized by customer_id and event type, but leave the records within these categories unsorted.
- We don't know under what conditions we should join and ORDER event with a SITE_VISIT event. The timestamps of these can differ.
  - What is the acceptable range to for a site visit to result in an order? (SITE_VISIT event_time - ORDER event_time)
  - What if there is no site visit event recorded, but an order occurred? Does this ever happen? Exception handling for divide by zero error is needed.
  - What if multiple site visit events are in the batch (perhaps someone did several "refreshes" of the session)? How should repeat events be handled?


### How to run Solution:

#### Generate Events

The last created events are saved in the input/input.txt file. 100 new events can be created by running:

    python src/EventGen.py 100

Feel free to use any number in the command line argument to tailor the desired number of random events.

#### Run Analytics

Once the desired json event data is in the input/input.txt file, the following command can be run:

    python src/Solution.py

This script calls the ingest(e, d) function to ingest the event (e) input data into data structure (d). It then automatically calls top_x_simple_ltv_customers(x, d) in the main() method, with x=5 by default. Feel free to change this x value in the top_x_simple_ltv_customers(x, d) function call (at Solution.py, line 79) to any positive integer.

### Output

The output of the Solution's top_x_simple_ltv_customers function is saved in output/output.txt in json format. The output contains a list of dictionary key-value pairs of the form {customer_id: ltv}.



### Performance:

The data structure (d) is a json nested dictionary structure.

The function ingest(e, d) iterates over every dictionary item listed in the input file. It then checks if a key for the customer_id and event_type is already in data structure d before creating the key or appending the event to the key's value in d. The time complexity for this task is O(n).

The function top_x_simple_ltv_customers(x, d) iterates over every customer record to get order sales total per customer and total site visits per customer (O(n)). However, it also performs a sort on the result list of customers in O(n*log(n)) time. The time complexity of the function is then O(n*log(n)).


### Future Improvements:

- Define Visit Class with properties for total_sale (customer expenditures) per visit. (Will need to define parameters to correlate ORDER event_time and SITE_VISIT event_time).
- Define Customer Class with properties for name, address, visits, and orders.
- Sort events collected within each category by event_time in d to more efficiently support time-dependent, transactional analytics functions.