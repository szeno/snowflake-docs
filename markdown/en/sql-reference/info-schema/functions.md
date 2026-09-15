# FUNCTIONS view

This Information Schema view displays a row for each user-defined function (UDF), external function, or data metric function defined in the
specified (or current) database.

For more information about external functions, see [Writing external functions](/sql-reference/external-functions).
For more information about UDFs, see [User-defined functions overview](/developer-guide/udf/udf-overview).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| FUNCTION\_CATALOG | VARCHAR | Database to which the function belongs. |
| FUNCTION\_SCHEMA | VARCHAR | Schema to which the function belongs. |
| FUNCTION\_NAME | VARCHAR | Function name. |
| FUNCTION\_OWNER | VARCHAR | Name of the role that owns the function. |
| ARGUMENT\_SIGNATURE | VARCHAR | Type signature of the function’s arguments. |
| DATA\_TYPE | VARCHAR | Data type of the function’s return value. |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER(9,0) | Maximum length in characters of a string return value. |
| CHARACTER\_OCTET\_LENGTH | NUMBER(9,0) | Maximum length in bytes of a string return value. |
| NUMERIC\_PRECISION | NUMBER(9,0) | Numeric precision of numeric return value. |
| NUMERIC\_PRECISION\_RADIX | NUMBER(9,0) | Radix of precision of numeric return value. |
| NUMERIC\_SCALE | NUMBER(9,0) | Scale of numeric return value. |
| FUNCTION\_LANGUAGE | VARCHAR | Language of the function’s handler. |
| FUNCTION\_DEFINITION | VARCHAR | Definition of the function’s handler. |
| VOLATILITY | VARCHAR | VOLATILE if the function is [volatile](/sql-reference/sql/create-function#label-create-function-volatile-immutable); IMMUTABLE if it is [immutable](/sql-reference/sql/create-function#label-create-function-volatile-immutable). |
| IS\_NULL\_CALL | VARCHAR(3) | `YES` if the function is [called on null input](/sql-reference/sql/create-function#label-create-function-called-on-null-input); otherwise, `NO`. |
| IS\_SECURE | VARCHAR(3) | `YES` if the function is [secure](/developer-guide/secure-udf-procedure); otherwise, `NO`. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the function. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for the function. |
| IS\_EXTERNAL [[1]](#footnote-1) | VARCHAR(3) | `YES` if the function is an [external function](/sql-reference/external-functions); otherwise, `NO`. |
| API\_INTEGRATION [[1]](#footnote-1) | VARCHAR | Name of the [API integration object to authenticate](/sql-reference/external-functions-introduction#label-external-function-api-integration) the call to the proxy service an external function makes. |
| CONTEXT\_HEADERS [[1]](#footnote-1) | VARCHAR | Context header information for the external function. |
| MAX\_BATCH\_ROWS [[1]](#footnote-1) | NUMBER(9,0) | Maximum number of rows in each batch sent to the proxy service for an external function. |
| REQUEST\_TRANSLATOR [[1]](#footnote-1) | VARCHAR | Name of the external function’s [request translator](/sql-reference/external-functions-translators) (if any). |
| RESPONSE\_TRANSLATOR [[1]](#footnote-1) | VARCHAR | Name of the external function’s [response translator](/sql-reference/external-functions-translators) (if any). |
| COMPRESSION [[1]](#footnote-1) | VARCHAR | Type of compression used for serializing function payload. |
| IMPORTS | VARCHAR | Names of files (including their stage location and path) containing imported libraries. |
| HANDLER | VARCHAR | Name of the handler function or class. |
| TARGET\_PATH | VARCHAR | Path to the stage in which Snowflake stores the compiled result of [inline handler code](/developer-guide/inline-or-staged). |
| RUNTIME\_VERSION | VARCHAR | Runtime version of the function’s handler language; NULL if the function handler is written in SQL or JavaScript. |
| PACKAGES | VARCHAR | Names of packages specified in the PACKAGES clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) statement. Currently, this column applies only when the handler is written in Python, Java, or Scala. |
| INSTALLED\_PACKAGES | VARCHAR | Names of all packages installed by the function. This includes packages specified by the PACKAGES clause as well as their installed dependencies. Currently, this column applies only when the handler is written in Python. |
| IS\_MEMOIZABLE | VARCHAR(3) | `YES` if the function is [memoizable](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable); otherwise, `NO`. |
| EXTERNAL\_ACCESS\_INTEGRATIONS | VARCHAR | Names of [external access integrations](/developer-guide/external-network-access/external-network-access-overview) specified by the function’s EXTERNAL\_ACCESS\_INTEGRATIONS parameter. |
| SECRETS | VARCHAR | Map of [secrets](/sql-reference/sql/create-secret) specified by the function’s SECRETS parameter, where map keys are secret variable names and map values are secret object names. |
| IS\_DATA\_METRIC | VARCHAR(3) | `YES` if the function is a [data metric function](/user-guide/data-quality-intro); otherwise, `NO`. |
| IS\_AGGREGATE | VARCHAR(3) | `YES` if the function is an aggregate function; otherwise, `NO`. |
| ARTIFACT\_REPOSITORY | VARCHAR | Name of the artifact repository used to resolve packages for the function. |

Expand

Show lessSee more

[1]
These fields apply only to [Writing external functions](/sql-reference/external-functions).

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
  The view does not honor the MANAGE GRANTS privilege and consequently might show less information compared to a SHOW command when both are
  executed by a user who holds the MANAGE GRANTS privilege.

- Omitting a length for the VARCHAR type results in a VARCHAR that specifies the default maximum length. For more information, see
  [VARCHAR](/sql-reference/data-types-text#label-data-types-text-varchar).

- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
