# Code Conversion - Hive Functional Differences

## SSC-FDM-HV0001

Inserting values into an external table is not supported in Snowflake

### Description

Hive Format tables allow you to insert values, but Snowflake External Tables do not support value insertions. This means that while the table structure will be converted, any operations that attempt to insert data directly into the external table in Snowflake will fail.

### Code Example

#### Input

##### Spark

Copy code

```
 CREATE EXTERNAL TABLE IF NOT EXISTS External_table_hive_format
(
  order_id int,
  date string,
  client_name string,
  total float
)
stored as AVRO
LOCATION 'gs://sc_external_table_bucket/folder_with_avro/orders.avro';
```

#### Output

##### Snowflake

Copy code

```
 --** SSC-FDM-HV0001 - INSERTING VALUES INTO AN EXTERNAL TABLE IS NOT SUPPORTED IN SNOWFLAKE **
CREATE EXTERNAL TABLE IF NOT EXISTS hive_format_orders_Andres
(
  order_id int AS CAST(GET_IGNORE_CASE($1, 'order_id') AS int),
  date string AS CAST(GET_IGNORE_CASE($1, 'date') AS string),
  client_name string AS CAST(GET_IGNORE_CASE($1, 'client_name') AS string),
  total float AS CAST(GET_IGNORE_CASE($1, 'total') AS float)
)
!!!RESOLVE EWI!!! /*** SSC-EWI-0032 - EXTERNAL TABLE REQUIRES AN EXTERNAL STAGE TO ACCESS gs:, DEFINE AND REPLACE THE EXTERNAL_STAGE PLACEHOLDER ***/!!!
LOCATION = @EXTERNAL_STAGE
AUTO_REFRESH = false
FILE_FORMAT = (TYPE = AVRO)
PATTERN = '/sc_external_table_bucket/folder_with_avro/orders.avro'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "spark",  "convertedOn": "06/18/2025",  "domain": "no-domain-provided" }}';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-HV0002

Partitioned column added to table definition

### Description

For Hive/Spark partitioned tables, the partition columns are stored in the directory structure rather than in the table data. Snowflake does not support this pattern. The partitioned columns are added to the table definition as regular columns so the table schema is complete.

### Code Example

#### Input

##### Hive

Copy code

```
 CREATE EXTERNAL TABLE sales_data
(
  product_id INT,
  amount DECIMAL(10,2)
)
PARTITIONED BY (sale_month STRING)
STORED AS PARQUET
LOCATION 's3://bucket/sales/';
```

#### Output

##### Snowflake

Copy code

```
 CREATE EXTERNAL TABLE sales_data (
  product_id INT,
  amount DECIMAL(10,2),
  sale_month STRING
)
--** SSC-FDM-HV0002 - PARTITIONED COLUMN ADDED TO TABLE DEFINITION. **
LOCATION = @EXTERNAL_STAGE
FILE_FORMAT = (TYPE = PARQUET);
```

#### Best Practices

- Verify that partition columns are correctly mapped to your file path structure.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-HV0003

NULL format parameter is not supported in FROM\_UNIXTIME

### Description

Hive’s FROM\_UNIXTIME function allows a NULL format parameter, in which case it uses a default format. Snowflake’s equivalent (TO\_VARCHAR with TO\_TIMESTAMP\_NTZ) does not support a NULL format parameter. The NULL is passed through, but the conversion may fail at runtime or behave unexpectedly.

### Code Example

#### Input

##### Hive

Copy code

```
 SELECT FROM_UNIXTIME(1697328000, CAST(NULL AS STRING));
```

#### Output

##### Snowflake

Copy code

```
 SELECT
  --** SSC-FDM-HV0003 - NULL FORMAT PARAMETER IS NOT SUPPORTED IN FROM_UNIXTIME. **
  TO_VARCHAR(TO_TIMESTAMP_NTZ(1697328000), CAST(NULL AS STRING));
```

#### Best Practices

- Replace NULL format parameters with an explicit format string (e.g., ‘yyyy-MM-dd HH:mm:ss’).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-HV0004

INSTR transformed to REGEXP\_INSTR changes literal to regex pattern

### Description

Hive’s INSTR function uses literal string matching. Snowflake does not have INSTR; it is translated to REGEXP\_INSTR. REGEXP\_INSTR interprets the pattern as a regex, so metacharacters (e.g., `.`, `*`, `$`) will behave differently than in Hive’s literal matching.

### Code Example

#### Input

##### Hive

Copy code

```
 SELECT INSTR('price: $10.99', pattern_col, 1, 1);
```

#### Output

##### Snowflake

Copy code

```
 SELECT
  --** SSC-FDM-HV0004 - HIVE'S INSTR USES LITERAL STRING MATCHING, BUT REGEXP_INSTR INTERPRETS THE PATTERN AS A REGEX. METACHARACTERS WILL BEHAVE DIFFERENTLY. **
  REGEXP_INSTR('price: $10.99', pattern_col, 1, 1);
```

#### Best Practices

- When the pattern contains regex metacharacters, escape them or use REGEXP\_REPLACE to sanitize the pattern.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
