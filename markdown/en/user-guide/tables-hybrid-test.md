# Performance testing

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This topic provides information for testing [hybrid tables](/user-guide/tables-hybrid) in Snowflake. When
evaluating hybrid tables for the first time in your environment, you will likely want to do some basic performance
testing. This section refers to the
[getting started with hybrid tables tutorial](/user-guide/tutorials/getting-started-with-hybrid-tables-tutorial). If
you have not completed that tutorial, now is a good time to do so.

Attention

Performance statistics reported in Snowsight are not indicative of query performance for driver-based workloads.

## Understand your use case

Testing for the outcome you are looking for is very important. Understanding how hybrid tables will augment
your architecture is important when designing your tests.

Design your test scenario:

- Do you require a high volume of UPDATE, INSERT, or DELETE statements?
- Does your application need fast access to indexed data?
- Do you have batch jobs you would like to run more often without impacting SELECT performance?
- What do you want to measure during the test?

## Select a test framework

Performance testing frameworks are ubiquitous in software development. Most customers have testing frameworks that
are already in place and can be used to test hybrid tables. Regardless of the test framework you select,
it needs to be able to:

- Authenticate with Snowflake using shared key authentication
- Support multi-threaded query execution
- Issue queries as prepared statements, binding variables as needed
- Create a mix of INSERT, UPDATE, DELETE, and SELECT queries

Ideally, your framework will track query execution time for each request in each thread to calculate:

- Total query throughput
- Min, max, average, and standard deviation of response time
- Total bytes received per query

## Execute the test

The hybrid tables query optimizer takes some time to “warm up” and establish a steady-state latency. This
warm-up period can vary based on the amount of data, the number of indexes, and the complexity of the query.
For most test cases, a warm-up period of 1-2 minutes is sufficient. Longer warm-up periods may be required.

Tip

The warm-up period ends when the throughput and latency curves converge to a steady state.

This is a typical performance test result for random queries on a single hybrid table. Note that the
performance improves over time and achieves a steady state after a few seconds:

![Hybrid tables performance test curves](/static/images/screens/hybrid_tables_performance_test_result.png)

Note

The time to achieve steady-state response times varies depending on many factors and can take
several minutes.
