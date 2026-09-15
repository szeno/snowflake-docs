# Sample data: TPC-H

As described in the [TPC Benchmark™ H (TPC-H)](http://www.tpc.org/tpch/) specification:

> “TPC-H is a decision support benchmark. It consists of a suite of business-oriented ad hoc queries and concurrent data modifications. The queries and the data populating the database have been chosen
> to have broad industry-wide relevance. This benchmark illustrates decision support systems that examine large volumes of data, execute queries with a high degree of complexity, and give answers to
> critical business questions.”

## Database and schemas

TPC-H comes with various data set sizes to test different scaling factors. For demonstration purposes, we’ve shared four versions of the TPC-H data. The data is provided in the following schemas in the
SNOWFLAKE\_SAMPLE\_DATA shared database:

- TPCH\_SF1: Consists of the base row size (several million elements).
- TPCH\_SF10: Consists of the base row size x 10.
- TPCH\_SF100: Consists of the base row size x 100 (several hundred million elements).
- TPCH\_SF1000: Consists of the base row size x 1000 (several billion elements).

To access the full list of TPC-H queries, download [this script](/static/samples/tpc-h-all-queries.sql).

## Database entities, relationships, and characteristics

The components of TPC-H consist of eight separate and individual tables (the Base Tables). The relationships between columns in these tables are illustrated in the following ER diagram:

> ![Schema for TPC-H benchmark data](/static/images/sample-data-tpch-schema.png)

(source: [TPC Benchmark H Standard Specification](http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v2.17.1.pdf))

## Query definitions

Each TPC-H query asks a business question and includes the corresponding query to answer the question. Some of the TPC-H queries are included in Snowflake’s Get Started tutorials.

This section describes one of the queries. For more information about TPC-H and all the queries that are involved, see the official
[TPC Benchmark H Standard Specification](http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v2.17.1.pdf).

The [TPC-H script](/static/samples/tpc-h-all-queries.sql), provided by Snowflake, contains the full list of TPC-H queries. You can
save the file to your local file system for reference.

### Q1: Pricing summary report query

This query reports the amount of business that was billed, shipped, and returned.

#### Business question

The Pricing Summary Report Query provides a summary pricing report for all line items that were shipped as of a given date. The date is within 60-120 days of the greatest ship date contained in the database.

#### Functional query definition

The query lists totals for extended price, discounted extended price, discounted extended price plus tax, average quantity, average extended price, and average discount. These aggregates are grouped by
RETURNFLAG and LINESTATUS, and listed in ascending order of RETURNFLAG and LINESTATUS. A count of the number of line items in each group is included:

> Copy code
>
> ```
> use schema snowflake_sample_data.tpch_sf1;   -- or snowflake_sample_data.{tpch_sf10 | tpch_sf100 | tpch_sf1000}
>
> select
>        l_returnflag,
>        l_linestatus,
>        sum(l_quantity) as sum_qty,
>        sum(l_extendedprice) as sum_base_price,
>        sum(l_extendedprice * (1-l_discount)) as sum_disc_price,
>        sum(l_extendedprice * (1-l_discount) * (1+l_tax)) as sum_charge,
>        avg(l_quantity) as avg_qty,
>        avg(l_extendedprice) as avg_price,
>        avg(l_discount) as avg_disc,
>        count(*) as count_order
>  from
>        lineitem
>  where
>        l_shipdate <= dateadd(day, -90, to_date('1998-12-01'))
>  group by
>        l_returnflag,
>        l_linestatus
>  order by
>        l_returnflag,
>        l_linestatus;
> ```

## Recommendations

Use the following recommendations to explore the sample data and compare query performance across runs.

### Set your database and schema

Set your session context to the sample database and to the schema for the scale factor you want to test. After you set
the context, you can refer to the tables by name without qualifying them:

Copy code

```
use database snowflake_sample_data;
use schema tpch_sf1;   -- or tpch_sf10, tpch_sf100, tpch_sf1000
```

### Tag your session

Set a query tag on your session so that you can easily find your queries later in Query History:

Copy code

```
alter session set query_tag = 'tpch_test';
```

### Run multiple passes

Run all 22 queries from the [TPC-H script](/static/samples/tpc-h-all-queries.sql) three times in succession (three
passes), then repeat the full set of passes a couple of times to confirm that the results are consistent.

To make sure that each pass runs the query instead of returning a cached result, turn off the query result cache for
your session:

Copy code

```
alter session set use_cached_result = false;
```

### Inspect the results

After your runs finish, open [Query History](/user-guide/ui-snowsight-activity) in Snowsight and use the
**Duration** column to inspect the elapsed time for each query. Filter by the query tag that you set to quickly find
your TPC-H queries.

You can also query the [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) in the ACCOUNT\_USAGE schema of
the shared SNOWFLAKE database. Filter on the query tag that you set and review the TOTAL\_ELAPSED\_TIME column (in
milliseconds) for each query:

Copy code

```
select query_text, warehouse_name, total_elapsed_time, execution_time, start_time
from snowflake.account_usage.query_history
where query_tag = 'tpch_test'
order by start_time;
```

Account usage views can have some latency, so recently completed queries might not appear right away.

Tip

To explore your query history conversationally, you can use [Cortex Code](/user-guide/cortex-code/cortex-code),
Snowflake’s AI coding agent, to write and refine these queries for you.

## Run the queries on interactive tables and warehouses

[Snowflake interactive tables and interactive warehouses](/user-guide/interactive) are optimized for low-latency,
high-concurrency queries. You can run the 22 TPC-H queries on interactive tables to compare their performance against
standard tables.

Because the SNOWFLAKE\_SAMPLE\_DATA database is read-only, first copy the sample data into your own tables. To compare
results, create two sets of tables: a standard set as a baseline and an interactive set. When you create the
interactive tables, cluster each one on the column that the queries filter or join on most:

- LINEITEM: cluster by L\_SHIPDATE.
- ORDERS: cluster by O\_ORDERDATE.
- CUSTOMER, PART, PARTSUPP, SUPPLIER, NATION, and REGION: cluster by the primary key column.

Then create an interactive warehouse, attach the eight interactive tables, and set a standard warehouse as its fallback
so that any query that exceeds the interactive query timeout reruns automatically. Run the
[TPC-H queries](/static/samples/tpc-h-all-queries.sql) against the standard tables and the interactive tables
separately, then compare the elapsed times.

For the full procedure, including how to create interactive tables and warehouses, configure a fallback warehouse, and
follow benchmarking best practices such as turning off the result cache and waiting for the cache to warm, see
[Snowflake interactive tables and interactive warehouses](/user-guide/interactive) and
[benchmarking best practices for interactive tables](/user-guide/interactive#benchmarking-best-practices).
