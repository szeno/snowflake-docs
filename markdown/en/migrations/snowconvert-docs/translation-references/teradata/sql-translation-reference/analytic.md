# ANALYTIC

In this section, you will find the documentation for the translation reference of Analytic Language Elements.

## EXPLAIN

Translation specification for the EXPLAIN clause.

As per Teradata’s [documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/QueryGridTM-Installation-and-User-Guide-3.08/Configuring-and-Using-Links/Using-Links/Using-a-Teradata-to-TargetConnector-Link/SQL-Command-Reference-for-the-Teradata-Initiator-Connector/EXPLAIN), the EXPLAIN clause produces a step-by-step execution plan, which is a textual report that breaks down the query’s execution into a series of steps.

The syntax for this statement is as follows:

Copy code

```
 EXPLAIN [ <SQL_statement> ];
```

### Query

Copy code

```
 EXPLAIN SELECT * FROM table_1
```

#### Result

| Explanation |
| --- |
| 1. First, we lock DEMO\_USER.table\_3 in TD\_MAP1 for read on a reserved    RowHash to prevent global deadlock. 2) Next, we lock DEMO\_USER.table\_3    in TD\_MAP1 for read. 3) We do an all-AMPs RETRIEVE step in TD\_MAP1 from    DEMO\_USER.table\_3 by way of an all-rows scan with no residual conditions    into Spool 1 (group\_amps), which is built locally on the AMPs. The size    of Spool 1 is estimated with high confidence to be 1 row (32 bytes). The    estimated time for this step is 0.01 seconds. 4) Finally, we send out an    END TRANSACTION step to all AMPs involved in processing the request. |

**Snowflake**

##### Query

Copy code

```
    EXPLAIN SELECT * FROM table_1
```

##### Result

| ID | OPERATION | OBJECTS | SCHEDULE | PROJECTION | EXPRESSIONS |
| --- | --- | --- | --- | --- | --- |
| 0 | ResultFinalize |  | 3 | [1] |  |  |
| 1 | Exchange (SINGLE) |  |  |  |  |  |
| 2 | ResultWorker |  | 2 | [1] |  |  |
| 3 | Projection |  | 1 | [1] |  |  |
| 4 | RowGenerator |  | 0 | [] |  |  |

As you can see from the results, EXPLAIN in Teradata and Snowflake have the same goal: to provide an explanation of the steps that will be performed when a query is executed. However, Teradata uses a more verbose explanation compared to Snowflake, which only shows the name of each step to be executed.

### Related EWIs

No related EWIs.
