Categories:
:   [Metadata functions](/sql-reference/functions-metadata)

# GET\_DDL

Returns a DDL statement that can be used to recreate the specified object. For databases and schemas, GET\_DDL is recursive
(that is, it returns the DDL statements for recreating all supported objects within the specified database/schema).

GET\_DDL currently supports the following object types:

- Cortex Agents (see [CREATE AGENT](/sql-reference/sql/create-agent))
- Cortex Search services (see [CREATE CORTEX SEARCH SERVICE](/sql-reference/sql/create-cortex-search))
- Alerts (see [CREATE ALERT](/sql-reference/sql/create-alert))
- Databases (see [CREATE DATABASE](/sql-reference/sql/create-database)), including [catalog-linked databases](/sql-reference/sql/create-database-catalog-linked).
- Data metric functions (see [CREATE DATA METRIC FUNCTION](/sql-reference/sql/create-data-metric-function))
- Contacts (see [CREATE CONTACT](/sql-reference/sql/create-contact))
- dbt project objects (see [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project))
- Dynamic tables (see [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table))
- Event tables (see [CREATE EVENT TABLE](/sql-reference/sql/create-event-table))
- External tables (see [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table))
- Failover groups (see [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group))
- File formats (see [CREATE FILE FORMAT](/sql-reference/sql/create-file-format))
- Hybrid tables (see [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table))
- Apache Iceberg™ tables (see [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table))
- Notebooks (see [CREATE NOTEBOOK](/sql-reference/sql/create-notebook))
- Online feature tables (see [CREATE ONLINE FEATURE TABLE](/sql-reference/sql/create-online-feature-table))
- Openflow deployments, runtimes, and connectors (see [CREATE OPENFLOW DEPLOYMENT](/sql-reference/sql/create-openflow-deployment),
  [CREATE OPENFLOW RUNTIME](/sql-reference/sql/create-openflow-runtime), [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector))
- Pipes (see [CREATE PIPE](/sql-reference/sql/create-pipe))
- Policies (see [CREATE AGGREGATION POLICY](/sql-reference/sql/create-aggregation-policy) , [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) , [CREATE DATA MOVEMENT POLICY](/sql-reference/sql/create-data-movement-policy) , [CREATE JOIN POLICY](/sql-reference/sql/create-join-policy) ,
  [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy) , [CREATE PASSWORD POLICY](/sql-reference/sql/create-password-policy) , [CREATE PRIVACY POLICY](/sql-reference/sql/create-privacy-policy) ,
  [CREATE PROJECTION POLICY](/sql-reference/sql/create-projection-policy) , [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy) , [CREATE SESSION POLICY](/sql-reference/sql/create-session-policy),
  [CREATE STORAGE LIFECYCLE POLICY](/sql-reference/sql/create-storage-lifecycle-policy))
- Data movement rules (see [CREATE DATA MOVEMENT RULE](/sql-reference/sql/create-data-movement-rule))
- Replication groups (see [CREATE REPLICATION GROUP](/sql-reference/sql/create-replication-group))
- Schemas (see [CREATE SCHEMA](/sql-reference/sql/create-schema))
- Semantic views (see [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view))
- Sequences (see [CREATE SEQUENCE](/sql-reference/sql/create-sequence))
- Storage integrations (see [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration))
- Stored procedures (see [CREATE PROCEDURE](/sql-reference/sql/create-procedure))
- Streams (see [CREATE STREAM](/sql-reference/sql/create-stream))
- Tables (see [CREATE TABLE](/sql-reference/sql/create-table))
- Tags (see [CREATE TAG](/sql-reference/sql/create-tag))
- Tasks (see [CREATE TASK](/sql-reference/sql/create-task))
- UDFs, including external functions (see [CREATE FUNCTION](/sql-reference/sql/create-function))
- User-defined types (see [CREATE TYPE](/sql-reference/sql/create-type))
- Views (see [CREATE VIEW](/sql-reference/sql/create-view))
- Warehouses (see [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse))

## Syntax

Copy code

```
GET_DDL( '<object_type>' , '[<namespace>.]<object_name>' [ , <use_fully_qualified_names_for_recreated_objects> ] )
```

## Arguments

**Required:**

`'object_type'`
:   Specifies the type of object for which the DDL is returned. Valid values (corresponding to the supported object types) are:

    - CORTEX\_AGENT
    - CORTEX\_SEARCH\_SERVICE
    - CONTACT
    - DATABASE
    - DATA MOVEMENT RULE
    - DYNAMIC\_TABLE
    - EVENT\_TABLE
    - FAILOVER\_GROUP
    - FILE\_FORMAT
    - FUNCTION (for UDFs, including data metric functions and external functions)
    - ICEBERG\_TABLE
    - INTEGRATION (storage)
    - PIPE
    - POLICY (aggregation, authentication, data movement, join, masking, password, projection, row access, session, and storage lifecycle policies)
    - PROCEDURE (for stored procedures)
    - REPLICATION\_GROUP
    - SCHEMA
    - SEMANTIC VIEW
    - SEQUENCE
    - STREAM
    - TABLE (for tables, external tables, and hybrid tables)
    - TAG (object tagging)
    - TASK
    - TYPE
    - VIEW (for views and materialized views)
    - WAREHOUSE

`'namespace.object_name'`
:   Specifies the fully-qualified name of the object for which the DDL is returned.

    Namespace is the database and/or schema in which the object resides:

    - Not used for databases.
    - For schemas, takes the form of `database`.
    - For schema objects (tables, views, streams, tasks, sequences, file formats, pipes, policies, and UDFs), takes the form of
      `database.schema` or `schema`.

    Namespace is optional if a database and schema are currently in use within the user session; otherwise, it is required.

**Optional:**

`use_fully_qualified_names_for_recreated_objects`
:   If TRUE, the generated DDL statements use fully qualified names for the objects to be recreated.

    Default: FALSE.

    Note

    This does not affect the names of other objects referenced in the DDL statement (e.g. the name of a table referenced in
    a view definition).

## Returns

Returns a string (a VARCHAR value) containing the text of the DDL statement that created the object.

For UDFs and stored procedures, the output might be slightly different from the original DDL. For example, if the UDF or stored
procedure contains JavaScript code, the delimiter characters around the JavaScript code might be different.

In addition, note that the DDL statement returned by the function might include default values for properties. For example, even
if the original CREATE PROCEDURE statement did not specify EXECUTE AS OWNER, the DDL statement returned by the function includes
EXECUTE AS OWNER, which is the default.

## Access control requirements

- For [semantic views](/user-guide/views-semantic/overview), you must use a role that has been
  [granted the REFERENCES or OWNERSHIP privilege on the semantic view](/user-guide/views-semantic/sql#label-semantic-views-privileges).

## Usage notes

The following notes apply to all supported objects:

- `object_type` and `object_name` (including `namespace` if specified) must be enclosed in single quotes.
- For `object_type`, `TABLE` and `VIEW` are interchangeable. If a `TABLE` object type is specified, and the object specified by name is a view, the function returns the DDL for
  the view and vice-versa.
- If `object_type` is `FUNCTION` (i.e. UDF) and the UDF has arguments, you must include the argument data types as part of the function name, in the form of
  `'function_name( [ arg_data_type [ , ... ] ] )'`, where `function_name` is the name of the function and `arg_data_type` is the data type of the argument.
- If `object_type` is `PROCEDURE` and the stored procedure has arguments, then you must include the
  argument data types as part of the function name, in the form of
  `'procedure_name( [ arg_data_type [ , ... ] ] )'`.
- Querying this function for most Snowflake object types requires the same minimum permissions needed to view the object (using [DESCRIBE <object>](/sql-reference/sql/desc) or [SHOW <objects>](/sql-reference/sql/show)).
  Snowflake restricts viewing special objects such as secure views to the owner, which is the role with the OWNERSHIP privilege on the object.
- When the returned DDL statement includes data type specifications, this function replaces data type aliases in the original
  statement with standard Snowflake data type names by default. If you want the returned DDL statement to include the data type
  aliases in the original statement, set the [ENABLE\_GET\_DDL\_USE\_DATA\_TYPE\_ALIAS](/sql-reference/parameters#label-enable-get-ddl-use-data-type-alias) parameter to TRUE.

For Iceberg tables:

- If you specify a `TABLE` object that’s an Iceberg table, the function returns the DDL for the Iceberg table.
- The output includes the `ICEBERG_VERSION` property for all Iceberg tables that are Snowflake-managed or part of a catalog-linked database, regardless of format version. For example,
  a v2 table includes `ICEBERG_VERSION = 2` and a v3 table includes `ICEBERG_VERSION = 3`.
- If [BASE\_LOCATION](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-base-location) was specified in the original CREATE ICEBERG TABLE statement,
  the function returns the original user input. Otherwise,
  the function returns the Snowflake-constructed file path (including the random 8-character string).
  For more information, see [Data and metadata directories](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

For catalog-linked database:

- The output includes the LINKED\_CATALOG options.
- For ALLOWED\_NAMESPACES and BLOCKED\_NAMESPACES, Snowflake doesn’t store nested namespaces if the set already contains the parent namespace.
  For example, if you create a database and specify `ALLOWED_NAMESPACES = ('ns1', 'ns1.ns2', 'ns1.ns3')`, Snowflake returns `ALLOWED_NAMESPACES = ('ns1')` in the GET\_DDL output.
  The same applies for BLOCKED\_NAMESPACES.

The following notes are specific to view objects. The query result always:

- Returns lowercase SQL text for `create or replace view`, even if the casing in the original SQL statement used to create the
  view was uppercase or mixed case.
- Includes the OR REPLACE clause.
- Includes the SECURE property, if the view is secure.
- Excludes the COPY GRANTS view parameter, even if the original CREATE VIEW statement specifies the COPY GRANTS parameter.
- Generates the column list.

  If a masking policy is set on a column, the result specifies the masking policy for the column.
- Removes in-line SQL comments before the view body (that is, before AS). For example, in the following code, the comment
  immediately prior to the AS clause is removed:

  Copy code

  ```
  CREATE VIEW view_t1
    -- GET_DDL() removes this comment.
    AS SELECT * FROM t1;
  ```

The following notes apply specifically to table and view objects with a tag or policy:

- The role executing the GET\_DDL query must have the global APPLY MASKING POLICY, APPLY ROW ACCESS POLICY, APPLY AGGREGATION POLICY, APPLY JOIN POLICY,
  APPLY PROJECTION POLICY, APPLY STORAGE LIFECYCLE POLICY, or APPLY TAG privilege and the USAGE privilege on the database and schema containing the policy or tag.
  Otherwise, Snowflake replaces the policy with `#UNKNOWN_POLICY` and the tag with `#UNKNOWN_TAG='#UNKNOWN_VALUE`. This text
  indicates that the column or the object is protected by a policy and a tag is set on the object or column. If this text is not removed
  prior to recreating the object, the CREATE OR REPLACE *<object>* statement fails.

  If this text is present in the GET\_DDL query result, prior to recreating the object, consult with your internal governance administrator
  to determine which policies and tags are necessary for the columns or object. Finally, edit the GET\_DDL query result and then recreate
  the object.

  Without the mentioned privileges, this table function does not return the corresponding row for the policy and tag assignments in the
  output of calling the function.
- When multiple tags are set on the object or column, the GET\_DDL output sorts the tags alphabetically by tag name.
- Dropping a tag removes the tag from the GET\_DDL output.
- If a tag is set on the table or view, the GET\_DDL output for the table or view includes the tag assignments in the CREATE OR REPLACE
  statement.
- If a masking policy, row access policy, or storage lifecycle policy is set, the GET\_DDL output includes the policy assignments using the WITH keyword.

When a tag is set on the database or the schema, the GET\_DDL output includes:

- An ALTER DATABASE statement when the tag is set on the database.
- An ALTER DATABASE statement and an ALTER SCHEMA statement when the tag is set on both the database and schema.
- An ALTER SCHEMA statement when the tag is set on the schema.
- A CREATE OR REPLACE statement to generate the tag, if the tag exists in the database or schema.

The following apply to storage integrations:

- The command always returns the CREATE OR REPLACE STORAGE INTEGRATION syntax.
- If a STORAGE\_AWS\_EXTERNAL\_ID was not specified during storage integration creation, this command returns the ID that was automatically
  generated during storage integration creation.

## Collation details

- Collation information is included in the input.

## Examples

The following examples demonstrate how to use this function to retrieve the DDL statement for an object:

- [Cortex Agents](#label-get-ddl-example-cortex-agents)
- [Views](#label-get-ddl-example-views)
- [Semantic views](#label-get-ddl-example-semantic-views)
- [Schemas](#label-get-ddl-example-schemas)
- [UDFs and stored procedures](#label-get-ddl-example-functions-procedures)
- [Masking policies](#label-get-ddl-example-masking-policies)
- [Storage integrations](#label-get-ddl-example-storage-integrations)
- [Warehouses](#label-get-ddl-example-warehouses)
- [Hybrid tables](#label-get-ddl-example-hybrid-tables)
- [Failover groups](#label-get-ddl-example-failover-groups)
- [Replication groups](#label-get-ddl-example-replication-groups)

### Cortex Agents

Return the DDL used to create a Cortex Agent named `my_agent`:

Copy code

```
SELECT GET_DDL('CORTEX_AGENT', 'my_agent');

+------------------------------------------------------------------------+
| GET_DDL('CORTEX_AGENT', 'MY_AGENT')                                    |
+------------------------------------------------------------------------+
| CREATE OR REPLACE AGENT my_agent                                       |
| COMMENT = 'Test agent'                                                 |
| PROFILE = '{"display_name": "Test Agent", "color": "blue"}'            |
| FROM SPECIFICATION                                                     |
| $$                                                                     |
| models:                                                                |
|   orchestration: "llama3-8b"                                           |
| instructions:                                                          |
|   response: "You are a helpful test agent"                             |
|   system: "Respond in a friendly and concise manner"                   |
| tools:                                                                 |
|   - tool_spec:                                                         |
|       type: "cortex_analyst_text_to_sql"                               |
|       name: "Analyst1"                                                 |
| tool_resources:                                                        |
|   Analyst1:                                                            |
|     semantic_view: "db.schema.semantic_view"                           |
| $$;                                                                    |
+------------------------------------------------------------------------+
```

### Views

Return the DDL used to create a view named `books_view`:

Copy code

```
SELECT GET_DDL('VIEW', 'books_view');
+-----------------------------------------------------------------------------+
| GET_DDL('VIEW', 'BOOKS_VIEW')                                               |
|-----------------------------------------------------------------------------|
|                                                                             |
| CREATE OR REPLACE VIEW BOOKS_VIEW as select title, author from books_table; |
|                                                                             |
+-----------------------------------------------------------------------------+
```

### Semantic views

See [Getting the SQL statement for a semantic view](/user-guide/views-semantic/sql#label-semantic-views-get-ddl).

### Schemas

Return the DDL used to create a schema named `books_schema` and the objects in the schema (the table `books_table`
and the view `books_view`):

Copy code

```
SELECT GET_DDL('SCHEMA', 'books_schema');
+-----------------------------------------------------------------------------+
| GET_DDL('SCHEMA', 'BOOKS_SCHEMA')                                           |
|-----------------------------------------------------------------------------|
| CREATE OR REPLACE SCHEMA BOOKS_SCHEMA;                                      |
|                                                                             |
| CREATE OR REPLACE TABLE BOOKS_TABLE (                                       |
| 	ID NUMBER(38,0),                                                          |
| 	TITLE VARCHAR(255),                                                       |
| 	AUTHOR VARCHAR(255)                                                       |
| );                                                                          |
|                                                                             |
| CREATE OR REPLACE VIEW BOOKS_VIEW as select title, author from books_table; |
|                                                                             |
+-----------------------------------------------------------------------------+
```

Return the DDL that uses fully-qualified names for the objects to be recreated:

Copy code

```
SELECT GET_DDL('SCHEMA', 'books_schema', true);
+---------------------------------------------------------------------------------------------------+
| GET_DDL('SCHEMA', 'BOOKS_SCHEMA', TRUE)                                                           |
|---------------------------------------------------------------------------------------------------|
| CREATE OR REPLACE SCHEMA BOOKS_DB.BOOKS_SCHEMA;                                                   |
|                                                                                                   |
| CREATE OR REPLACE TABLE BOOKS_DB.BOOKS_SCHEMA.BOOKS_TABLE (                                       |
| 	ID NUMBER(38,0),                                                                                |
| 	TITLE VARCHAR(255),                                                                             |
| 	AUTHOR VARCHAR(255)                                                                             |
| );                                                                                                |
|                                                                                                   |
| CREATE OR REPLACE VIEW BOOKS_DB.BOOKS_SCHEMA.BOOKS_VIEW as select title, author from books_table; |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

Note

As demonstrated in the example above, the DDL statement doesn’t use a fully-qualified name for the table used to create the
view. To resolve the name of this table, Snowflake uses the name of the database and the name of the schema for the view.

### UDFs and stored procedures

Return the DDL used to create a UDF named `multiply` that has two arguments with the data type NUMBER:

Copy code

```
SELECT GET_DDL('FUNCTION', 'multiply(number, number)');

+--------------------------------------------------+
| GET_DDL('FUNCTION', 'MULTIPLY(NUMBER, NUMBER)')  |
+--------------------------------------------------+
| CREATE OR REPLACE "MULTIPLY"(A NUMBER, B NUMBER) |
| RETURNS NUMBER(38,0)                             |
| COMMENT='multiply two numbers'                   |
| AS 'a * b';                                      |
+--------------------------------------------------+
```

Return the DDL to create a stored procedure named `stproc_1` that has one argument with the data type FLOAT:

Copy code

```
SELECT GET_DDL('procedure', 'stproc_1(float)');
+---------------------------------------------------+
| GET_DDL('PROCEDURE', 'STPROC_1(FLOAT)')           |
|---------------------------------------------------|
| CREATE OR REPLACE PROCEDURE "STPROC_1"("F" FLOAT) |
| RETURNS FLOAT                                     |
| LANGUAGE JAVASCRIPT                               |
| EXECUTE AS OWNER                                  |
| AS '                                              |
| ''return F;''                                     |
| ';                                                |
+---------------------------------------------------+
```

### Masking policies

Return the DDL to create a masking policy named `employee_ssn_mask` to mask social security numbers. Masked values are seen unless the user’s current role is `payroll`.

Copy code

```
SELECT GET_DDL('POLICY', 'employee_ssn_mask');

+----------------------------------------------------------------------------+
|                   GET_DDL('POLICY', 'EMPLOYEE_SSN_MASK')                   |
+----------------------------------------------------------------------------+
| CREATE MASKING POLICY employee_ssn_mask AS (val string) RETURNS string ->  |
| case                                                                       |
|   when current_role() in ('PAYROLL')                                       |
|   then val                                                                 |
|   else '******'                                                            |
| end;                                                                       |
+----------------------------------------------------------------------------+
```

### Storage integrations

Return the DDL to create a storage integration named `s3_int` that creates an external AWS stage.

Copy code

```
SELECT GET_DDL('INTEGRATION', s3_int);

+----------------------------------------------------------------------------+
| GET_DDL('INTEGRATION', 's3_int')                                           |
|----------------------------------------------------------------------------|
| CREATE OR REPLACE STORAGE INTEGRATION s3_int                               |
|   TYPE = EXTERNAL_STAGE                                                    |
|   STORAGE_PROVIDER = 'S3'                                                  |
|   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::001234567890:role/myrole'           |
|   STORAGE_AWS_EXTERNAL_ID='ACCOUNT_SFCRole=2_kztjogs3W9S18I+iWapHpIz/wq4=' |
|   ENABLED = TRUE                                                           |
|   STORAGE_ALLOWED_LOCATIONS = ('s3://mybucket1/path1/');                   |
+----------------------------------------------------------------------------+
```

### Warehouses

Suppose that you execute the following statement to create a warehouse named `my_wh`:

Copy code

```
CREATE OR REPLACE WAREHOUSE my_wh
  WAREHOUSE_SIZE=LARGE
  INITIALLY_SUSPENDED=TRUE;
```

The following call to the GET\_DDL function returns the DDL statement to recreate this warehouse:

Copy code

```
SELECT GET_DDL('WAREHOUSE', 'my_wh');
```

```
+-------------------------------------------+
| GET_DDL('WAREHOUSE', 'MY_WH')             |
|-------------------------------------------|
| create or replace warehouse MY_WH         |
| with                                      |
|     warehouse_type='STANDARD'             |
|     warehouse_size='Large'                |
|     max_cluster_count=1                   |
|     min_cluster_count=1                   |
|     scaling_policy=STANDARD               |
|     auto_suspend=600                      |
|     auto_resume=TRUE                      |
|     initially_suspended=TRUE              |
|     enable_query_acceleration=FALSE       |
|     query_acceleration_max_scale_factor=8 |
|     max_concurrency_level=8               |
|     statement_queued_timeout_in_seconds=0 |
|     statement_timeout_in_seconds=172800   |
| ;                                         |
+-------------------------------------------+
```

Note that the statement returned by the GET\_DDL function includes default values for the properties not specified in the CREATE
WAREHOUSE statement. For example, the CREATE WAREHOUSE statement did not specify the AUTO\_RESUME property, so the returned
statement includes AUTO\_RESUME=TRUE, which is the default value for this property.

### Hybrid tables

The following example shows the DDL that is returned for a hybrid table named `ht_weather`, which has a PRIMARY KEY
constraint on the `id` column.

Copy code

```
CREATE OR REPLACE HYBRID TABLE ht_weather
 (id INT PRIMARY KEY,
  start_time TIMESTAMP,
  precip NUMBER(3,2),
  city VARCHAR(20),
  county VARCHAR(20));
```

Note that the first argument to the function uses the `TABLE` type for hybrid tables.

Copy code

```
SELECT GET_DDL('TABLE','ht_weather');
```

The PRIMARY KEY constraint takes an out-of-line position in the output, after the column definitions.
See also [Constraints in GET\_DDL](/sql-reference/constraints-overview#label-constraints-in-get-ddl).

```
+---------------------------------------------+
| GET_DDL('TABLE','HT_WEATHER')               |
|---------------------------------------------|
| create or replace HYBRID TABLE HT_WEATHER ( |
|   ID NUMBER(38,0) NOT NULL,                 |
|   START_TIME TIMESTAMP_NTZ(9),              |
|   PRECIP NUMBER(3,2),                       |
|   CITY VARCHAR(20),                         |
|   COUNTY VARCHAR(20),                       |
|   primary key (ID)                          |
| );                                          |
+---------------------------------------------+
```

### Failover groups

Return the DDL used to create a failover group named `my_fg`:

Copy code

```
SELECT GET_DDL('FAILOVER_GROUP', 'my_fg');

+---------------------------------------------------------------+
| GET_DDL('FAILOVER_GROUP', 'MY_FG')                            |
+---------------------------------------------------------------+
| CREATE FAILOVER GROUP "my_fg"                                 |
|   OBJECT_TYPES = DATABASES, ROLES, WAREHOUSES                 |
|   ALLOWED_DATABASES = "my_db1", "my_db2"                      |
|   ALLOWED_ACCOUNTS = my_org.my_account1, my_org.my_account2   |
|   REPLICATION_SCHEDULE = '10 MINUTE';                         |
+---------------------------------------------------------------+
```

### Replication groups

Return the DDL used to create a replication group named `my_rg`:

Copy code

```
SELECT GET_DDL('REPLICATION_GROUP', 'my_rg');

+--------------------------------------------------------------------------------------+
| GET_DDL('REPLICATION_GROUP', 'MY_RG')                                                |
+--------------------------------------------------------------------------------------+
| CREATE REPLICATION GROUP "my_rg"                                                     |
|   OBJECT_TYPES = DATABASES, ROLES                                                    |
|   ALLOWED_DATABASES = "my_db"                                                        |
|   REPLICATION_ALLOWED_TO_ACCOUNTS = my_org.my_account1, my_org.my_account2;          |
+--------------------------------------------------------------------------------------+
```
