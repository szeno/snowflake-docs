# May 01, 2025: Dynamic tables: Support for filtering by current time and date for incremental refresh (*General availability*)

We are pleased to announce support for using the [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp), [CURRENT\_DATE](/sql-reference/functions/current_date),
and [CURRENT\_TIME](/sql-reference/functions/current_time) functions and their aliases as a filter for dynamic tables in incremental refresh
mode.

You can now use these functions inside of predicates such as a WHERE/HAVING/QUALIFY clause.

For example:

Copy code

```
CREATE TABLE my_table
 AS
  SELECT column1 AS id, parse_json(column2) AS entity, current_timestamp() as event_timestamp
  FROM values
  (12712555,
  '{ name:  { first: "John", last: "Smith"},
   contact: [
   { business:[
   { type: "phone", content:"555-1234" },
   { type: "email", content:"j.smith@example.com" } ] } ] }'),
  (98127771,
  '{ name:  { first: "Jane", last: "Doe"},
   contact: [
   { business:[
   { type: "phone", content:"555-1236" },
   { type: "email", content:"j.doe@example.com" } ] } ] }') v;

CREATE DYNAMIC TABLE my_dynamic_table
 TARGET_LAG = DOWNSTREAM
 WAREHOUSE = mywh
 REFRESH_MODE = INCREMENTAL
 AS
  SELECT id, entity, event_timestamp
  FROM my_table
  WHERE event_timestamp > timestampadd(month, -1, current_timestamp);
```

To use these functions, you must explicitly [set your dynamic table’s refresh mode to INCREMENTAL](/sql-reference/sql/create-dynamic-table#label-create-dt-refresh-mode).
