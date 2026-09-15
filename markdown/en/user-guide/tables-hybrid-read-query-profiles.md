# Analyze query profiles for hybrid tables

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

Unistore workloads pose some interesting questions about query execution that you can investigate by using the Snowsight Query Profile
feature or information gleaned from [EXPLAIN](/sql-reference/sql/explain) output. In addition to monitoring overall performance and throughput, you
may want to know if a table scan is being executed against the row store or object storage, or whether a specific secondary index is being used.

This section identifies **Query Profile** operators and attributes that pertain to hybrid table operations and presents some examples to help
you understand how to read query plans that access hybrid tables. See also [Monitor query activity with Query History](/user-guide/ui-snowsight-activity).

## Hybrid table scans and index scans

Table and index scan operators appear in query profiles to show access to hybrid tables. These operators typically appear at
the bottom of the tree, representing the first step in reading the data that is needed to execute a specific query. Queries against standard
tables always use table scans; they do not use index scans.

When a primary key index is used to scan a hybrid table, a **TableScan** operator appears in the query profile, not an
**IndexScan** operator. When any other index is used to scan a hybrid table, such as a secondary index, you will see an **IndexScan** operator.

Under **Attributes** for the **IndexScan** operator, you can see the fully qualified name of the index and
**Access predicates**. These are the predicates that are applied to the index during the scan. You can also see predicates for
filters that are applied during table scans.

When a predicate is “pushed” to an index, the predicate contains a placeholder, inside parentheses, for the constant that was used in the query.
For example: `SENSOR_DATA_DEVICE2.DEVICE_ID = (:SFAP_PRE_NR_1)`

### Scan mode

Hybrid table data is maintained in two formats to serve both operational and analytical workloads. A common question asked by administrators is
whether a given query will access the row store or the column store (object storage). A query may read from one or both types of storage,
depending on the tables in question, the specific requirements of the query, availability of indexes, and other factors.

The query profile for hybrid table queries includes a **Scan Mode** attribute for each table scan operator in the tree:

- **ROW-BASED**: The query reads from the table data in the row store, or uses indexes to compute query results.
- **COLUMN-BASED**: The query reads from an object storage copy of the same data that was loaded into the row store. Index scans can also access
  object storage, for [Time Travel](/user-guide/data-time-travel) queries.

Scan mode is specific to hybrid tables. If a table scan is run on a standard table, no **Scan Mode** attribute is displayed.

### Data read from the columnar warehouse cache

Where possible, table scans for hybrid tables read data from a columnar warehouse cache. This cache is an extension to the standard warehouse cache; see [Optimizing the warehouse cache](/user-guide/performance-query-warehouse-cache). The cache contains data that has been read from the hybrid table storage provider and is
accessible by read-only queries against hybrid tables.

To see cache usage in a given query profile, select the table scan operator and check the **Percentage scanned from cache** under **Statistics**.

Queries that select from hybrid tables do not benefit from the [query results cache](/user-guide/querying-persisted-results).

## Throttling for hybrid table requests

In the **Profile Overview**, you can see a **Hybrid Table Requests Throttling** percentage. To see this overview, do not select an operator in
the tree; the overview applies to the whole query plan.

For example, the following query recorded that 87.5% of its execution time was spent being
throttled by the hybrid table storage provider. A high throttling percentage is an indicator that too many hybrid table read and write requests are
being sent to the storage provider, relative to the quota for the database. For more information, see
[Quotas and throttling](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-ht-quotas-throttling).

![Query profile overview shows a high throttling percentage for hybrid table requests.](/static/images/screens/hybrid_table_profile_overview_throttling.png)

## Examples

The following Snowsight examples of query profiles show attributes specific to hybrid table
operations. To understand these examples, you do not need to create and load the tables that are queried and modified. However,
here is the CREATE TABLE statement for one of the tables for reference. Note the definition of the PRIMARY KEY constraint (on the
`timestamp` column) and a secondary index (on the `device_id` column):

Copy code

```
CREATE OR REPLACE HYBRID TABLE sensor_data_device1 (
  timestamp TIMESTAMP_NTZ PRIMARY KEY,
  device_id VARCHAR(10),
  temperature DECIMAL(6,4),
  vibration DECIMAL(6,4),
  motor_rpm INT,
  INDEX device_idx(device_id)
 );
```

Another similar hybrid table, `sensor_data_device2`, is also used in the examples.

### Query plan that accesses the primary key column

When your query filters the primary key of the table (`timestamp`), which is automatically indexed, the query profile uses a
**TableScan** operator. Also note that **ROW\_BASED** scan mode is used for this query.

Copy code

```
SELECT * FROM sensor_data_device1 WHERE timestamp='2024-03-01 13:45:56.000';
```

![TableScan operator for query that filters on the primary key column, timestamp](/static/images/screens/table_scan_pk_row_based.png)

### Query plan that accesses a secondary index

The query that generated this profile looks like this:

Copy code

```
SELECT COUNT(*) FROM sensor_data_device1 WHERE device_id='DEVICE2';
```

Only part of the profile is shown here, focusing on the **IndexScan** operator and its attributes.
The scan mode is **ROW\_BASED**, and you can see the complete predicate by hovering over **Access Predicates**.
The fully qualified index name is also displayed.

![IndexScan operator with attributes, including access predicate and ROW_BASED scan mode](/static/images/screens/secondary_index_scan_with_access_predicate.png)

See also [INCLUDE columns](/user-guide/tables-hybrid-index#label-indexes-with-include-columns).

### Query plan for DML on a hybrid table

DML operations on hybrid tables typically modify single rows. For example:

Copy code

```
UPDATE sensor_data_device2 SET device_id='DEVICE3' WHERE timestamp = '2024-04-02 00:00:05.000';
```

The query profile for the **TableScan** operator shows that this UPDATE accesses the row store for the
hybrid table (scan mode is **ROW\_BASED**):

![Table scan operator that uses a ROW_BASED scan for a single-row UPDATE](/static/images/screens/single_row_update_table_scan.png)

### Recurring query that benefits from cached data

In this case, assume that the following query is run twice in quick succession on a hybrid table.

Copy code

```
SELECT device_id, AVG(temperature)
  FROM sensor_data_device2
  WHERE temperature>33
  GROUP BY device_id;
```

The first query reads all of the data from object storage. The second run of the query reads 100% of the data from the columnar cache.
Also note that the scan mode for this query is **COLUMN\_BASED**.

![Table scan operator that read 100% of the data from the cache](/static/images/screens/table_scan_cached_100_percent.png)

### Query plan for a join (hybrid table to standard table)

When you join a hybrid table to a standard table, you will see a **Scan Mode** attribute for the scan on the hybrid table, but not on
the standard table. For example, the **TableScan** operator on the left side of this join plan used **ROW\_BASED** scan mode. The `order_header`
table is a hybrid table with `order_id` as its primary key (the joining column in this example). The other table, `truck_history`, is a standard table.

![TableScan operator for a hybrid table in a join, including access predicate and ROW_BASED scan mode](/static/images/screens/table_scan_join_hybrid_table.png)
