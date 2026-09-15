Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# FUNCTIONS view

This Account Usage view displays a row for each user-defined function (UDF) defined in the account.

For more information about UDFs, see [User-defined functions overview](/developer-guide/udf/udf-overview).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| FUNCTION\_ID | NUMBER | Internal/system-generated identifier for the UDF. |
| FUNCTION\_NAME | VARCHAR | Name of the UDF. |
| FUNCTION\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the UDF. |
| FUNCTION\_SCHEMA | VARCHAR | Schema which the UDF belongs to. |
| FUNCTION\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the UDF. |
| FUNCTION\_CATALOG | VARCHAR | Database which the UDF belongs to. |
| FUNCTION\_OWNER | VARCHAR | Name of the role that owns the UDF. |
| ARGUMENT\_SIGNATURE | VARCHAR | Type signature of the UDF’s arguments. |
| DATA\_TYPE | VARCHAR | Return value data type. |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER | Maximum length in characters of string return value. |
| CHARACTER\_OCTET\_LENGTH | NUMBER | Maximum length in bytes of string return value. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of numeric return value. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of precision of numeric return value. |
| NUMERIC\_SCALE | NUMBER | Scale of numeric return value. |
| FUNCTION\_LANGUAGE | VARCHAR | Language of the UDF. |
| FUNCTION\_DEFINITION | VARCHAR | UDF definition. |
| VOLATILITY | VARCHAR | Whether the UDF is volatile or immutable. |
| IS\_NULL\_CALL | VARCHAR | Whether the UDF is called when input is null. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the UDF was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the UDF was dropped. |
| COMMENT | VARCHAR | Comment for the function. |
| IS\_EXTERNAL [[1]](#footnote-1) | VARCHAR(3) | `YES` if the function is an [external function](/sql-reference/external-functions); otherwise, `NO`. |
| API\_INTEGRATION [[1]](#footnote-1) | VARCHAR | Name of the API integration object to authenticate the call to the proxy service. |
| CONTEXT\_HEADERS [[1]](#footnote-1) | VARCHAR | Context header information for the external function. |
| MAX\_BATCH\_ROWS [[1]](#footnote-1) | NUMBER | Maximum number of rows in each batch sent to the proxy service. |
| COMPRESSION [[1]](#footnote-1) | VARCHAR | Type of compression. |
| PACKAGES | VARCHAR | Packages requested by the function. |
| RUNTIME\_VERSION | VARCHAR | Runtime version of the language used by the function. NULL if the function is SQL or JavaScript. |
| INSTALLED\_PACKAGES | VARCHAR | All packages installed by the function. Output for Python functions only. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| IS\_MEMOIZABLE | VARCHAR(3) | `YES` if the function is [memoizable](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable); otherwise, `NO`. |
| IS\_DATA\_METRIC | VARCHAR(3) | `YES` if the function is a [data metric function](/user-guide/data-quality-intro); otherwise, `NO`. |
| SECRETS | JSON map | Map of [secrets](/sql-reference/sql/create-secret) specified by the function’s SECRETS parameter, where map keys are secret variable names and map values are secret object names. |
| EXTERNAL\_ACCESS\_INTEGRATIONS | VARCHAR | Names of [external access integrations](/developer-guide/external-network-access/external-network-access-overview) specified by the function’s EXTERNAL\_ACCESS\_INTEGRATION parameter. |
| IS\_AGGREGATE | VARCHAR(3) | `YES` if the function is an aggregate function; otherwise, `NO`. |

Expand

Show lessSee more

[1]
These fields apply only to [Writing external functions](/sql-reference/external-functions).

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not recognize the MANAGE GRANTS privilege and consequently might show less information compared to a SHOW command executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
