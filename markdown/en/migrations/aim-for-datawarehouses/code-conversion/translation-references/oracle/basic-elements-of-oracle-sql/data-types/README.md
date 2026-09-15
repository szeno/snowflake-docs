# Oracle - Data Types

This section shows equivalents between data types in Oracle and Snowflake, as well as some notes on arithmetic differences.

| **Oracle** | **Snowflake** |
| --- | --- |
| [ANSI Data Types](#ansi-data-types) | *\*Go to the link to get more information* |
| [BFILE](oracle-built-in-data-types#bfile-data-type) | VARCHAR |
| [BINARY\_DOUBLE](oracle-built-in-data-types#binary_double) | FLOAT |
| [BINARY\_FLOAT](oracle-built-in-data-types#binary_float) | FLOAT |
| [BLOB](oracle-built-in-data-types#blob-data-type) | BINARY |
| [CHAR (N)](oracle-built-in-data-types#char-data-type) | CHAR (N) |
| [CLOB](oracle-built-in-data-types#clob-data-type) | VARCHAR |
| [DATE](oracle-built-in-data-types#date-data-type) | TIMESTAMP |
| [FLOAT](oracle-built-in-data-types#float-data-type) | FLOAT |
| [INTERVAL YEAR TO MONTH](oracle-built-in-data-types#interval-year-to-month-data-type) | VARCHAR(20) |
| [INTERVAL DAY TO SECOND](oracle-built-in-data-types#interval-day-to-second-data-type) | VARCHAR(20) |
| [JSON](oracle-built-in-data-types#json-data-type) | VARIANT |
| [LONG](oracle-built-in-data-types#long-data-type) | VARCHAR |
| [LONG RAW](oracle-built-in-data-types#raw-and-long-raw-data-types) | BINARY |
| [NCHAR (N)](oracle-built-in-data-types#nchar-data-type) | NCHAR (N) |
| [NCLOB](oracle-built-in-data-types#nclob-data-type) | VARCHAR |
| [NUMBER(p, s)](oracle-built-in-data-types#number-data-type) | NUMBER(p, s) |
| [NVARCHAR2 (N)](oracle-built-in-data-types#nvarchar2-data-type) | VARCHAR (N) |
| [RAW](oracle-built-in-data-types#raw-and-long-raw-data-types) | BINARY |
| [ROWID](./rowid-types) | VARCHAR(18) |
| [VARCHAR2 (N)](oracle-built-in-data-types#varchar2-data-type) | VARCHAR (N) |
| [SDO\_GOMETRY](./spatial-types#sdo_geometry) | Currently not supported |
| [SDO\_TOPO\_\_\_GEOMETRY](./spatial-types#sdo_topo_geometry) | *\*to be defined* |
| [SDO\_GEORASTER](./spatial-types#sdo_georaster) | *\*to be defined* |
| [SYS.ANYDATA](./any-types#anydata) | VARIANT |
| [SYS.ANYDATASET](./any-types#anydataset) | *\*to be defined* |
| [SYS.ANYTYPE](./any-types#anytype) | *\*to be defined* |
| [TIMESTAMP](oracle-built-in-data-types#timestamp-data-type) | TIMESTAMP |
| [TIMESTAMP WITH TIME ZONE](oracle-built-in-data-types#timestamp-with-time-zone-data-type) | TIMESTAMP\_TZ |
| [TIMESTAMP WITH LOCAL TIME ZONE](oracle-built-in-data-types#timestamp-with-local-time-zone-data-type) | TIMESTAMP\_LTZ |
| [URITYPE](xml-types#uri-data-types) | *\*to be defined* |
| [UROWID](rowid-types#urowid-data-type) | VARCHAR(18) |
| [VARCHAR](oracle-built-in-data-types#varchar-data-type) | VARCHAR |
| [VARCHAR2](oracle-built-in-data-types#varchar2-data-type) | VARCHAR |
| [XMLType](xml-types#xmltype) | VARIANT |

Expand

Show lessSee more

## Notes on arithmetic operations

Please be aware that every operation performed on numerical datatypes is internally stored as a Number. Furthermore, depending on the operation performed it is possible to incur an error related to how intermediate values are stored within Snowflake, for more information please check this post on [Snowflake’s post on intermediate numbers in Snowflake](https://community.snowflake.com/s/question/0D50Z00008HhSHCSA3/sql-compilation-error-invalid-intermediate-datatype-number7148).

## ANSI Data Types

### Description

> SQL statements that create tables and clusters can also use ANSI data types and data types from the IBM products SQL/DS and DB2. Oracle recognizes the ANSI or IBM data type name that differs from the Oracle Database data type name. It converts the data type to the equivalent Oracle data type, records the Oracle data type as the name of the column data type, and stores the column data in the Oracle data type based on the conversions shown in the tables that follow. ([Oracle Language Reference ANSI, DB2, and SQL/DS Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-0BC16006-32F1-42B1-B45E-F27A494963FF)).

When creating a new table, Oracle and Snowflake handle some data types as synonyms and aliases and transform them into the default data type. As shown in the next table:

| ANSI | ORACLE | SNOWFLAKE |
| --- | --- | --- |
| CHARACTER (n) | CHAR (n) | VARCHAR |
| CHAR (n) | CHAR (n) | VARCHAR |
| CHARACTER VARYING (n) | VARCHAR2 (n) | VARCHAR |
| CHAR VARYING (n) | VARCHAR2 (n) | VARCHAR |
| NATIONAL CHARACTER (n) | NCHAR (n) | VARCHAR\* |
| NATIONAL CHAR (n) | NCHAR (n) | VARCHAR\* |
| NCHAR (n) | NCHAR (n) | VARCHAR |
| NATIONAL CHARACTER VARYING (n) | NVARCHAR2 (n) | VARCHAR\* |
| NATIONAL CHAR VARYING (n) | NVARCHAR2 (n) | VARCHAR\* |
| NCHAR VARYING (n) | NVARCHAR2 (n) | NUMBER (p, s) |
| NUMERIC [(p, s)] | NUMBER (p, s) | NUMBER (p, s) |
| DECIMAL [(p, s)] | NUMBER (p, s) | NUMBER (38) |
| INTEGER | NUMBER (38) | NUMBER (38) |
| INT | NUMBER (38) | NUMBER (38) |
| SMALLINT | NUMBER (38) | NUMBER (38) |
| FLOAT | FLOAT (126) | DOUBLE |
| DOUBLE PRECISION | FLOAT (126) | DOUBLE |
| REAL | FLOAT (63) | DOUBLE |

Expand

Show lessSee more

To get more information about the translation specification of the Oracle data types, go to [Oracle Built-in Data Types](oracle-built-in-data-types).

Note

VARCHAR\*: Almost all the ANSI datatypes compile in Snowflake, but those marked with an asterisk, are manually converted to VARCHAR.

### Known Issues

No issues were found.

### Related EWIs

EWIs related to these data types are specified in the transformation of the [Oracle Built-in data types.](oracle-built-in-data-types)

## Data Type Customization

Data Type Customization is enabled to specify rules for data type transformation based on data type origin and column name. This feature allows you to personalize data type conversions and set precision values more accurately during migration.

For complete documentation on configuring data type customization, including JSON structure, configuration options, and priority rules, see [Data type mappings](#data-type-mappings).

### Data type mappings

Default mappings for data type conversions are defined. However, you can point to a JSON file to customize specific data type mappings.

**Customize data types:** You can upload a JSON file to define specific data type transformation rules. This feature allows you to customize how data types are converted during migration.

**Supported transformations include:**

- `NUMBER` to custom `NUMBER` with specific precision and scale
- `NUMBER` to `DECFLOAT` for preserving exact decimal precision

When you upload a data type customization file:

- Your transformation rules are applied during conversion
- Numeric literals in `INSERT` statements targeting customized columns are automatically cast to the appropriate type
- A [TypeMappings Report](/migrations/aim-for-datawarehouses/manual-migration/technical-documentation/type-mappings-report) is generated showing all data type transformations applied

**JSON Structure:**

The JSON file supports three ways to specify data type changes:

| Method | Scope | Use Case |
| --- | --- | --- |
| `projectTypeChanges.types` | Global | Transform all occurrences of a specific data type |
| `projectTypeChanges.columns` | Global | Transform columns matching a name pattern (case-insensitive substring match) |
| `specificTableTypeChanges.tables` | Table-specific | Transform specific columns in specific tables |

Expand

Show lessSee more

Warning

**Use column name patterns carefully.** The `projectTypeChanges.columns` rules only apply to columns with `NUMBER` data types, but they match by name pattern without considering the precision or scale of the original `NUMBER` type. This means a pattern like `"MONTH"` will transform **all** matching `NUMBER` columns to the target type, regardless of their original precision (e.g., `NUMBER(10,0)`, `NUMBER(38,18)`, or `NUMBER` without precision). Always review the [TypeMappings Report](/migrations/aim-for-datawarehouses/manual-migration/technical-documentation/type-mappings-report) after conversion to verify that the transformations were applied correctly.

**Priority order:** When multiple rules apply to the same column, the following priorities are used from highest to lowest:

1. `specificTableTypeChanges` (most specific)
2. `projectTypeChanges.columns` (name pattern)
3. `projectTypeChanges.types` (global type mapping)

**Example JSON configuration:**

Copy code

```
{
  "projectTypeChanges": {
    "types": {
      "NUMBER": "DECFLOAT",
      "NUMBER(10, 0)": "NUMBER(18, 0)"
    },
    "columns": [
      {
        "nameExpression": "PRICE",
        "targetType": "DECFLOAT"
      },
      {
        "nameExpression": ".*_AMOUNT$",
        "targetType": "NUMBER(18, 2)"
      }
    ]
  },
  "specificTableTypeChanges": {
    "tables": [
      {
        "tableName": "EMPLOYEES",
        "columns": [
          {
            "columnName": "SALARY",
            "targetType": "NUMBER(15, 2)"
          }
        ]
      }
    ]
  }
}
```

**Download template:** Copy and save the JSON structure above as your starting point.

**Example transformation:**

Given the following Oracle input code:

#### Oracle

Copy code

```
CREATE TABLE employees (
    employee_ID NUMBER,
    manager_YEAR NUMBER(10, 0),
    manager_MONTH NUMBER(10, 0),
    salary NUMBER(12, 2)
);
```

And a JSON customization file with:

- `"NUMBER": "NUMBER(11, 2)"` in `projectTypeChanges.types`
- `"NUMBER(10, 0)": "NUMBER(18, 0)"` in `projectTypeChanges.types`
- `"MONTH"` pattern targeting `NUMBER(2,0)` in `projectTypeChanges.columns`
- `SALARY` column targeting `NUMBER(15, 2)` in `specificTableTypeChanges` for EMPLOYEES table

The output will be:

#### Snowflake

Copy code

```
CREATE OR REPLACE TABLE employees (
    employee_ID NUMBER(11, 2),
    manager_YEAR NUMBER(18, 0),
    manager_MONTH NUMBER(2, 0),
    salary NUMBER(15, 2)
);
```

| Column | Original Type | Transformed To | Rule Applied |
| --- | --- | --- | --- |
| employee\_ID | NUMBER | NUMBER(11, 2) | `projectTypeChanges.types` |
| manager\_YEAR | NUMBER(10, 0) | NUMBER(18, 0) | `projectTypeChanges.types` |
| manager\_MONTH | NUMBER(10, 0) | NUMBER(2, 0) | `projectTypeChanges.columns` (MONTH pattern) |
| salary | NUMBER(12, 2) | NUMBER(15, 2) | `specificTableTypeChanges` (highest priority) |

Expand

Show lessSee more

### NUMBER to DECFLOAT Transformation

Transforming Oracle `NUMBER` columns to Snowflake `DECFLOAT` data type is supported. This is useful when you need to preserve the exact decimal precision of numeric values during migration.

When a `NUMBER` column is configured to be transformed to `DECFLOAT`:

1. The column data type in `CREATE TABLE` statements is transformed to `DECFLOAT`
2. Numeric literals in `INSERT` statements that target `DECFLOAT` columns are automatically wrapped with `CAST(... AS DECFLOAT)` to ensure proper data type handling
3. Column references in `INSERT ... SELECT` statements are also cast appropriately

#### Example

##### Oracle

Copy code

```
CREATE TABLE products (
    product_id NUMBER(10),
    price NUMBER(15, 2)
);

INSERT INTO products VALUES (1, 99.99);
```

##### Snowflake (with DECFLOAT customization for price column)

Copy code

```
CREATE OR REPLACE TABLE products (
    product_id NUMBER(10),
    price DECFLOAT
);

INSERT INTO products VALUES (1, CAST(99.99 AS DECFLOAT));
```

Note

The TypeMappings report (TypeMappings.csv) provides a detailed view of all data type transformations applied during conversion. See [TypeMappings Report](/migrations/aim-for-datawarehouses/manual-migration/technical-documentation/type-mappings-report) for more information.
