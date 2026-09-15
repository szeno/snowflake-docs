# Mar 02, 2026: Using standard SQL clauses to query semantic views (*General availability*)

The ability to use SQL clauses in a SELECT statement to query a semantic view is now generally available and is no longer in
[Preview](/release-notes/preview-features).

You can specify the name of the semantic view in the FROM clause, rather than specifying the SEMANTIC\_VIEW clause. For
example, the following query specifies the SEMANTIC\_VIEW clause:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    DIMENSIONS customer.customer_market_segment
    METRICS orders.order_average_value
  )
  ORDER BY customer_market_segment;
```

The following statement demonstrates how to execute the same query without specifying the SEMANTIC\_VIEW clause:

Copy code

```
SELECT customer_market_segment, AGG(order_average_value)
  FROM tpch_analysis
  GROUP BY customer_market_segment
  ORDER BY customer_market_segment;
```

For information, see [Specifying the name of the semantic view in the FROM clause](/user-guide/views-semantic/querying#label-semantic-views-querying-standard-sql).
