# Sample data sets

Snowflake provides sample data sets, such as the industry-standard TPC-DS and TPC-H benchmarks, for evaluating and testing a broad range of Snowflake’s SQL support.

Sample data sets are provided in a database named SNOWFLAKE\_SAMPLE\_DATA that has been
[shared with your account](/user-guide/data-sharing-intro) from the Snowflake SFC\_SAMPLES account.
If you do not see the database, you can create it yourself. Refer to [Use the sample database](/user-guide/sample-data-using).

The database contains a schema for each data set, with the sample data stored in the tables in each schema. The database and schemas
do not use any data storage so they do not incur storage charges for your account. You can execute queries on the tables in
these databases just as you would with any other databases in your account. Executing queries requires a running, current warehouse
for your session, which consumes credits.

**Next Topics:**

- [Use the sample database](/user-guide/sample-data-using)
- [Sample data: TPC-DS](/user-guide/sample-data-tpcds)
- [Sample data: TPC-H](/user-guide/sample-data-tpch)
- [Sample Data: OpenWeatherMap — Deprecated](/user-guide/sample-data-openweathermap)
