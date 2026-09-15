# Openflow Connector for Salesforce Bulk API: Salesforce formula fields

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how the Openflow Connector for Salesforce Bulk API translates Salesforce formula
fields into Snowflake SQL views, including supported functions and limitations.

## How formula views work

When **Enable Views Creation** is set to `true`, the connector performs the following for each object that has formula fields:

1. Retrieves the formula expressions from the Salesforce object metadata via the Describe API.
2. Parses each formula expression and translates it into equivalent Snowflake SQL.
3. Generates a `CREATE OR REPLACE VIEW` statement that combines non-formula columns from the base table with the translated formula expressions as computed columns.
4. Runs the DDL against Snowflake to create or update the view.

The resulting view is named `<Object Type>_FORMULA_VW`. For example, the `Account` object produces a view named `ACCOUNT_FORMULA_VW`. You can query this view to obtain formula field values alongside the replicated data.

The view is automatically updated whenever the connector detects schema changes in the source object, ensuring that formula definitions stay in sync with Salesforce.

## Cross-object formula fields

Salesforce formulas can reference fields from related objects using relationship traversal (for example, `Account.Owner.Name`). The connector supports these cross-object references by generating `LEFT JOIN` clauses in the view definition. Each relationship traversal produces a join to the corresponding related table in Snowflake.

For cross-object formulas to work correctly, the related objects must also be replicated by the connector. If a related object is not being synced, the formula columns that reference it are replaced with a typed `NULL` in the view. The remaining formula columns continue to compute normally. The affected columns have a `LOOKUP_NOT_SYNCED` comment. Once the referenced objects are added to replication and synced, the view is automatically rebuilt on the next connector run.

## Chained formula fields

Formula fields that reference other formula fields (chained formulas) are supported. The connector resolves the dependency graph before SQL generation and expands each referenced formula field’s expression into the referencing formula’s AST. Multi-hop chains are fully expanded. If a dependency cannot be translated, the dependent field also returns `NULL` and the column comment indicates `FORMULA_CHAIN_NOT_SUPPORTED`.

## Formula view column comments

Each formula column in the generated view includes a SQL `COMMENT` annotation:

- For successfully translated formulas, the comment contains the original Salesforce formula expression.
- For formulas that could not be translated, the comment contains the failure reason code followed by the original Salesforce formula expression, separated by a colon (for example, `FUNCTION_NOT_SUPPORTED: IMAGE(url, 'alt')`).

You can inspect these comments by running `DESCRIBE VIEW <view_name>` in Snowflake.

## Supported formula functions

The following Salesforce formula functions are translated into equivalent Snowflake SQL:

| Category | Salesforce function | Snowflake equivalent |
| --- | --- | --- |
| Logical | `IF` | `CASE WHEN ... THEN ... ELSE ... END` |
| Logical | `CASE` | `CASE ... WHEN ... THEN ... ELSE ... END` |
| Logical | `AND` / `OR` / `NOT` | `AND` / `OR` / `NOT` |
| Null handling | `ISBLANK` | `(expr IS NULL OR TO_VARCHAR(expr) = '')`; returns `FALSE` for boolean fields |
| Null handling | `ISNULL` | `expr IS NULL` |
| Null handling | `NULLVALUE` | `COALESCE` |
| Null handling | `BLANKVALUE` | `CASE WHEN expr IS NULL OR TO_VARCHAR(expr) = '' THEN default ELSE expr END` |
| Text | `LEFT` | `LEFT` |
| Text | `RIGHT` | `RIGHT` |
| Text | `MID` | `SUBSTR` |
| Text | `LEN` | `LENGTH` |
| Text | `SUBSTITUTE` | `REPLACE` |
| Text | `TRIM` | `TRIM` |
| Text | `UPPER` | `UPPER` |
| Text | `LOWER` | `LOWER` |
| Text | `CONTAINS` | `CONTAINS` |
| Text | `BEGINS` | `STARTSWITH` |
| Text | `FIND` | `CHARINDEX` |
| Text | `LPAD` | `LPAD` |
| Text | `RPAD` | `RPAD` |
| Text | `BR` | Newline character literal |
| Conversion | `TEXT` | `CAST(... AS STRING)` |
| Conversion | `VALUE` | `TRY_CAST(... AS NUMBER)` |
| Math | `ABS` | `ABS` |
| Math | `ROUND` | `ROUND` |
| Math | `CEILING` | `CEIL` |
| Math | `FLOOR` | `FLOOR` |
| Math | `MOD` | `MOD` |
| Math | `SQRT` | `SQRT` |
| Math | `MAX` | `GREATEST` |
| Math | `MIN` | `LEAST` |
| Math | `LOG` | `LOG(10, ...)` |
| Math | `EXP` | `EXP` |
| Math | `LN` | `LN` |
| Date and time | `NOW` | `CURRENT_TIMESTAMP()` |
| Date and time | `TODAY` | `CURRENT_DATE()` |
| Date and time | `YEAR` | `YEAR` |
| Date and time | `MONTH` | `MONTH` |
| Date and time | `DAY` | `DAY` |
| Date and time | `DATEVALUE` | `TO_DATE` |
| Date and time | `DATETIMEVALUE` | `TO_TIMESTAMP` |
| Date and time | `ADDMONTHS` | `DATEADD(MONTH, ...)` |
| Picklist | `ISPICKVAL` | `COALESCE(field, '') = COALESCE(value, '')` |

Expand

Show lessSee more

In addition to functions, the following operators are supported:

- Arithmetic: `+`, `-`, `*`, `/`, `^` (exponentiation, translated to `POWER`)
- Comparison: `=`, `==`, `!=`, `<>`, `<`, `<=`, `>`, `>=`
- Logical: `AND`, `OR`, `&&`, `||`
- String concatenation: `&` (translated to `||` with `COALESCE` null handling)
- Unary: `-` (negation), `NOT`

## Unsupported formula constructs

The following formula constructs are not yet supported. Support for additional functions and constructs will be added in future releases. When a formula uses any of these, the corresponding column in the view returns `NULL` and the column comment indicates the failure reason.

| Failure reason | Description |
| --- | --- |
| `FUNCTION_NOT_SUPPORTED` | The formula uses a function that has no Snowflake equivalent or that is specific to the Salesforce UI. This includes: `IMAGE`, `HYPERLINK`, `URLFOR`, `HTMLENCODE`, `JSENCODE`, `LINKTO`, `GEOLOCATION`, `DISTANCE`, `VLOOKUP`, `REGEX`, `PREDICT`, `GETSESSIONID`, `GETRECORDIDS`, `REQUIRESCRIPT`, `ISCHANGED`, `ISNEW`, `ISCLONE`, `PRIORVALUE`. |
| `GLOBAL_VARIABLE_NOT_SUPPORTED` | The formula references a Salesforce global variable such as `$User.Name`, `$Organization.Name`, or `$Profile.Name`. These variables have no equivalent in Snowflake. |
| `FORMULA_CHAIN_NOT_SUPPORTED` | A formula field in the chain could not be translated. When a formula field references another formula field (a chained formula), the connector expands the dependency before translation. If the dependency itself fails to translate, the referencing formula also fails with this reason code. This can also occur for cyclic formula references, which are not allowed by Salesforce. |
| `ROLLUP_NOT_SUPPORTED` | The field is a rollup summary field rather than a formula field. Rollup summaries aggregate data from child records and cannot be expressed as a simple SQL view. |
| `LOOKUP_NOT_SYNCED` | The formula references a relationship that cannot be resolved from the Salesforce object metadata. This typically occurs when the relationship name in the formula does not match any known relationship on the object. |
| `ID_FORMAT_MISMATCH` | The formula contains a hardcoded 15-character Salesforce ID. Salesforce uses 15-character IDs internally, but the Bulk API returns 18-character IDs. Formulas with hardcoded 15-character IDs cannot be reliably translated. |
| `COMPOUND_FIELD_REFERENCE` | The formula references a compound field (such as `MailingAddress`) that is not stored as a single column in Snowflake. |
| `PARSE_ERROR` | The formula expression could not be parsed. This might indicate a syntax that the connector does not yet recognize. |
| `UNSUPPORTED_SYNTAX` | The formula uses a syntax construct that is recognized but cannot be translated (for example, an `IF` function with fewer than three arguments). |

Expand

Show lessSee more
