# Code Conversion - Vertica Issues

## SSC-EWI-VT0001

Inherited privileges clause is not supported in Snowflake.

### Description

Vertica’s **`INCLUDE SCHEMA PRIVILEGES`** allows views to inherit schema-level privileges, unlike Snowflake where view access is managed by explicit **`GRANT`** statements. Migrating these Vertica views to Snowflake requires manually translating these inherited permissions into specific **`GRANTs` .**

#### Code Example

##### Input Code:

##### Vertica

Copy code

```
 CREATE OR REPLACE VIEW mySchema.myuser
INCLUDE SCHEMA PRIVILEGES
AS
SELECT lastname FROM users;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE VIEW mySchema.myuser
!!!RESOLVE EWI!!! /*** SSC-EWI-VT0001 - INHERITED PRIVILEGES CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
INCLUDE SCHEMA PRIVILEGES
AS
SELECT lastname FROM
    users;
```

#### Best Practices

- For Snowflake, the recommendation is to translate these inherited Vertica permissions by using **`GRANT`** statements to assign the necessary privileges on the view directly to specific roles.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-VT0002

Order by table option is not supported in Snowflake

### Description

In Vertica, this `ORDER BY` clause specifies how data is physically sorted within a **superprojection**, an optimized storage structure for a table. This explicit physical ordering at table creation is not directly supported in Snowflake.

Snowflake handles data storage differently, utilizing **micro-partitions**. While the data within these micro-partitions can exhibit some natural order based on insertion or if **clustering keys** are defined, an `ORDER BY` clause is not used to dictate this physical arrangement during table creation in the same explicit manner as in Vertica’s superprojections. Instead, Snowflake employs clustering to optimize data layout for performance, providing a more automated approach to physical ordering.

#### Code Example

##### Input Code:

##### Vertica

Copy code

```
 CREATE TABLE metrics
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
ORDER BY measurement_date, business_unit, metric_category;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE metrics
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
!!!RESOLVE EWI!!! /*** SSC-EWI-VT0002 - ORDER BY TABLE OPTION IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
ORDER BY measurement_date, business_unit, metric_category
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

#### Best Practices

- For Snowflake, the recommendation is to add **clustering keys** to emulate this behavior, following [Snowflake’s own recommendations for clustering key implementation](https://docs.snowflake.com/en/user-guide/tables-clustering-keys).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
