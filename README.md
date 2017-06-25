The original problem statement can be found here: https://github.com/sflydwh/code-challenge


## Problem Statement, reduced:

The goal of this project is to:

1. Create event data in accordance with a data schema given in the problem statement. 
2. Define a function ingest(e, d) to ingest event data (e) and update data structure (d).
3. Define a function top_x_simple_ltv_customers(x, d) to return the Lifetime Value (“LTV”) of the top x customers based on data in d.
4. Call functions to produce output.


## Assumptions about the Problem:

- The problem statement doesn't say how much input data to generate. The function GenEvents called in main() has the keyword argument 'number_events' which can be set to generate a number of random events.
- For simplicity, there's no special handling of New or Update verbs. Whenever a CUSTOMER event occurs, it is added to the CUSTOMER event list for that customer. More data processing and some exception handling is needed to ensure updates to customer profiles occur in order. However, this special handling was not required to solve the stated problem.
- It is not known how records need to be sorted by future calling analytics functions; therefore, the data structure (d) event records are categorized by customer_id and event type, but left unsorted with these categories.
- It is not known under what conditions a join of an ORDER event and a SITE_VISIT event should occur. The timestamps of these can differ.
  - What is the acceptable range of time to say a site visit results in an order? (SITE_VISIT event_time - ORDER event_time)
  - What if there is no site visit event recorded, but an order occurred? Does this ever happen? Exception handling for divide by zero error is needed.
  - How should repeat events be handled? (Ex: Avoid joining one order to multiple site visits, and handle case when multiple orders result from a single site visit).
- The event data has been left 'intact' within data structure d; that is, no duplicate keys (ex: customer_id, event_type) were deleted from the dictionary event object added to d during the ingest(e, d) task. This may make it easier to recreate the original input data in the future, if needed.


## How to run Solution:

#### Generate Events

The last created events are saved in the input/input.txt file. 100 new events for 10 users can be created by running:

    python src/EventGen.py 100

Feel free to use any number in the command line argument to tailor the desired number of random events for 10 users. The default is 1. To update the number of users to generate events for, the user_names end range in the generate_event function can be updated (line 22, EventGen.py). Be sure to use a number large enough to support analytic functions in the Solution, but small enough that users are likely to be assigned many events.

#### Run Analytics

Once the desired json event data is in the input/input.txt file, the following command can be run:

    python src/Solution.py

This script calls the ingest(e, d) function to ingest the event (e) input data into data structure (d). It then automatically calls top_x_simple_ltv_customers(x, d) in the main() method, with x=5 by default. Feel free to change this x value in the top_x_simple_ltv_customers(x, d) function call (at Solution.py, line 79) to any positive integer.

#### Output

The output of the Solution's top_x_simple_ltv_customers function is saved in output/output.txt in json format. The output contains a list of dictionary key-value pairs of the form {customer_id: ltv}.

#### Testing and Further Analysis

An ipython notebook file named "Verification and Visualization with Pandas and Matplotlib.ipynb" independently calculates LTV for all customers, and shows results which mirror those of the Solution.py output. This is done for testing purposes, but also to try out some visualizations.


## Performance:

The data structure (d) is a json nested dictionary structure.

The function ingest(e, d) iterates over every dictionary item listed in the input file. It then checks if a key for the customer_id and event_type is already in data structure d before creating the key or appending the event to the key's value in d. The time complexity for this task is O(n).

The function top_x_simple_ltv_customers(x, d) iterates over every customer record to get order sales total per customer and total site visits per customer (O(n)). However, it also performs a sort on the result list of customers in O(n * log(n)) time. The time complexity of the function is then O(n * log(n)).


## Future Improvements:

- Define Visit Class with properties for total_sale (customer expenditures) per visit. (Will need to define parameters to correlate ORDER event_time and SITE_VISIT event_time).
- Define Customer Class with properties for name, address, visits, and orders.
- Sort events collected within each category by event_time in d to more efficiently support time-dependent, transactional analytics functions.
- Explore alternatives to changing state of variables - get away from global variables.
- Improve sample event generating functions (if needed); for example, make # of user_names created equal to some random number in the range of (1, number_events/4).