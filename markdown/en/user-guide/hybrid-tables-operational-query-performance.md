# Performance improvements for operational queries on hybrid tables

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Transactional workloads often execute the same short-running statements repeatedly. This public preview introduces additional automatic performance improvements for queries on [hybrid tables](/user-guide/tables-hybrid) that modify or select a small number of rows and execute in less than 100 ms. We refer to these queries as “operational queries”.

This optimization improves latency and throughput under very high query loads by reducing the setup costs for processing each query. It builds upon the existing hybrid table features that already remove much of the per-query overhead from parsing, plan compilation, and optimization through reuse and caching. Snowflake automatically recognizes recurring, structurally consistent query patterns and optimizes their execution, delivering significantly
lower latency and better price-performance for operational workloads.

## Enable operational query optimizations

To enable this public preview, set the `ENABLE_USE_STABLE_PATH` parameter to `TRUE` on a warehouse. You can use an existing warehouse or create a new one for testing.

Copy code

```
CREATE WAREHOUSE operational_query_testing;
ALTER WAREHOUSE operational_query_testing SET ENABLE_USE_STABLE_PATH = TRUE;
```

## Notes on billing and costs

Snowflake billing is unchanged by the optimizations in this public preview. In practice, workloads that leverage these optimizations
often see reduced total costs because of improved efficiency, reducing the amount of warehouse time to execute.

Snowflake currently does not bill for any [cloud services compute](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage) credits incurred for queries that run on the optimized path. This will change when this feature reaches general availability. For more information about costs for using hybrid tables, see [Evaluate cost for hybrid tables](/user-guide/tables-hybrid-cost).

## Overview

Operational queries are hybrid table queries that modify or select a small number of rows and execute in less than 100 ms. An operational query is eligible for the new optimization scheme when:

- The same SQL statement structure is executed repeatedly.
- The query operates exclusively on hybrid tables.
- The size of the query result does not exceed 100 KB.

When Snowflake observes repeated executions of an eligible query, subsequent executions benefit from these optimizations. If the statement
is parameterized (for example, by using bind variables via a driver), queries with the same structure but different bind values are also eligible.

When you use this public preview, many operational workloads may experience up to 8x better throughput. For example, in internal testing on a [Gen2 warehouse](/user-guide/warehouses-gen2) using a 100% read workload from the [Yahoo Cloud Serving Benchmark (YCSB)](https://github.com/brianfrankcooper/YCSB), Snowflake observed up to 8x better throughput compared to running the same workload without these optimizations.

## Optimized queries

Optimization is strictly limited to SQL statements that interact with hybrid tables only. Queries that join or access standard Snowflake tables
are not optimized by this feature.

The following SQL statements benefit from the optimizations in this public preview:

- [INSERT](/sql-reference/sql/insert), [UPDATE](/sql-reference/sql/update), and [DELETE](/sql-reference/sql/delete) statements
- [SELECT](/sql-reference/sql/select) statements

These statements are optimized if they contain:

- [WHERE](/sql-reference/constructs/where) clause conditions with comparison operators (`=`, `<`, `>`)
- An [ORDER BY](/sql-reference/constructs/order-by) clause, with or without a [LIMIT](/sql-reference/constructs/limit) clause
- [Joins](/sql-reference/constructs/join)

Note

Only the following join patterns are optimized in this public preview:

- **Primary Key to Primary Key joins**: The join condition matches the primary key columns on both sides of the join.
- **Foreign Key to Foreign Key joins**: The join condition matches foreign key columns on both sides of the join.
- **Index nested loop joins on a primary key**: For each row from the outer table, Snowflake uses the primary key index on the inner hybrid table to look up matching rows. This pattern is efficient when one side of the join is small or highly selective and the other side is joined on its primary key.

Other join patterns continue to work but will not benefit from the full set of optimizations.

### SQL statement limitations

Queries that contain the following features and constructs continue to perform as expected, but do not benefit from the optimizations in this public preview.

- [GROUP BY clause](/sql-reference/constructs/group-by)
- [Joins](/sql-reference/constructs/join) other than Primary Key to Primary Key joins, Foreign Key to Foreign Key joins, or index nested loop joins on a primary key
- [LIMIT](/sql-reference/constructs/limit) (when used independently, without an [ORDER BY](/sql-reference/constructs/order-by) clause)
- [Set operations](/sql-reference/operators-query)
- [Subqueries](/user-guide/querying-subqueries)
- [FOR UPDATE](/sql-reference/constructs/for-update)
- [Common table expressions](/sql-reference/constructs/with) (CTEs)
- [Time Travel](/user-guide/data-time-travel) constructs
- [Stored procedures](/developer-guide/stored-procedure/stored-procedures-overview)

Do not inject randomized comments into the query string. For example, do not use the following syntax:

Copy code

```
SELECT /* random-text */ a FROM ...
```

When queries are executed repeatedly, such changes might affect eligibility for optimizations.

### Other limitations

- **Transactions**: This preview supports only single-statement [transactions](/sql-reference/transactions) with [AUTOCOMMIT](/sql-reference/transactions#label-txn-autocommit) enabled.
  Multi-statement transactions are not supported in this preview.
- **Observability**: Snowflake tracks query execution in two system views:

  - [QUERY\_HISTORY](/sql-reference/account-usage/query_history) records the first execution of each query in detail.
  - [AGGREGATE\_QUERY\_HISTORY](/sql-reference/account-usage/aggregate_query_history) logs later successful runs of the same query to reduce logging volume.

  Currently, neither view shows whether a specific execution used the optimizations in this public preview. For eligible repeatable queries, execution latency should consistently fall in the low double-digit millisecond range within a few minutes of starting a new session.

## Getting started

To accurately measure the throughput and latency benefits of these optimizations, Snowflake recommends simulating a realistic workload using [JMeter](https://jmeter.apache.org/). A [JMeter test setup](https://github.com/sfc-gh-dadhikari/htbench) is available to measure QPS under a 90% read and 10% write workload.

You also need:

- [A role and schema for testing](#label-operational-query-performance-dedicated-role-warehouse-schema) (see the following steps to create a dedicated role, warehouse, and schema)
- [A dedicated user with key-pair authentication](#label-operational-query-performance-dedicated-user-keypair)
- [(Optional) JMeter for performance testing](#label-operational-query-performance-jmeter-testing)

Your application should use a Snowflake driver for running parameterized queries and follow [best practices](/user-guide/tables-hybrid-best-practices). The [Snowflake JDBC driver](/developer-guide/jdbc/jdbc) is recommended for this purpose.

### Create a dedicated role, warehouse, and schema

Using Snowsight, set up a dedicated [role](/user-guide/admin-user-management) for testing as well as a dedicated [warehouse](/user-guide/warehouses-overview) and [schema](/sql-reference/ddl-database).

Copy code

```
USE ROLE ACCOUNTADMIN;

-- Create role HT_BENCH_ROLE
CREATE OR REPLACE ROLE ht_bench_role;
GRANT ROLE ht_bench_role TO ROLE ACCOUNTADMIN;

-- Create HT_BENCH_WH warehouse
CREATE OR REPLACE WAREHOUSE ht_bench_wh
  WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE;
GRANT OWNERSHIP ON WAREHOUSE ht_bench_wh TO ROLE ht_bench_role;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE ht_bench_role;

-- Create HT_BENCH_DB database and schema
CREATE OR REPLACE DATABASE ht_bench_db;
GRANT OWNERSHIP ON DATABASE ht_bench_db TO ROLE ht_bench_role;
CREATE OR REPLACE SCHEMA data;
GRANT OWNERSHIP ON SCHEMA ht_bench_db.data TO ROLE ht_bench_role;

-- Use role
USE ROLE ht_bench_role;

-- Set context to use HT_BENCH_DB database and DATA schema
USE DATABASE ht_bench_db;
USE SCHEMA ht_bench_db.data;

-- Create hybrid table
CREATE OR REPLACE HYBRID TABLE icecream_orders (
  id NUMBER(38,0) NOT NULL,
  store_id NUMBER(38,0) NOT NULL,
  flavor VARCHAR(20) NOT NULL,
  num_scoops NUMBER(38,0),
  PRIMARY KEY (id)
);

-- Insert some data
INSERT INTO icecream_orders
  SELECT
    SEQ4() AS ID,
    UNIFORM(1, 100, RANDOM()) AS STORE_ID,
    ARRAY_CONSTRUCT('VANILLA','CHOCOLATE','STRAWBERRY','MANGO','PISTACHIO')
      [UNIFORM(0,4,RANDOM())]::STRING AS FLAVOR,
    UNIFORM(1, 5, RANDOM()) AS NUM_SCOOPS
  FROM TABLE(GENERATOR(ROWCOUNT => 10000));
```

This example creates a hybrid table with a [PRIMARY KEY constraint](/sql-reference/constraints), then populates it with sample data using the [SEQ4](/sql-reference/functions/seq1), [UNIFORM](/sql-reference/functions/uniform), [RANDOM](/sql-reference/functions/random), [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct), and [GENERATOR](/sql-reference/functions/generator) functions.

### Create a dedicated user with key-pair authentication

Create a user and set up authentication. This example creates a user named `ht_bench_user` and sets up key-pair authentication.

Create a private key using [key-pair authentication](/user-guide/key-pair-auth):

Copy code

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
```

Create a public key:

Copy code

```
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

For the user to connect without a password, you need to configure the public key. Copy the public key from `rsa_key.pub` and paste it
into the following SQL:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE USER ht_bench_user DEFAULT_ROLE = ht_bench_role;

-- Copy the key text from the rsa_key.pub file created in the previous step
ALTER USER ht_bench_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...<replace with your key>';

-- Finally, grant the role to the user
GRANT ROLE ht_bench_role TO USER ht_bench_user;
```

### Set up JMeter testing

To accurately measure the throughput and latency benefits of these optimizations, Snowflake recommends simulating a realistic workload
using [JMeter](https://jmeter.apache.org/). When running benchmarks, expect a warmup period of 1-2 minutes before the system reaches a steady state. During this time, Snowflake recognizes recurring query patterns and applies optimizations.

JMeter is an open-source load testing and performance measurement tool that can be used to benchmark and analyze the performance of hybrid
tables. It allows users to create and execute test plans that simulate concurrent workloads, measure throughput, and analyze system behavior
under load.

Download JMeter from the [official JMeter website](https://jmeter.apache.org/download_jmeter.cgi) for your platform. JMeter requires a recent version of Java 8 or higher.
You also need to download the latest [Snowflake JDBC driver](/developer-guide/jdbc/jdbc).

Tip

You can use [SDKMAN!](https://sdkman.io/), an open-source tool to easily configure your Java version.

Save the following JMeter test plan as `snowflake-hybrid-tables.jmx`. The plan performs point-lookup `SELECT` queries against the `icecream_orders` hybrid table created earlier in this guide.

Show JMeter test plan (snowflake-hybrid-tables.jmx)

Copy code

```
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="Hybrid Tables Test Plan">
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables">
        <collectionProp name="Arguments.arguments">
          <elementProp name="NUMBER_OF_KEYS" elementType="Argument">
            <stringProp name="Argument.name">NUMBER_OF_KEYS</stringProp>
            <stringProp name="Argument.value">${__P(NUMBER_OF_KEYS,100)}</stringProp>
            <stringProp name="Argument.desc">The number of keys to sample for each loop to iterate on.</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="NUMBER_OF_THREADS" elementType="Argument">
            <stringProp name="Argument.name">NUMBER_OF_THREADS</stringProp>
            <stringProp name="Argument.value">${__P(NUMBER_OF_THREADS,10)}</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="ACCOUNT_LOCATOR" elementType="Argument">
            <stringProp name="Argument.name">ACCOUNT_LOCATOR</stringProp>
            <stringProp name="Argument.value">${__P(ACCOUNT_LOCATOR,)}</stringProp>
            <stringProp name="Argument.desc">The account locator (without snowflakecomputing.com)</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="WAREHOUSE_NAME" elementType="Argument">
            <stringProp name="Argument.name">WAREHOUSE_NAME</stringProp>
            <stringProp name="Argument.value">${__P(WAREHOUSE_NAME,)}</stringProp>
            <stringProp name="Argument.desc">The Snowflake warehouse used for hybrid table testing.</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="DATABASE_NAME" elementType="Argument">
            <stringProp name="Argument.name">DATABASE_NAME</stringProp>
            <stringProp name="Argument.value">${__P(DATABASE_NAME,)}</stringProp>
            <stringProp name="Argument.desc">The database to use for testing.</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="SCHEMA_NAME" elementType="Argument">
            <stringProp name="Argument.name">SCHEMA_NAME</stringProp>
            <stringProp name="Argument.value">${__P(SCHEMA_NAME,DATA)}</stringProp>
            <stringProp name="Argument.desc">The schema name to use when connecting</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="USER_NAME" elementType="Argument">
            <stringProp name="Argument.name">USER_NAME</stringProp>
            <stringProp name="Argument.value">${__P(USER_NAME,)}</stringProp>
            <stringProp name="Argument.desc">The username to use when connecting</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="ROLE_NAME" elementType="Argument">
            <stringProp name="Argument.name">ROLE_NAME</stringProp>
            <stringProp name="Argument.value">${__P(ROLE_NAME,)}</stringProp>
            <stringProp name="Argument.desc">The role name to use when connecting</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="PRIVATE_KEY_FILE_PATH" elementType="Argument">
            <stringProp name="Argument.name">PRIVATE_KEY_FILE_PATH</stringProp>
            <stringProp name="Argument.value">${__P(PRIVATE_KEY_FILE_PATH,)}</stringProp>
            <stringProp name="Argument.desc">The private key file name to use</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="STABLE_PATH" elementType="Argument">
            <stringProp name="Argument.name">STABLE_PATH</stringProp>
            <stringProp name="Argument.value">${__P(STABLE_PATH,TRUE)}</stringProp>
            <stringProp name="Argument.desc">Whether to enable the operational query optimization (TRUE or FALSE).</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    <hashTree>
      <JDBCDataSource guiclass="TestBeanGUI" testclass="JDBCDataSource" testname="Snowflake JDBC">
        <boolProp name="autocommit">true</boolProp>
        <stringProp name="checkQuery"></stringProp>
        <stringProp name="connectionAge">5000</stringProp>
        <stringProp name="dataSource">jdbcConfig</stringProp>
        <stringProp name="dbUrl">jdbc:snowflake://${ACCOUNT_LOCATOR}.snowflakecomputing.com</stringProp>
        <stringProp name="driver">net.snowflake.client.jdbc.SnowflakeDriver</stringProp>
        <boolProp name="keepAlive">true</boolProp>
        <stringProp name="password"></stringProp>
        <stringProp name="poolMax">0</stringProp>
        <stringProp name="timeout">10000</stringProp>
        <stringProp name="transactionIsolation">DEFAULT</stringProp>
        <stringProp name="trimInterval">60000</stringProp>
        <stringProp name="username"></stringProp>
        <boolProp name="preinit">false</boolProp>
        <stringProp name="connectionProperties">user=${USER_NAME};db=${DATABASE_NAME};schema=${SCHEMA_NAME};warehouse=${WAREHOUSE_NAME};role=${ROLE_NAME};private_key_file=${PRIVATE_KEY_FILE_PATH};JDBC_QUERY_RESULT_FORMAT=JSON;enablePutGet=false</stringProp>
        <stringProp name="TestPlan.comments">Setup snowflake connection by adjusting the connection string as required.</stringProp>
      </JDBCDataSource>
      <hashTree/>
      <ResultCollector guiclass="RespTimeGraphVisualizer" testclass="ResultCollector" testname="Response Time Graph">
        <boolProp name="ResultCollector.error_logging">false</boolProp>
        <objProp>
          <name>saveConfig</name>
          <value class="SampleSaveConfiguration">
            <time>true</time>
            <latency>true</latency>
            <timestamp>true</timestamp>
            <success>true</success>
            <label>true</label>
            <code>true</code>
            <message>true</message>
            <threadName>true</threadName>
            <dataType>true</dataType>
            <encoding>false</encoding>
            <assertions>true</assertions>
            <subresults>true</subresults>
            <responseData>false</responseData>
            <samplerData>false</samplerData>
            <xml>false</xml>
            <fieldNames>true</fieldNames>
            <responseHeaders>false</responseHeaders>
            <requestHeaders>false</requestHeaders>
            <responseDataOnError>false</responseDataOnError>
            <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
            <assertionsResultsToSave>0</assertionsResultsToSave>
            <bytes>true</bytes>
            <sentBytes>true</sentBytes>
            <url>true</url>
            <threadCounts>true</threadCounts>
            <idleTime>true</idleTime>
            <connectTime>true</connectTime>
          </value>
        </objProp>
        <stringProp name="filename"></stringProp>
        <stringProp name="RespTimeGraph.interval">100</stringProp>
        <stringProp name="RespTimeGraph.graphtitle">Response Time Graph</stringProp>
        <intProp name="RespTimeGraph.graphtitlefondsize">3</intProp>
        <intProp name="RespTimeGraph.linestrockwidth">2</intProp>
        <intProp name="RespTimeGraph.lineshapepoint">4</intProp>
        <intProp name="RespTimeGraph.legendsize">1</intProp>
        <stringProp name="RespTimeGraph.seriesselectionmatchlabel">.*Query</stringProp>
        <intProp name="RespTimeGraph.legendplacement">1</intProp>
        <boolProp name="RespTimeGraph.seriesselection">true</boolProp>
      </ResultCollector>
      <hashTree/>
      <!-- Setup Thread Group - Run once before benchmark -->
      <SetupThreadGroup guiclass="SetupThreadGroupGui" testclass="SetupThreadGroup" testname="Setup - Init" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">1</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">1</stringProp>
        <stringProp name="ThreadGroup.ramp_time">0</stringProp>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
      </SetupThreadGroup>
      <hashTree>
        <JDBCSampler guiclass="TestBeanGUI" testclass="JDBCSampler" testname="Set Stable Path on Warehouse" enabled="true">
          <stringProp name="dataSource">jdbcConfig</stringProp>
          <stringProp name="query">ALTER WAREHOUSE ${WAREHOUSE_NAME} SET ENABLE_USE_STABLE_PATH = ${STABLE_PATH}</stringProp>
          <stringProp name="queryArguments"></stringProp>
          <stringProp name="queryArgumentsTypes"></stringProp>
          <stringProp name="queryTimeout">60</stringProp>
          <stringProp name="queryType">Update Statement</stringProp>
          <stringProp name="resultSetHandler">Store as String</stringProp>
          <stringProp name="resultSetMaxRows"></stringProp>
          <stringProp name="resultVariable"></stringProp>
          <stringProp name="variableNames"></stringProp>
        </JDBCSampler>
        <hashTree/>
        <JDBCSampler guiclass="TestBeanGUI" testclass="JDBCSampler" testname="Fetch Sample IDs (Once)" enabled="true">
          <stringProp name="dataSource">jdbcConfig</stringProp>
          <stringProp name="queryType">Select Statement</stringProp>
          <stringProp name="query">SELECT ID FROM ICECREAM_ORDERS SAMPLE (${NUMBER_OF_KEYS} ROWS);</stringProp>
          <stringProp name="queryArguments"></stringProp>
          <stringProp name="queryArgumentsTypes"></stringProp>
          <stringProp name="variableNames">SAMPLED_ID</stringProp>
          <stringProp name="resultVariable">sampledIds</stringProp>
          <stringProp name="queryTimeout"></stringProp>
          <stringProp name="resultSetMaxRows"></stringProp>
          <stringProp name="resultSetHandler">Store as Object</stringProp>
          <stringProp name="TestPlan.comments">Fetch sample IDs ONCE and store globally for all threads</stringProp>
        </JDBCSampler>
        <hashTree>
          <JSR223PostProcessor guiclass="TestBeanGUI" testclass="JSR223PostProcessor" testname="Store IDs Globally" enabled="true">
            <stringProp name="scriptLanguage">groovy</stringProp>
            <stringProp name="parameters"></stringProp>
            <stringProp name="filename"></stringProp>
            <stringProp name="cacheKey">true</stringProp>
            <stringProp name="script">
// Get the result set from the JDBC sampler
def ids = vars.getObject("sampledIds")
def idList = []

if (ids != null) {
    ids.each { row -&gt;
        idList.add(row.get("ID").toString())
    }
}

// Store as comma-separated string in JMeter properties (global)
def idString = idList.join(",")
props.put("GLOBAL_IDS", idString)
props.put("GLOBAL_IDS_COUNT", idList.size().toString())

log.info("Stored " + idList.size() + " IDs globally for all threads")
            </stringProp>
          </JSR223PostProcessor>
          <hashTree/>
        </hashTree>
      </hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="SELECT Thread Group">
        <stringProp name="TestPlan.comments">This thread group will issue SELECT commands using shared IDs</stringProp>
        <stringProp name="ThreadGroup.num_threads">${NUMBER_OF_THREADS}</stringProp>
        <intProp name="ThreadGroup.ramp_time">1</intProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller">
          <boolProp name="LoopController.continue_forever">true</boolProp>
          <intProp name="LoopController.loops">-1</intProp>
        </elementProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">${__P(DURATION,300)}</stringProp>
        <stringProp name="ThreadGroup.delay">0</stringProp>
      </ThreadGroup>
      <hashTree>
        <!-- Pick random ID from global pool each iteration -->
        <JSR223PreProcessor guiclass="TestBeanGUI" testclass="JSR223PreProcessor" testname="Pick Random ID" enabled="true">
          <stringProp name="scriptLanguage">groovy</stringProp>
          <stringProp name="parameters"></stringProp>
          <stringProp name="filename"></stringProp>
          <stringProp name="cacheKey">true</stringProp>
          <stringProp name="script">
// Get global IDs (fetched once in setup)
def idString = props.get("GLOBAL_IDS")
if (idString != null &amp;&amp; idString.length() &gt; 0) {
    def ids = idString.split(",")
    def randomIndex = new Random().nextInt(ids.length)
    vars.put("ID", ids[randomIndex])
} else {
    log.error("GLOBAL_IDS not found - setup may have failed")
    vars.put("ID", "1")
}
          </stringProp>
        </JSR223PreProcessor>
        <hashTree/>
        <JDBCSampler guiclass="TestBeanGUI" testclass="JDBCSampler" testname="Orders Query">
            <stringProp name="dataSource">jdbcConfig</stringProp>
            <stringProp name="queryType">Prepared Select Statement</stringProp>
            <stringProp name="query">SELECT * FROM ICECREAM_ORDERS WHERE ID = ?</stringProp>
            <stringProp name="queryArguments">${ID}</stringProp>
            <stringProp name="queryArgumentsTypes">INTEGER</stringProp>
            <stringProp name="variableNames"></stringProp>
            <stringProp name="resultVariable"></stringProp>
            <stringProp name="queryTimeout"></stringProp>
            <stringProp name="resultSetMaxRows"></stringProp>
            <stringProp name="resultSetHandler">Store as Object</stringProp>
          </JDBCSampler>
          <hashTree>
            <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="View Results Tree" enabled="false">
              <boolProp name="ResultCollector.error_logging">false</boolProp>
              <objProp>
                <name>saveConfig</name>
                <value class="SampleSaveConfiguration">
                  <time>true</time>
                  <latency>true</latency>
                  <timestamp>true</timestamp>
                  <success>true</success>
                  <label>true</label>
                  <code>true</code>
                  <message>true</message>
                  <threadName>true</threadName>
                  <dataType>true</dataType>
                  <encoding>false</encoding>
                  <assertions>true</assertions>
                  <subresults>true</subresults>
                  <responseData>false</responseData>
                  <samplerData>false</samplerData>
                  <xml>false</xml>
                  <fieldNames>true</fieldNames>
                  <responseHeaders>false</responseHeaders>
                  <requestHeaders>false</requestHeaders>
                  <responseDataOnError>false</responseDataOnError>
                  <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                  <assertionsResultsToSave>0</assertionsResultsToSave>
                  <bytes>true</bytes>
                  <sentBytes>true</sentBytes>
                  <url>true</url>
                  <threadCounts>true</threadCounts>
                  <idleTime>true</idleTime>
                  <connectTime>true</connectTime>
                </value>
              </objProp>
              <stringProp name="filename"></stringProp>
            </ResultCollector>
            <hashTree/>
            <ResultCollector guiclass="GraphVisualizer" testclass="ResultCollector" testname="Lookup Response">
              <boolProp name="ResultCollector.error_logging">false</boolProp>
              <objProp>
                <name>saveConfig</name>
                <value class="SampleSaveConfiguration">
                  <time>true</time>
                  <latency>true</latency>
                  <timestamp>true</timestamp>
                  <success>true</success>
                  <label>true</label>
                  <code>true</code>
                  <message>true</message>
                  <threadName>true</threadName>
                  <dataType>true</dataType>
                  <encoding>false</encoding>
                  <assertions>true</assertions>
                  <subresults>true</subresults>
                  <responseData>false</responseData>
                  <samplerData>false</samplerData>
                  <xml>false</xml>
                  <fieldNames>true</fieldNames>
                  <responseHeaders>false</responseHeaders>
                  <requestHeaders>false</requestHeaders>
                  <responseDataOnError>false</responseDataOnError>
                  <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                  <assertionsResultsToSave>0</assertionsResultsToSave>
                  <bytes>true</bytes>
                  <sentBytes>true</sentBytes>
                  <url>true</url>
                  <threadCounts>true</threadCounts>
                  <idleTime>true</idleTime>
                  <connectTime>true</connectTime>
                </value>
              </objProp>
              <stringProp name="filename"></stringProp>
            </ResultCollector>
            <hashTree/>
          </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

Note

For accurate benchmark results, run the JMeter client from a cloud virtual machine in the same cloud region as the target Snowflake deployment. The VM should have **at least 8 cores** so that the client itself is not the bottleneck when driving sustained concurrent load. Snowflake recommends a regional VM or a [Snowpark Container Services](/developer-guide/snowpark-container-services/overview) deployment, so that measured throughput and latency reflect hybrid table performance rather than cross-region network effects or client-side CPU limits. Running JMeter from a laptop or a cross-region machine is supported but will significantly understate the throughput and overstate the latency you would observe in production.

#### Set environment variables

Set the following environment variables to connect to Snowflake using JMeter. To find your account locator, see
[Account identifiers](/user-guide/admin-account-identifier).

Copy code

```
export SNOWFLAKE_JDBC_JAR_PATH=<PATH_TO_DOWNLOADED_SNOWFLAKE_JDBC_JAR>
export ACCOUNT_LOCATOR=<ACCOUNT_LOCATOR>
export USER_NAME="ht_bench_user"
export ROLE_NAME="ht_bench_role"
export WAREHOUSE_NAME="ht_bench_wh"
export DATABASE_NAME="ht_bench_db"
export SCHEMA_NAME="data"
export PRIVATE_KEY_FILE_PATH="/path/to/rsa/private/key/rsa_key.p8"
```

#### Run JMeter

You are now ready to run JMeter:

Copy code

```
jmeter -n -t snowflake-hybrid-tables.jmx \
  -Juser.classpath=$SNOWFLAKE_JDBC_JAR_PATH \
  -JNUMBER_OF_THREADS=150 \
  -JNUMBER_OF_KEYS=250 \
  -JDURATION=300 \
  -JSTABLE_PATH=TRUE \
  -JACCOUNT_LOCATOR=$ACCOUNT_LOCATOR \
  -JUSER_NAME=$USER_NAME \
  -JDATABASE_NAME=$DATABASE_NAME \
  -JSCHEMA_NAME=$SCHEMA_NAME \
  -JWAREHOUSE_NAME=$WAREHOUSE_NAME \
  -JROLE_NAME=$ROLE_NAME \
  -JPRIVATE_KEY_FILE_PATH=$PRIVATE_KEY_FILE_PATH \
  -l results.jtl \
  -Dnet.snowflake.jdbc.max_connections=200 \
  -Dnet.snowflake.jdbc.max_connections_per_route=200
```

This command runs JMeter for 5 minutes (300 seconds), using 150 concurrent threads that perform point lookups against a sampled set of 250 keys.
The test plan drives the load as fast as the warehouse can serve it; there is no client-side rate limit. Before the benchmark begins, the test
plan runs `ALTER WAREHOUSE ... SET ENABLE_USE_STABLE_PATH = TRUE` to enable the optimization. To measure the baseline without these optimizations,
re-run the command with `-JSTABLE_PATH=FALSE`. You can adjust the other parameters (`JNUMBER_OF_THREADS`, `JDURATION`, `JNUMBER_OF_KEYS`) to
simulate different scenarios.

After the run is complete, you can see the throughput (queries per second). Allow 1-2 minutes of warmup before the system reaches steady state. After
warmup, the output might show that QPS peaks at almost 5,000 QPS on an XSMALL warehouse:

Copy code

```
summary + 147615 in 00:00:30 = 4920.5/s Avg:    30 Min:     7 Max:  1535 Err:     0 (0.00%) Active: 150 Started: 150 Finished: 150
```

## Examples of optimized queries

The following statements should give you an idea of the types of queries that would benefit from the optimizations in this public preview.
To take advantage of these optimizations, these statements would need to be submitted repeatedly through a supported driver. For more information, see [Using a driver for parameterized queries](#label-operational-query-performance-using-driver).

Copy code

```
-- Simple point-lookups
SELECT * FROM icecream_orders WHERE id = 100;

-- Filtered scan with predicates
SELECT flavor, num_scoops FROM icecream_orders WHERE store_id = 3 AND num_scoops >= 2;

-- DML
UPDATE icecream_orders SET num_scoops = 3 WHERE id = 500;
INSERT INTO icecream_orders VALUES (99999999, 42, 'VANILLA', 3);
DELETE FROM icecream_orders WHERE id = 500;
```

The following examples are queries that would *not* benefit from the optimizations in this public preview because of documented [limitations](#label-operational-query-performance-sql-limitations).

Copy code

```
-- GROUP BY
SELECT flavor, COUNT(*) AS order_count
  FROM icecream_orders
  WHERE store_id = 5
  GROUP BY flavor
  ORDER BY order_count DESC;

-- Joins (create a stores table if you want to run this query)
SELECT * FROM icecream_orders o JOIN stores s ON o.store_id = s.id;

-- Multi-statement transactions without AUTOCOMMIT
BEGIN;
UPDATE icecream_orders SET num_scoops = 3 WHERE id = 500;
INSERT INTO icecream_orders VALUES (99999999, 42, 'VANILLA', 3);
COMMIT;

-- Statements containing subqueries and/or limits > 1 are also not optimized
SELECT *
  FROM (
    SELECT id, store_id, flavor, num_scoops
    FROM icecream_orders
    WHERE num_scoops >= 2
  ) sub
  LIMIT 10;
```

## Using a driver for parameterized queries

Individual SQL statements that are executed through a [driver](/developer-guide/drivers) and parameterized using bind variables are also eligible for these optimizations.

### Choosing a driver

For this public preview, Snowflake recommends the [Snowflake JDBC driver](/developer-guide/jdbc/jdbc), especially when you use it with a connection pool.

Executions through other drivers, such as the [Go Snowflake driver](/developer-guide/golang/go-driver), also benefit from these improvements.
While the [Snowflake connector for Python](/developer-guide/python-connector/python-connector) is supported, workloads using it may experience more limited benefits because of differences in
connection management, including the lack of built-in connection pooling.

### Example of JDBC prepared statements

The following example demonstrates using JDBC prepared statements with bind variables:

Copy code

```
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class IceCreamOrdersExample {

  public static void run(Connection connection) throws Exception {

    // UPDATE example (same statement, different bind values)
    String updateSql = "UPDATE ICECREAM_ORDERS SET NUM_SCOOPS = ? WHERE ID = ?";

    try (PreparedStatement pstmt = connection.prepareStatement(updateSql)) {

      // First execution
      pstmt.setInt(1, 2);   // NUM_SCOOPS
      pstmt.setLong(2, 25); // ID
      pstmt.executeUpdate();

      // Second execution (same prepared statement)
      pstmt.setInt(1, 3);
      pstmt.setLong(2, 26);
      pstmt.executeUpdate();
    }

    // SELECT example (point lookup)
    String selectSql =
        "SELECT ID, STORE_ID, FLAVOR, NUM_SCOOPS FROM ICECREAM_ORDERS WHERE ID = ?";

    try (PreparedStatement pstmt = connection.prepareStatement(selectSql)) {
      pstmt.setLong(1, 25);

      try (ResultSet rs = pstmt.executeQuery()) {
        while (rs.next()) {
          long id = rs.getLong("ID");
          long storeId = rs.getLong("STORE_ID");
          String flavor = rs.getString("FLAVOR");
          java.sql.Timestamp orderTs = rs.getTimestamp("ORDER_TS");
          int numScoops = rs.getInt("NUM_SCOOPS");

          System.out.printf("ID=%d store=%d flavor=%s ts=%s scoops=%d%n",
              id, storeId, flavor, orderTs, numScoops);
        }
      }
    }
  }
}
```
