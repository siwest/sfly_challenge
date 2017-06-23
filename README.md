The original problem statement can be found here: https://github.com/sflydwh/code-challenge


### Problem Statement, reduced:

The goal of this project is to:

#. Create event data IAW data schema given in problem statement. 
#. Define Ingest(e,D) function to ingest event data. 
#. Define TopXSimpleLTVCustomers(x, D) function to calculate the Lifetime Value (“LTV”) of a customer based on data in D.
#. Call functions to produce output.


### Assumptions about the Problem:

#. We don't know how much input data we need to generate. The function GenEvents called in main() has the keyword argument 'number_events' which can be set to generate a number of random events.
#. New Customer Update Rule: For simplicity, New or Update verbs are treated as the same create or update instruction. There's no check to ensure a record exists before it is updated. Some exception handling is needed.
#. We don't know how records will ultimately be sorted by calling analytics functions, so we leave the event records categorized by customer_id and event type, but leave the records within these categories unsorted.
#. We don't know how the range of timestamps to use to correlate ORDER event_time and SITE_VISIT event_time fields needed to calculate average customer value per week (order expenditure / site_visit event). 

  - We could probably use 1 hour windows, but what if there are multiple site visits in one day? 
  - Could there be a case where no site visit occurred by a customer, yet there was an order by the customer? Exception handling for divide by zero error is needed.


### Performance:

Lookup by customer is O(1) (on average) for dictionaries.


### Optimizations:

- Define Visit Class with properties for total_sale (customer expenditures) per visit. (Will need to define parameters to correlate ORDER event_time and SITE_VISIT event_time).
- Define Customer Class with properties for name, address, visits, and orders.