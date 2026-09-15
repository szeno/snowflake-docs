# Using an SQL query as a logical table in a semantic view

You can use an SQL query (rather than a physical table) as the logical table in a semantic view.

## Defining a logical table as an SQL query

To specify the SQL query, use the AS clause in the definition of the logical table:

Copy code

```
CREATE [ OR REPLACE ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
  TABLES (
    <table_alias> AS ( <query> )
      ... other keywords for the logical table ...
    [ , ... ]
  )

  ...
```

Note

- When you specify an SQL query for a logical table, the alias for the logical table is required.
- You can’t use [session variables](/sql-reference/session-variables) in the query.
- The query that you specify has the [same limitations](/sql-reference/sql/create-view#label-create-view-usage-notes) as the query that you specify in
  the AS clause of the CREATE VIEW command.

For example, suppose that you have two tables for customer information and customer addresses:

Copy code

```
CREATE OR REPLACE TABLE customer(
  c_cust_id VARCHAR,
  c_first_name VARCHAR,
  c_last_name VARCHAR
);

INSERT INTO customer VALUES
  ('cust001', 'Mary', 'Smith'),
  ('cust002', 'Bill', 'Wilson');

CREATE OR REPLACE TABLE customer_address(
  ca_cust_id VARCHAR,
  ca_zipcode VARCHAR,
  ca_street_addr VARCHAR
);

INSERT INTO customer_address VALUES
  ('cust001', '94027', '300 Main Street'),
  ('cust002', '94030', '600 Main Street');
```

If you want to define a logical table that corresponds to an SQL query that joins these two tables, you can specify the SQL query
in the AS clause of the logical table definition:

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW my_customer_sv
  TABLES (
    customer_info AS (
      SELECT * FROM customer JOIN customer_address
        ON customer.c_cust_id = customer_address.ca_cust_id
    ) PRIMARY KEY (c_cust_id) WITH SYNONYMS ('customer_details')
      COMMENT = 'Information about customers'
  )
  DIMENSIONS (
    customer_info.first_name AS customer_info.c_first_name,
    customer_info.last_name AS customer_info.c_last_name,
    customer_info.street_address AS customer_info.ca_street_addr,
    customer_info.zip_code AS customer_info.ca_zipcode
  );
```

The following statement queries this semantic view:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
  my_customer_sv
  DIMENSIONS customer_info.first_name, customer_info.last_name,
    customer_info.street_address, customer_info.zip_code
);
```

```
+------------+-----------+-----------------+----------+
| FIRST_NAME | LAST_NAME | STREET_ADDRESS  | ZIP_CODE |
|------------+-----------+-----------------+----------|
| Bill       | Wilson    | 600 Main Street | 94030    |
| Mary       | Smith     | 300 Main Street | 94027    |
+------------+-----------+-----------------+----------+
```

## Specifying a logical table as an SQL query in the YAML specification

To define a logical table as an SQL query in the
[YAML specification for a semantic view](/user-guide/views-semantic/semantic-view-yaml-spec), specify the `definition`
name/value pair under `base_table`:

Copy code

```
name: MY_CUSTOMER_SV
  tables:
  - name: CUSTOMER_INFO
    ...
    base_table:
      definition: SELECT * FROM customer JOIN customer_address ON customer.c_cust_id = customer_address.ca_cust_id
```

Note

If you specify `definition` under `base_table`, you can’t specify `database`, `schema`, and `table`.

Similarly, if you specify `database`, `schema`, or `table`, you can’t specify `definition`.

## How logical tables as SQL queries appear in DESC SEMANTIC VIEW and Snowflake views

The output of the [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) command includes a `DEFINITION` property for logical tables
(where `object_kind` is `TABLE`).

- If a logical table is set to an SQL query, the output includes the `DEFINITION` property, which is set to the SQL query.

  The `BASE_TABLE_DATABASE_NAME`, `BASE_TABLE_SCHEMA_NAME`, and `BASE_TABLE_NAME` properties do not appear in the output.
- If a logical table is set to a physical table, the output includes the `BASE_TABLE_DATABASE_NAME`, `BASE_TABLE_SCHEMA_NAME`,
  and `BASE_TABLE_NAME` properties, which are set to the names of the database containing the physical table, the schema
  containing the physical table, and the physical table.

  The `DEFINITION` property does not appear in the output.

For example, the following statement prints out the properties of the `my_customer_sv` semantic view:

Copy code

```
DESC SEMANTIC VIEW my_customer_sv;
```

```
+-------------+----------------+---------------+-----------------+--------------------------------------------------------------------------------------------------+
| object_kind | object_name    | parent_entity | property        | property_value                                                                                   |
|-------------+----------------+---------------+-----------------+--------------------------------------------------------------------------------------------------|
| TABLE       | CUSTOMER_INFO  | NULL          | DEFINITION      | SELECT * FROM customer JOIN customer_address ON customer.c_cust_id = customer_address.ca_cust_id |
| TABLE       | CUSTOMER_INFO  | NULL          | SYNONYMS        | ["customer_details"]                                                                             |
| TABLE       | CUSTOMER_INFO  | NULL          | PRIMARY_KEY     | ["C_CUST_ID"]                                                                                    |
| TABLE       | CUSTOMER_INFO  | NULL          | COMMENT         | Information about customers                                                                      |
...
```

The [ACCOUNT\_USAGE SEMANTIC\_TABLES view](/sql-reference/account-usage/semantic_tables) and
[INFO\_SCHEMA SEMANTIC\_TABLES view](/sql-reference/info-schema/semantic_tables) include a `definition` column at the
end of the column list. The `definition` column includes the SQL query for the table:

Copy code

```
SELECT semantic_table_name, definition
  FROM SNOWFLAKE.ACCOUNT_USAGE.SEMANTIC_TABLES
  WHERE semantic_view_name = 'MY_CUSTOMER_SV';
```

```
+---------------------+--------------------------------------------------------------------------------------------------+
| SEMANTIC_TABLE_NAME | DEFINITION                                                                                       |
|---------------------+--------------------------------------------------------------------------------------------------|
| CUSTOMER_INFO       | SELECT * FROM customer JOIN customer_address ON customer.c_cust_id = customer_address.ca_cust_id |
+---------------------+--------------------------------------------------------------------------------------------------+
```

Copy code

```
SELECT name, definition
  FROM INFORMATION_SCHEMA.SEMANTIC_TABLES
  WHERE semantic_view_name = 'MY_CUSTOMER_SV';
```

```
+---------------+--------------------------------------------------------------------------------------------------+
| NAME          | DEFINITION                                                                                       |
|---------------+--------------------------------------------------------------------------------------------------|
| CUSTOMER_INFO | SELECT * FROM customer JOIN customer_address ON customer.c_cust_id = customer_address.ca_cust_id |
+---------------+--------------------------------------------------------------------------------------------------+
```
