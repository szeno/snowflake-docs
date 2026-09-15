# Code Conversion - Druid Issues

This page provides a reference for the conversion issues reported when Apache Druid SQL and native queries are translated to Snowflake equivalents. For each issue you will find its severity, a description of when it is generated, a code example, and recommendations.

## SSC-EWI-DR0001

PARSE\_LONG with a radix other than 10 or 16 (or a non-literal radix) is not supported in Snowflake.

### Severity

Medium

#### Description

Druid’s `PARSE_LONG` accepts an optional radix argument that selects the numeric base used to interpret the input string. Snowflake’s [TRY\_TO\_NUMBER](/sql-reference/functions/try_to_number) covers only the decimal and hexadecimal cases through a format model, so there is no general base-N equivalent.

When the radix is a literal other than 10 or 16, or is a non-literal expression whose value cannot be resolved at conversion time, the call is left unchanged and this EWI is added to flag the need for manual conversion.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT PARSE_LONG(order_code, 2) FROM Orders;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT PARSE_LONG(order_code, 2) !!!RESOLVE EWI!!! /*** SSC-EWI-DR0001 - PARSE_LONG WITH A NON-DECIMAL/NON-HEXADECIMAL OR NON-LITERAL RADIX IS NOT SUPPORTED IN SNOWFLAKE ***/!!! FROM Orders;
```

#### Best Practices

1. **Replace the call with explicit base conversion logic.** For a fixed radix, decompose the string and accumulate the digit values, or expose the conversion as a UDF that is validated against representative source values.
2. **Resolve non-literal radix arguments first.** If the radix comes from a column or variable, determine which bases actually occur in the data; a single dominant base usually collapses into one of the supported decimal or hexadecimal paths.

## SSC-EWI-DR0002

Druid LOOKUP is not supported in Snowflake.

### Severity

Medium

#### Description

Druid’s `LOOKUP` resolves a value against a lookup namespace registered in the cluster, which is a Druid-managed structure with no Snowflake counterpart. The call is preserved unchanged and this EWI is added, including when the call appears nested inside an aggregate argument.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT COUNT(DISTINCT LOOKUP(product_id, 'product_names')) FROM Sales;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT COUNT(DISTINCT LOOKUP(product_id, 'product_names') !!!RESOLVE EWI!!! /*** SSC-EWI-DR0002 - DRUID LOOKUP IS NOT SUPPORTED IN SNOWFLAKE ***/!!!) FROM Sales;
```

#### Best Practices

1. **Materialize the lookup namespace as a Snowflake table.** Load the key-value pairs into a table and replace the `LOOKUP` call with a join on the key column.
2. **Preserve the miss behavior.** Druid returns `NULL` for keys that are absent from the namespace, so use a `LEFT JOIN` rather than an inner join when unmatched rows must survive.

## SSC-EWI-DR0003

Druid COMPLEX\_DECODE\_BASE64 decodes an internal complex (sketch) type that has no Snowflake equivalent.

### Severity

Medium

#### Description

`COMPLEX_DECODE_BASE64` deserializes a base64 payload into a Druid internal complex type, such as a `hyperUnique` sketch. Snowflake has no data type that can hold the decoded value, so the call is left unchanged and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT COMPLEX_DECODE_BASE64('hyperUnique', customer_sketch) FROM Metrics;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT COMPLEX_DECODE_BASE64('hyperUnique', customer_sketch) !!!RESOLVE EWI!!! /*** SSC-EWI-DR0003 - DRUID COMPLEX_DECODE_BASE64 DECODES AN INTERNAL COMPLEX (SKETCH) TYPE THAT IS NOT SUPPORTED IN SNOWFLAKE ***/!!! FROM Metrics;
```

#### Best Practices

1. **Recompute the metric from base rows.** Migrate the detail data that produced the sketch and rebuild the measure with a Snowflake aggregate such as [APPROX\_COUNT\_DISTINCT](/sql-reference/functions/approx_count_distinct).
2. **Do not migrate the serialized payload.** The encoded sketch is only meaningful to Druid’s implementation, so carrying the column over provides no usable value in Snowflake.

## SSC-EWI-DR0004

Druid APPEND merges datasources by column name; the generated UNION ALL pairs columns positionally and may differ or fail if the column lists differ.

### Severity

Medium

#### Description

A `TABLE(APPEND(...))` call with two or more datasources is rewritten as a derived table containing a `UNION ALL` of the sources. Druid aligns the merged datasources by column name and supplies `NULL` for columns missing from a source, whereas Snowflake’s `UNION ALL` aligns branches by ordinal position. This EWI is added because the rewrite can produce mismatched columns, or fail outright, whenever the source column lists are not identical.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT order_id FROM TABLE(APPEND('CurrentOrders', 'ArchivedOrders')) o;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT order_id FROM ( SELECT * FROM CurrentOrders UNION ALL SELECT * FROM ArchivedOrders ) o !!!RESOLVE EWI!!! /*** SSC-EWI-DR0004 - DRUID APPEND MERGES DATASOURCES BY COLUMN NAME; THE GENERATED UNION ALL PAIRS COLUMNS POSITIONALLY AND MAY DIFFER OR FAIL IF THE COLUMN LISTS DIFFER ***/!!!;
```

#### Best Practices

1. **Project an explicit, identically ordered column list in each branch.** Replacing `SELECT *` with named columns restores the name-based alignment that Druid applied.
2. **Add the missing columns as typed NULLs.** Where a source genuinely lacks a column, select `CAST(NULL AS <type>) AS <column>` in that branch so the branch widths and types line up.

## SSC-EWI-DR0005

Druid APPEND requires one or more literal string datasource names.

### Severity

Medium

#### Description

The `APPEND` rewrite depends on resolving each datasource name at conversion time. When the argument list is empty, or an argument is not a literal string, no valid `UNION ALL` can be produced, so the call is left unchanged and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT order_id FROM TABLE(APPEND()) o;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT order_id FROM TABLE(APPEND() !!!RESOLVE EWI!!! /*** SSC-EWI-DR0005 - DRUID APPEND REQUIRES ONE OR MORE LITERAL STRING DATASOURCE NAMES ***/!!!) o;
```

#### Best Practices

1. **Correct the source statement.** Druid itself rejects an empty `APPEND`, so an empty or non-literal argument list usually indicates dead or generated code that should be repaired or removed before conversion.
2. **Expand dynamic datasource lists manually.** If the names were assembled at runtime, enumerate the resulting datasources and write the corresponding `UNION ALL` query explicitly.

## SSC-EWI-DR0006

Druid query-context parameters other than `sqlTimeZone` are not supported in Snowflake.

### Severity

Medium

#### Description

Druid `SET` statements configure query-context parameters that tune the Druid engine. Only `sqlTimeZone` has a verified Snowflake session equivalent and is translated to `ALTER SESSION SET TIMEZONE`. Every other key is left in place with this EWI attached above it, signaling that no equivalent Snowflake session parameter was verified for that key.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SET vectorize = 'force';
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-DR0006 - DRUID QUERY-CONTEXT PARAMETER 'vectorize' IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
SET vectorize = 'force';
```

#### Best Practices

1. **Drop engine-tuning keys.** Parameters such as `vectorize` or `useApproximateCountDistinct` control Druid execution internals that Snowflake manages automatically, so they can usually be removed.
2. **Re-evaluate scope and units before mapping a key.** Parameters that look similar to a Snowflake setting often differ; for example, Druid’s `timeout` is expressed in milliseconds per query while [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#statement-timeout-in-seconds) is in seconds and applies at the session or warehouse level.

## SSC-EWI-DR0007

Druid REPLACE INTO … OVERWRITE WHERE was translated to INSERT INTO; prepend a matching DELETE for the target and predicate to preserve replacement behavior.

### Severity

Medium

#### Description

Druid’s `REPLACE INTO ... OVERWRITE WHERE` atomically drops the segments matching the predicate and then ingests the new rows. Snowflake has no single statement with that behavior, so the statement is translated to `INSERT INTO` and this EWI is added. The message embeds a ready-to-use `DELETE` template in which the target and the predicate are rendered from the source statement; the predicate text is reproduced verbatim, so Druid-specific functions inside it still require manual translation.

`REPLACE INTO ... OVERWRITE ALL` does not produce this EWI because it is translated to `INSERT OVERWRITE INTO`, which is row-set equivalent.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
REPLACE INTO DailySales
OVERWRITE WHERE __time >= TIMESTAMP '2025-01-01'
SELECT store_id, __time FROM SalesStage
WHERE __time >= TIMESTAMP '2025-01-01'
PARTITIONED BY ALL;
```

##### Output Code:

##### Snowflake

Copy code

```
INSERT INTO DailySales
SELECT store_id, __time FROM SalesStage
WHERE __time >= TIMESTAMP '2025-01-01'
!!!RESOLVE EWI!!! /*** SSC-EWI-DR0007 - DRUID REPLACE INTO ... OVERWRITE WHERE WAS TRANSLATED TO INSERT INTO; SEGMENT-DROP LOST. PREDICATE VERBATIM FROM DRUID SOURCE. TO PRESERVE ATOMIC REPLACE, PREPEND: DELETE FROM DailySales WHERE __time >= TIMESTAMP '2025-01-01'; ***/!!!;
```

#### Best Practices

1. **Prepend the supplied DELETE and wrap both statements in a transaction.** Running the delete and the insert inside a single [transaction](/sql-reference/transactions) restores the all-or-nothing behavior of the source statement.
2. **Review the predicate before executing it.** The predicate is copied verbatim, so any Druid-specific function it references must be translated first, otherwise the `DELETE` will fail or match the wrong rows.

## SSC-EWI-DR0008

A Druid native javascript aggregator has no Snowflake equivalent; the column was emitted as NULL. Reimplement the aggregation logic manually.

### Severity

Medium

#### Description

Druid native queries can define a `javascript` aggregator whose accumulate, combine, and reset behavior is expressed as JavaScript functions. Snowflake has no equivalent aggregate, so the output column is emitted as `NULL` with this EWI attached, keeping the rest of the converted query intact.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
{
  "queryType": "groupBy",
  "dataSource": "events",
  "granularity": "all",
  "dimensions": ["country"],
  "aggregations": [{
    "type": "javascript",
    "name": "js_agg",
    "fieldNames": ["amount"],
    "fnAggregate": "function(current, x) { return current + x; }",
    "fnCombine": "function(a, b) { return a + b; }",
    "fnReset": "function() { return 0; }"
  }],
  "intervals": ["2026-01-01T00:00:00Z/2026-02-01T00:00:00Z"]
}
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
country,
NULL AS js_agg /*** SSC-EWI-DR0008 - A DRUID NATIVE JAVASCRIPT AGGREGATOR HAS NO SNOWFLAKE EQUIVALENT; THE COLUMN WAS EMITTED AS NULL. REIMPLEMENT THE AGGREGATION LOGIC MANUALLY. ***/
FROM
events
WHERE
__time >= TIMESTAMP '2026-01-01 00:00:00'
AND __time < TIMESTAMP '2026-02-01 00:00:00'
GROUP BY
country;
```

#### Best Practices

1. **Express the accumulator in SQL when the logic is a standard reduction.** Many JavaScript aggregators are simple sums, counts, or conditional sums that map directly onto built-in Snowflake aggregates.
2. **Use a UDAF only for genuinely custom logic.** When the reduction cannot be expressed in SQL, implement a [user-defined aggregate function](/developer-guide/udf/python/udf-python-aggregate-functions) and validate it against Druid results before switching consumers over.

## SSC-EWI-DR0009

This Druid native query is not supported and produced no Snowflake SQL.

### Severity

Medium

#### Description

This issue is generated when a Druid native query is recognized but cannot be lowered to Snowflake SQL — for example, a `search` query without explicit `searchDimensions`, or one that carries a native `filter`. A comment stating the specific reason is emitted in place of the query so the output file is never silently empty.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
{
  "queryType": "search",
  "dataSource": "products",
  "searchDimensions": ["brand"],
  "query": {"type": "insensitive_contains", "value": "phone"},
  "filter": {"type": "selector", "dimension": "country", "value": "US"}
}
```

##### Output Code:

##### Snowflake

Copy code

```
-- SSC-EWI-DR0009: Native query could not be converted: Unsupported construct: filter
;
```

#### Best Practices

1. **Read the reason in the emitted comment.** The text after the code names the exact construct that blocked the conversion, which identifies the part of the query that must be rewritten.
2. **Rewrite the query as a Snowflake SELECT.** Map the dimensions to the projection, the native filter to a `WHERE` predicate, and the intervals to a `__time` range, then verify the result against the Druid output.

## SSC-EWI-DR0010

Some Druid native query types, such as `segmentMetadata`, have no Snowflake equivalent and are not converted.

### Severity

Medium

#### Description

Some Druid native query types do not read data rows at all. `segmentMetadata`, for example, introspects segment structure, which has no Snowflake data-query counterpart. A comment naming the query type is emitted instead of converted SQL.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
{
  "queryType": "segmentMetadata",
  "dataSource": "sales",
  "intervals": ["2026-01-01/2026-02-01"]
}
```

##### Output Code:

##### Snowflake

Copy code

```
-- ** SSC-EWI-DR0010 - THE DRUID 'segmentMetadata' NATIVE QUERY TYPE HAS NO SNOWFLAKE EQUIVALENT AND WAS NOT CONVERTED. **
```

#### Best Practices

1. **Use Snowflake metadata sources for introspection.** The [INFORMATION\_SCHEMA](/sql-reference/info-schema) views and [ACCOUNT\_USAGE](/sql-reference/account-usage) schema provide column, table, and storage metadata that cover most `segmentMetadata` use cases.
2. **Retire tooling tied to Druid segments.** Monitoring built around segment counts or sizes generally has no meaning against Snowflake micro-partitions and should be redesigned rather than translated.

## SSC-EWI-DR0011

FIRST\_VALUE and LAST\_VALUE without ORDER BY inside OVER are not supported in Snowflake. Add an ORDER BY clause.

### Severity

Medium

#### Description

Druid accepts `FIRST_VALUE` and `LAST_VALUE` with an `OVER` clause that specifies no ordering. Snowflake requires an `ORDER BY` inside the window specification for these functions, so the call is preserved and this EWI is added. The issue is also generated when the window is supplied through a named `WINDOW` clause that defines no ordering.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT FIRST_VALUE(order_total) OVER () FROM Orders;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT FIRST_VALUE(order_total) OVER () !!!RESOLVE EWI!!! /*** SSC-EWI-DR0011 - FIRST_VALUE AND LAST_VALUE WITHOUT ORDER BY INSIDE OVER ARE NOT SUPPORTED IN SNOWFLAKE. ADD AN ORDER BY CLAUSE. ***/!!! FROM Orders;
```

#### Best Practices

1. **Add the ordering the source implicitly relied on.** Druid queries of this shape commonly assume time order, so `ORDER BY __time` is a frequent match; confirm the intent before adopting it.
2. **Make the ordering deterministic.** If the chosen ordering expression contains ties, add a tie-breaking column so the selected row is stable across runs.

## SSC-EWI-DR0012

JSON\_PATHS is not supported in Snowflake. There is no recursive JSONPath enumerator.

### Severity

Medium

#### Description

Druid’s `JSON_PATHS` returns the set of JSONPath strings present in a nested value. Snowflake exposes no function that recursively enumerates paths, so the call is left unchanged and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT JSON_PATHS(payload) FROM Events;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT JSON_PATHS(payload) !!!RESOLVE EWI!!! /*** SSC-EWI-DR0012 - JSON_PATHS IS NOT SUPPORTED IN SNOWFLAKE ***/!!! FROM Events;
```

#### Best Practices

1. **Build the path set with recursive FLATTEN.** [FLATTEN](/sql-reference/functions/flatten) called with `RECURSIVE => TRUE` exposes a `PATH` column that can be aggregated to reproduce the enumeration.
2. **Prefer direct path access when the shape is known.** If the query only needs a fixed set of fields, read them with path notation instead of enumerating every path first.

## SSC-EWI-DR0013

STRING\_FORMAT is not supported in Snowflake. Java String.format has no Snowflake builtin.

### Severity

Medium

#### Description

Druid’s `STRING_FORMAT` applies Java `String.format` semantics, including its conversion specifiers, width, and locale handling. Snowflake has no built-in function with the same behavior, so the call is preserved and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT STRING_FORMAT('%s', customer_name) FROM Customers;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT STRING_FORMAT('%s', customer_name) !!!RESOLVE EWI!!! /*** SSC-EWI-DR0013 - STRING_FORMAT IS NOT SUPPORTED IN SNOWFLAKE ***/!!! FROM Customers;
```

#### Best Practices

1. **Rewrite simple format strings with concatenation.** Specifiers such as `%s` and `%d` usually reduce to `||` with an explicit cast on each argument.
2. **Use TO\_CHAR for numeric and date formatting.** Width, padding, and precision specifiers map onto [TO\_CHAR](/sql-reference/functions/to_char) format models, with [LPAD](/sql-reference/functions/lpad) or [RPAD](/sql-reference/functions/rpad) for fixed-width output.

## SSC-EWI-DR0014

BITWISE\_CONVERT\_\* IEEE bit conversion is not supported in Snowflake.

### Severity

Medium

#### Description

`BITWISE_CONVERT_DOUBLE_TO_LONG_BITS` and `BITWISE_CONVERT_LONG_BITS_TO_DOUBLE` reinterpret a value’s IEEE 754 binary representation. Snowflake exposes no equivalent conversion, so the call is preserved and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT BITWISE_CONVERT_DOUBLE_TO_LONG_BITS(metric_value) FROM Metrics;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT BITWISE_CONVERT_DOUBLE_TO_LONG_BITS(metric_value) !!!RESOLVE EWI!!! /*** SSC-EWI-DR0014 - BITWISE_CONVERT IEEE BIT CONVERSION IS NOT SUPPORTED IN SNOWFLAKE ***/!!! FROM Metrics;
```

#### Best Practices

1. **Identify what the bit pattern was used for.** These conversions typically support bit-packing, hashing, or ordering tricks that have simpler Snowflake alternatives such as [HASH](/sql-reference/functions/hash) or a direct `ORDER BY`.
2. **Implement and validate a UDF only if the exact encoding is required.** Round-trip a representative sample, including negative zero, infinities, and `NaN`, before relying on the result.

## SSC-EWI-DR0015

Apache DataSketches aggregates are not supported in Snowflake.

### Severity

Medium

#### Description

Aggregates backed by Apache DataSketches, such as `APPROX_COUNT_DISTINCT_DS_HLL`, `APPROX_COUNT_DISTINCT_DS_THETA`, and `DS_QUANTILES_SKETCH`, produce and merge sketch objects that Snowflake cannot represent. The call is left unchanged and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT APPROX_COUNT_DISTINCT_DS_HLL(customer_id) FROM Sales;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT APPROX_COUNT_DISTINCT_DS_HLL(customer_id) !!!RESOLVE EWI!!! /*** SSC-EWI-DR0015 - APACHE DATASKETCHES AGGREGATES ARE NOT SUPPORTED IN SNOWFLAKE ***/!!! FROM Sales;
```

#### Best Practices

1. **Map cardinality sketches onto Snowflake approximations.** [APPROX\_COUNT\_DISTINCT](/sql-reference/functions/approx_count_distinct) and its [HLL](/sql-reference/functions/hll) family cover the HLL and Theta distinct-count cases; [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile) covers quantile sketches.
2. **Recheck accuracy expectations.** Error bounds and merge semantics differ between DataSketches and the Snowflake implementations, so compare against exact values on a sample before accepting the substitution.

## SSC-EWI-DR0016

TABLE(EXTERN(…)) is not supported in Snowflake. It is a Druid ingestion table function.

### Severity

Medium

#### Description

`EXTERN` is a Druid ingestion table function that reads external data using an inline input source, input format, and signature specification. Snowflake loads external data through stages and file formats instead, so the call is preserved and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT * FROM TABLE(EXTERN('{}', '{}', '{}'));
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT * FROM TABLE(EXTERN('{}', '{}', '{}') !!!RESOLVE EWI!!! /*** SSC-EWI-DR0016 - TABLE(EXTERN(...)) IS NOT SUPPORTED IN SNOWFLAKE ***/!!!);
```

#### Best Practices

1. **Recreate the input source as a stage.** Define an external or internal [stage](/sql-reference/sql/create-stage) pointing at the same location, and a [file format](/sql-reference/sql/create-file-format) matching the Druid input format.
2. **Translate the signature into the target schema.** The column names and types declared in the `EXTERN` signature become the table definition or the `SELECT` projection over the staged files.

## SSC-EWI-DR0017

BIG\_SUM is not supported in Snowflake.

### Severity

Medium

#### Description

Druid’s `BIG_SUM` accumulates values using arbitrary-precision arithmetic to avoid overflow on very large totals. Snowflake has no aggregate with the same unbounded behavior, so the call is preserved and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT BIG_SUM(amount) FROM Payments;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT BIG_SUM(amount) !!!RESOLVE EWI!!! /*** SSC-EWI-DR0017 - BIG_SUM IS NOT SUPPORTED IN SNOWFLAKE ***/!!! FROM Payments;
```

#### Best Practices

1. **Use SUM when the total fits Snowflake precision.** Snowflake `NUMBER` supports up to 38 digits, which covers most monetary and counter aggregations; confirm the maximum expected total first.
2. **Rescale or partition the aggregation when it does not fit.** Summing in smaller units, or aggregating per group and combining afterward, keeps intermediate values inside the supported range.

## SSC-EWI-DR0018

IPV6\_MATCH is not supported in Snowflake.

### Severity

Medium

#### Description

`IPV6_MATCH` tests whether an IPv6 address falls inside a CIDR block. Snowflake provides no built-in IPv6 or CIDR matching function, so the call is left unchanged and this EWI is added.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT IPV6_MATCH(client_ip, '2001:db8::/32') FROM AccessLog;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT IPV6_MATCH(client_ip, '2001:db8::/32') !!!RESOLVE EWI!!! /*** SSC-EWI-DR0018 - IPV6_MATCH IS NOT SUPPORTED IN SNOWFLAKE ***/!!! FROM AccessLog;
```

#### Best Practices

1. **Compare on a normalized, fixed-width form.** Expanding each address to its full 32 hex digits at load time turns prefix matching into a plain string comparison on the leading characters.
2. **Filter upstream when the CIDR set is static.** If only a few blocks are ever matched, tagging rows during ingestion avoids reimplementing CIDR arithmetic in the query layer.
