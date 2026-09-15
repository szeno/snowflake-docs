# Object Dependencies

This topic provides concepts on object dependencies and information related to the Account Usage view OBJECT\_DEPENDENCIES.

## What is an object dependency?

An object dependency means that in order to operate on an object, the object that is being operated on must reference metadata for itself
or reference metadata for at least one other object. Snowflake tracks object dependencies in the Account Usage view
[OBJECT\_DEPENDENCIES](/sql-reference/account-usage/object_dependencies).

Snowflake supports object dependencies in your local Snowflake account and certain dependencies related to data sharing, such as creating a
view in the consumer account from a table that is made available through a provider share. The dependencies for shared objects enable data
officers to ensure greater data integrity, comply with each regulatory standard more fully, and generate more detailed impact analysis.

Snowflake supports the following dependency types that can trigger a dependency: the object `name` value, the object ID value, and
the combination of the object `name` value with the object ID value.

BY\_NAME:
:   A `BY_NAME` dependency occurs when the SQL statement specifies the `name` value of the object itself
    (e.g. a [CREATE](/sql-reference/sql/create) or [ALTER](/sql-reference/sql/alter) command), or when an object calls the
    `name` value of another object (e.g. using a [FROM](/sql-reference/constructs/from) clause) to complete a SQL operation.

    For example, consider the following statement:

    > Copy code
    >
    > ```
    > create view myview as select * from mytable;
    > ```

    The table `name` value `mytable` is metadata for the table. The view named `myview` is dependent on the table named
    `mytable`; the table must exist to create the view.

    Snowflake refers to the view named `myview` as the referencing object and the table `mytable` as the
    referenced object.

BY\_ID:
:   A `BY_ID` dependency occurs when an object stores the object ID value of another object. One example of an ID
    dependency is an external stage storing the OBJECT\_ID value of a storage integration. Currently, the storage integration object ID value
    is only accessible to Snowflake and is not made visible through any customer-facing SQL operation.

    > Copy code
    >
    > ```
    > create stage my_ext_stage
    >   url='s3://load/files/'
    >   storage_integration = myint;
    > ```

    Snowflake refers to the external stage named `my_ext_stage` as the referencing object and the storage integration named
    `myint` as the referenced object.

BY\_NAME\_AND\_ID:
:   Some Snowflake objects (e.g. materialized views) are dependent on both the object `name` value and the object ID value. These
    objects are often the result of a CREATE OR REPLACE statement to replace an existing object or an ALTER statement to rename an object.

    For more information, see the [Usage notes](/sql-reference/account-usage/object_dependencies#label-object-dependencies-acctuse-usage-notes) section of the Account Usage OBJECT\_DEPENDENCIES view.

### Supported object dependencies

Snowflake supports referencing objects and referenced objects as follows:

| Referencing Object | Referenced Object | Dependency Type |
| --- | --- | --- |
| View, Secure View, dynamic table, SQL UDF, SQL UDTF, and other objects referenced by name | View  Secure View  Materialized View  Dynamic table  UDF (all kinds)  UDTF  and other objects referenced by name | BY\_NAME |
| External Stage  Stream | Storage Integration  Table, View, Secure View | BY\_ID |
| External table | Stage | BY\_ID |
| Materialized View | Table, External Table | BY\_NAME\_AND\_ID |

Expand

Show lessSee more

Note that Snowflake supports only the following objects in the context of data sharing:

| Referencing object | Referenced object | Dependency type |
| --- | --- | --- |
| View, dynamic table, SQL UDF, SQL UDTF | Table  Secure view  Secure materialized view  Dynamic table  Secure UDF and secure UDTF | BY\_NAME |
| Materialized view | Table | BY\_NAME\_AND\_ID |

Expand

Show lessSee more

For more information, see the [Usage Notes](/sql-reference/account-usage/object_dependencies#label-object-dependencies-acctuse-usage-notes) section of the OBJECT\_DEPENDENCIES view.

### Benefits

Identifying object dependencies can provide insight into data tracking use cases as follows:

Impact analysis:
:   Knowing the object dependency allows data stewards to identify the relationships between referencing objects and referenced objects to
    ensure that updates to referenced objects do not adversely impact users of the referencing object.

    For example, a table owner plans to add a column to a table. Querying the OBJECT\_DEPENDENCIES view based on the table name returns all
    of the objects (e.g. views) that will be affected.

    The data steward can then coordinate a plan of action to ensure that the timing of table and view updates do not result in any broken
    queries that would adversely affect users querying the views created from the table.

Compliance:
:   The object dependency relationship helps the compliance officer identify the relationship between sensitive data sources
    (i.e. referenced object) and data targets (i.e. referencing object). The compliance officer can then decide how best to update the
    referenced object and referencing object based on the compliance requirements (e.g. GDPR).

Data integrity:
:   The object dependency relationship helps primary data professionals, such as analysts, scientists, compliance officers, and other
    business users, to have confidence that the data originates from a trustworthy source.

### Limitations

In addition to the view [usage notes](/sql-reference/account-usage/object_dependencies), note the following limitations when querying
the OBJECT\_DEPENDENCIES view:

Session parameters:
:   Snowflake cannot accurately compute the dependencies of objects that include [session parameters](/sql-reference/parameters#label-session-parameters) in
    their definitions because session parameters can take on different values depending on the context.

    Snowflake recommends not using session variables in view and function definitions.

Snowflake implementations:
:   This view does not capture dependencies that are necessary for Snowflake implementations. For example, the view does not record the
    dependency necessary to create a new table from the clone of another table.

Object resolution:
:   If a view definition uses a function to call an object to create the view, or if an object is called inside another function or view,
    Snowflake does not record an object dependency. For example:

    > Copy code
    >
    > ```
    > create or replace view v_on_stage_function
    > as
    > select *
    > from T1
    > where get_presigned_url(@stage1, 'data_0.csv.gz')
    > is not null;
    > ```

    In this example, the function `get_presigned_url` calls the stage `stage1`. Snowflake does not record that the view named
    `v_on_stage_function` depends on the stage named `stage1`.

Broken dependencies:
:   If the dependency type value is `BY_NAME_AND_ID` and an object dependency changes due to a CREATE OR REPLACE or ALTER operation on an
    object, Snowflake only records the object dependency prior to these operations.

    Snowflake does not record the object dependency in the view query result after these operations because the result is a broken reference.

### Object dependencies with snowflake features and services

External objects:
:   Snowflake tracks object dependencies for Snowflake objects only. For example, if a Snowflake object depends on an
    Amazon S3 bucket, this view does not record the dependency on the bucket because the bucket is an Amazon object, not a Snowflake object.

Replication:
:   While a secondary object depends on the primary object, this view does not record dependencies due to a replication operation.

Data sharing:
:   For provider accounts, this view does not allow a data sharing provider account to determine dependent objects in the data sharing
    consumer account. For example, a data sharing provider creates a view and shares the view. The data sharing provider cannot use this view
    to determine any object in the consumer account that was created from the shared view (e.g. new tables or views).

    For consumer accounts, this view does not allow a data sharing consumer account to determine dependent objects in the data sharing
    provider account. For example, if a data sharing consumer account uses a UDF made available by the data sharing provider account, the
    data sharing consumer cannot use this view to identify any objects the shared UDF depends on.

    For more information, refer to the [Usage notes](/sql-reference/account-usage/object_dependencies#label-object-dependencies-acctuse-usage-notes).

## Querying the OBJECT\_DEPENDENCIES view

The following examples cover these use cases:

1. Show objects depending on an external table.
2. Impact analysis: find the objects referenced by a table.
3. GDPR: find the data source for a given view.
4. Data sharing.

### Show objects depending on an external table

Create a materialized view named `sales_view` from the external table named `sales_staging_table`:

> Copy code
>
> ```
> CREATE OR REPLACE MATERIALIZED VIEW sales_view AS SELECT * FROM sales_staging_table;
> ```

Query the OBJECT\_DEPENDENCIES view in the Account Usage schema of the shared SNOWFLAKE database. Note that the materialized view is the
`referencing_object_name` and the external table is the `referenced_object_domain`:

> Copy code
>
> ```
> SELECT referencing_object_name, referencing_object_domain, referenced_object_name, referenced_object_domain
> FROM snowflake.account_usage.object_dependencies
> WHERE referenced_object_name = 'SALES_STAGING_TABLE' and referenced_object_domain = 'EXTERNAL TABLE';
> ```
>
> ```
> +-------------------------+---------------------------+------------------------+--------------------------+
> | REFERENCING_OBJECT_NAME | REFERENCING_OBJECT_DOMAIN | REFERENCED_OBJECT_NAME | REFERENCED_OBJECT_DOMAIN |
> +-------------------------+---------------------------+------------------------+--------------------------+
> | SALES_VIEW              | MATERIALIZED VIEW         | SALES_STAGING_TABLE    | EXTERNAL TABLE           |
> +-------------------------+---------------------------+------------------------+--------------------------+
> ```

### Impact analysis: Find the Objects referenced by a table

Consider a base table named `SALES_NA`, where `NA` indicates North America, `US` indicates United States, and `CAL` indicates
California, with a series of nested views:

- (table) `SALES_NA` » (view) `NORTH_AMERICA_SALES` » (view) `US_SALES`
- (table) `SALES_NA` » (view) `NORTH_AMERICA_SALES` » (view) `CAL_SALES`

To create the table and nested views, execute the following commands:

> Copy code
>
> ```
> CREATE TABLE sales_na(product string);
> CREATE OR REPLACE VIEW north_america_sales AS SELECT * FROM sales_na;
> CREATE VIEW us_sales AS SELECT * FROM north_america_sales;
> CREATE VIEW cal_sales AS SELECT * FROM north_america_sales;
> ```

Similarly, consider the relationship of the base table `SALES_NA` to its nested views, and consider the base table `SALES_UK`, where
`UK` indicates the United Kingdom, to its nested view.

Note that two different views serve as source objects to derive the view named `GLOBAL_SALES`:

- (table) `SALES_NA` » (view) `NORTH_AMERICA_SALES` » (view) `GLOBAL_SALES`
- (table) `SALES_UK` » (view) `GLOBAL_SALES`

To create these nested views, execute the following commands:

> Copy code
>
> ```
> CREATE TABLE sales_uk (product string);
> CREATE VIEW global_sales AS SELECT * FROM sales_uk UNION ALL SELECT * FROM north_america_sales;
> ```

Query the OBJECT\_DEPENDENCIES view in the Account Usage schema of the shared SNOWFLAKE database to determine the object references for the
table `SALES_NA`. Note the fourth row in the query result, which specifies the table `SALES_NA` but does not reference the table
`SALES_UK`:

> Copy code
>
> ```
> WITH RECURSIVE referenced_cte
> (object_name_path, referenced_object_name, referenced_object_domain, referencing_object_domain, referencing_object_name, referenced_object_id, referencing_object_id)
>     AS
>       (
>         SELECT referenced_object_name || '-->' || referencing_object_name as object_name_path,
>                referenced_object_name, referenced_object_domain, referencing_object_domain, referencing_object_name, referenced_object_id, referencing_object_id
>           FROM snowflake.account_usage.object_dependencies referencing
>           WHERE true
>             AND referenced_object_name = 'SALES_NA' AND referenced_object_domain='TABLE'
>
>         UNION ALL
>
>         SELECT object_name_path || '-->' || referencing.referencing_object_name,
>               referencing.referenced_object_name, referencing.referenced_object_domain, referencing.referencing_object_domain, referencing.referencing_object_name,
>               referencing.referenced_object_id, referencing.referencing_object_id
>           FROM snowflake.account_usage.object_dependencies referencing JOIN referenced_cte
>             ON referencing.referenced_object_id = referenced_cte.referencing_object_id
>             AND referencing.referenced_object_domain = referenced_cte.referencing_object_domain
>       )
>
>   SELECT object_name_path, referenced_object_name, referenced_object_domain, referencing_object_name, referencing_object_domain
>     FROM referenced_cte
> ;
> ```
>
> ```
> +-----------------------------------------------+------------------------+--------------------------+-------------------------+---------------------------+
> | OBJECT_NAME_PATH                              | REFERENCED_OBJECT_NAME | REFERENCED_OBJECT_DOMAIN | REFERENCING_OBJECT_NAME | REFERENCING_OBJECT_DOMAIN |
> +-----------------------------------------------+------------------------+--------------------------+-------------------------+---------------------------+
> | SALES_NA-->NORTH_AMERICA_SALES                | SALES_NA               | TABLE                    | NORTH_AMERICA_SALES     | VIEW                      |
> | SALES_NA-->NORTH_AMERICA_SALES-->CAL_SALES    | NORTH_AMERICA_SALES    | VIEW                     | CAL_SALES               | VIEW                      |
> | SALES_NA-->NORTH_AMERICA_SALES-->US_SALES     | NORTH_AMERICA_SALES    | VIEW                     | US_SALES                | VIEW                      |
> | SALES_NA-->NORTH_AMERICA_SALES-->GLOBAL_SALES | NORTH_AMERICA_SALES    | VIEW                     | GLOBAL_SALES            | VIEW                      |
> +-----------------------------------------------+------------------------+--------------------------+-------------------------+---------------------------+
> ```

### GDPR: Find the data source for a given view

Derived objects (e.g. views, CTAS) can be created from many different source objects to provide a custom view or dashboard. To meet
regulatory requirements such as GDPR, compliance officers and auditors need to be able to trace data from a given object to its original
data source.

For example, the view `GLOBAL_SALES` is derived from two different dependency paths that point to two different base tables:

- (table) `SALES_NA` » (view) `NORTH_AMERICA_SALES` » (view) `GLOBAL_SALES`
- (table) `SALES_UK` » (view) `GLOBAL_SALES`

To create these nested views, execute the following commands:

> Copy code
>
> ```
> CREATE TABLE sales_na (product string);
> CREATE OR REPLACE VIEW north_america_sales AS SELECT * FROM sales_na;
> CREATE TABLE sales_uk (product string);
> CREATE VIEW global_sales AS SELECT * FROM sales_uk UNION ALL SELECT * FROM north_america_sales;
> ```

Query the OBJECT\_DEPENDENCIES view in the Account Usage schema of the shared SNOWFLAKE database to find the data source(s) of the view
`GLOBAL_SALES`. Each row in the query result specifies a dependency path to a unique object.

> Copy code
>
> ```
> WITH RECURSIVE referenced_cte
> (object_name_path, referenced_object_name, referenced_object_domain, referencing_object_domain, referencing_object_name, referenced_object_id, referencing_object_id)
>     AS
>       (
>         SELECT referenced_object_name || '<--' || referencing_object_name AS object_name_path,
>                referenced_object_name, referenced_object_domain, referencing_object_domain, referencing_object_name, referenced_object_id, referencing_object_id
>           from snowflake.account_usage.object_dependencies referencing
>           WHERE true
>             AND referencing_object_name = 'GLOBAL_SALES' and referencing_object_domain='VIEW'
>
>         UNION ALL
>
>         SELECT referencing.referenced_object_name || '<--' || object_name_path,
>               referencing.referenced_object_name, referencing.referenced_object_domain, referencing.referencing_object_domain, referencing.referencing_object_name,
>               referencing.referenced_object_id, referencing.referencing_object_id
>           FROM snowflake.account_usage.object_dependencies referencing JOIN referenced_cte
>             ON referencing.referencing_object_id = referenced_cte.referenced_object_id
>             AND referencing.referencing_object_domain = referenced_cte.referenced_object_domain
>       )
>
>   SELECT object_name_path, referencing_object_name, referencing_object_domain, referenced_object_name, referenced_object_domain
>     FROM referenced_cte
> ;
> ```
>
> ```
> +-----------------------------------------------+-------------------------+---------------------------+------------------------+--------------------------+
> | OBJECT_NAME_PATH                              | REFERENCING_OBJECT_NAME | REFERENCING_OBJECT_DOMAIN | REFERENCED_OBJECT_NAME | REFERENCED_OBJECT_DOMAIN |
> +-----------------------------------------------+-------------------------+---------------------------+------------------------+--------------------------+
> | SALES_UK<--GLOBAL_SALES                       | GLOBAL_SALES            | VIEW                      | SALES_UK               | TABLE                    |
> | NORTH_AMERICA_SALES<--GLOBAL_SALES            | GLOBAL_SALES            | VIEW                      | NORTH_AMERICA_SALES    | VIEW                     |
> | SALES_NA<--NORTH_AMERICA_SALES<--GLOBAL_SALES | NORTH_AMERICA_SALES     | VIEW                      | SALES_NA               | TABLE                    |
> +-----------------------------------------------+-------------------------+---------------------------+------------------------+--------------------------+
> ```

### Data sharing

Consider the following table, which is an excerpt from the OBJECT\_DEPENDENCIES view in the consumer account, where:

- `V1` specifies a view that the consumer creates from a shared object.
- `S_V1` specifies a view that the provider shares.
- `S_T1` specifies a table that the provider shares.

| Row | REFERENCING\_OBJECT\_NAME | REFERENCED\_OBJECT\_NAME | REFERENCED\_OBJECT\_DOMAIN | REFERENCED\_OBJECT\_ID |
| --- | --- | --- | --- | --- |
| 1 | V1 | S\_V1 | TABLE | NULL |
| 2 | V1 | S\_T1 | TABLE | NULL |

Expand

Show lessSee more

Given this table, note the following:

- If the provider [revokes](/sql-reference/sql/revoke-privilege-share) `S_T1` from the share, the consumer continues to see rows
  that specify `S_T1` (row 2) in their local view as long as `S_T1` was not renamed prior to the revocation.
- If the provider drops a table or view in their account, the table or view is no longer included in the share. The local consumer
  view preserves existing records for the dropped table or view because the table or view was shared prior to the drop operation
  in the provider account.

  The consumer cannot observe view changes in the provider account.
