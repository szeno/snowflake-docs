# Code Conversion - Druid Functional Differences

This page provides a reference for the functional differences reported when Apache Druid SQL and native queries are translated to Snowflake equivalents. Each entry describes the behavior that changes, shows the generated code, and lists the checks to perform on the converted query.

## SSC-FDM-DR0001

EARLIEST/LATEST order by the Druid ‘\_\_time’ column. Verify the ‘\_\_time’ column exists in Snowflake and preserves the intended ordering.

#### Description

Druid’s `EARLIEST` and `LATEST` return the value associated with the smallest or largest `__time` value, using that column implicitly. They are translated to Snowflake [MIN\_BY](/sql-reference/functions/min_by) and [MAX\_BY](/sql-reference/functions/max_by) with `__time` supplied as an explicit ordering argument, so the result depends on that column being migrated and ordering the rows as it did in Druid.

The optional second argument of `EARLIEST` and `LATEST` is Druid’s `maxBytesPerValue` storage hint and is dropped during translation.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT EARLIEST(status) FROM Orders;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT MIN_BY(status, "__time") /*** SSC-FDM-DR0001 - EARLIEST/LATEST ORDER BY THE DRUID '__time' COLUMN. VERIFY THE '__time' COLUMN EXISTS IN SNOWFLAKE AND PRESERVES THE INTENDED ORDERING ***/ FROM Orders;
```

#### Best Practices

- Confirm that `__time` was migrated with the same name, and that its Snowflake type preserves the precision the ordering depends on.
- Check for ties on `__time`. When several rows share a timestamp, `MIN_BY` and `MAX_BY` may return any of them, so add a tie-breaker if the source relied on a stable pick.

## SSC-FDM-DR0002

Druid STRING\_AGG does not guarantee element order; a WITHIN GROUP (ORDER BY) clause was added for deterministic output, which may change the concatenation order.

#### Description

Druid’s `STRING_AGG` concatenates values in an unspecified order. It is translated to Snowflake [LISTAGG](/sql-reference/functions/listagg) with a `WITHIN GROUP (ORDER BY expression)` clause added so the output is deterministic. That ordering is derived from the aggregated expression, so the resulting sequence can differ from what the Druid query happened to produce. A `DISTINCT` quantifier in the source is carried through to the `LISTAGG` argument list.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT STRING_AGG(product_name, ',') FROM Products;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT LISTAGG(product_name, ',') WITHIN GROUP( ORDER BY product_name) /*** SSC-FDM-DR0002 - DRUID STRING_AGG DOES NOT GUARANTEE ELEMENT ORDER; A 'WITHIN GROUP (ORDER BY)' CLAUSE WAS ADDED FOR DETERMINISTIC OUTPUT, WHICH MAY CHANGE THE CONCATENATION ORDER ***/ FROM Products;
```

#### Best Practices

- Replace the generated ordering expression when the business logic expects a specific sequence, such as chronological order by `__time`.
- Treat downstream comparisons of the concatenated string as suspect. Snapshot tests that pinned a Druid-produced order will need to be rebaselined.

## SSC-FDM-DR0003

Druid ARRAY\_CONTAINS with an array argument tests subset containment; the translated Snowflake ARRAY\_CONTAINS tests element equality, so results may differ.

#### Description

When its second argument is an array, Druid’s `ARRAY_CONTAINS` (and the equivalent `MV_CONTAINS`) tests whether every element of that array is present in the first argument. The call is translated to Snowflake [ARRAY\_CONTAINS](/sql-reference/functions/array_contains) with the arguments flipped, but Snowflake tests whether a single value is an element of an array rather than performing subset containment, so the two can disagree.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT ARRAY_CONTAINS(tags, ARRAY['priority', 'open']) FROM Tickets;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT ARRAY_CONTAINS(ARRAY_CONSTRUCT('priority', 'open'), tags) /*** SSC-FDM-DR0003 - DRUID ARRAY_CONTAINS WITH AN ARRAY ARGUMENT TESTS SUBSET CONTAINMENT; THE TRANSLATED SNOWFLAKE ARRAY_CONTAINS TESTS ELEMENT EQUALITY, SO RESULTS MAY DIFFER ***/ FROM Tickets;
```

#### Best Practices

- Restore subset semantics explicitly, for example by requiring `ARRAY_CONTAINS` to hold for each searched element, or by comparing `ARRAY_SIZE(ARRAY_INTERSECTION(...))` against the size of the searched array.
- Single-value `ARRAY_CONTAINS` calls are unaffected; only the array-argument form needs review.

## SSC-FDM-DR0004

Druid ARRAY\_SLICE returns NULL for an out-of-bounds start; the translated Snowflake ARRAY\_SLICE returns an empty array for a positive start past the end and counts a negative start from the end, so results may differ.

#### Description

Druid allows `ARRAY_SLICE` (and `MV_SLICE`) to omit the end index, which slices to the end of the array. Snowflake [ARRAY\_SLICE](/sql-reference/functions/array_slice) requires the end, so `ARRAY_SIZE(array)` is supplied. The two engines then diverge on out-of-bounds starts: Druid returns `NULL`, while Snowflake returns an empty array for a positive start past the end and interprets a negative start as an offset from the end.

This difference is reported when the start is a literal that can be shown to be out of bounds. A start given as a column cannot be range-checked at conversion time, so no marker is emitted in that case.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT ARRAY_SLICE(items, -1) FROM Orders;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT ARRAY_SLICE(items, -1, ARRAY_SIZE(items)) /*** SSC-FDM-DR0004 - DRUID ARRAY_SLICE RETURNS NULL FOR AN OUT-OF-BOUNDS START; THE TRANSLATED SNOWFLAKE ARRAY_SLICE RETURNS AN EMPTY ARRAY FOR A POSITIVE START PAST THE END AND COUNTS A NEGATIVE START FROM THE END, SO RESULTS MAY DIFFER ***/ FROM Orders;
```

#### Best Practices

- Guard the call when downstream logic distinguishes `NULL` from an empty array, for example with a `CASE` that reproduces Druid’s `NULL` result for out-of-range starts.
- Review column-driven start expressions too. They are not flagged, but the same divergence applies whenever the runtime value falls outside the array bounds.

## SSC-FDM-DR0005

Druid REGEXP\_LIKE performs a partial match; the pattern was wrapped to emulate this under Snowflake’s full-string match. Verify anchored patterns, newlines, and Java-vs-Snowflake regex differences.

#### Description

Druid’s `REGEXP_LIKE` succeeds when the pattern matches anywhere in the input, whereas Snowflake [REGEXP\_LIKE](/sql-reference/functions/regexp_like) requires the pattern to match the entire string. The pattern is therefore wrapped as `.*(<pattern>).*` — folded into a single literal when the pattern is a literal, or built with concatenation when it is not.

The wrapper reproduces the partial-match behavior, but it does not reconcile the underlying regex dialects: Druid uses Java regular expressions, and anchors, newline handling, and Java-specific constructs can still behave differently.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT REGEXP_LIKE(customer_name, 'son') FROM Customers;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT REGEXP_LIKE(customer_name, '.*(son).*') /*** SSC-FDM-DR0005 - DRUID REGEXP_LIKE PERFORMS A PARTIAL MATCH; THE PATTERN WAS WRAPPED TO EMULATE THIS UNDER SNOWFLAKE FULL-STRING MATCH. VERIFY ANCHORED PATTERNS, NEWLINES, AND JAVA-VS-SNOWFLAKE REGEX DIFFERENCES ***/ FROM Customers;
```

#### Best Practices

- Re-examine patterns that already contained `^` or `$`. Combining them with the wrapper changes what the expression accepts.
- Test against multiline values. The `.` metacharacter does not match newlines by default, so a pattern that matched in Druid may fail on multiline input.

## SSC-FDM-DR0006

Druid PARSE\_LONG returns NULL for non-integer text; Snowflake TRY\_TO\_NUMBER may instead round decimals, trim whitespace, or parse scientific notation. Verify inputs that are not plain integers.

#### Description

`PARSE_LONG` with no radix, or with an explicit radix of 10, is translated to Snowflake [TRY\_TO\_NUMBER](/sql-reference/functions/try_to_number). Druid returns `NULL` for any text that is not a plain integer, whereas `TRY_TO_NUMBER` is more permissive: it can round decimal values, tolerate surrounding whitespace, and parse scientific notation.

The radix-16 path uses a hexadecimal format model and does not exhibit this leniency, so it carries no marker.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT PARSE_LONG(order_code) FROM Orders;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT TRY_TO_NUMBER(order_code) /*** SSC-FDM-DR0006 - DRUID PARSE_LONG RETURNS NULL FOR NON-INTEGER TEXT; SNOWFLAKE TRY_TO_NUMBER MAY INSTEAD ROUND DECIMALS, TRIM WHITESPACE, OR PARSE SCIENTIFIC NOTATION. VERIFY INPUTS THAT ARE NOT PLAIN INTEGERS ***/ FROM Orders;
```

#### Best Practices

- Add an integer-only validation, such as a `REGEXP_LIKE` guard, when the source logic depended on `NULL` being returned for malformed values.
- Pay particular attention to rows counted or filtered by `IS NULL`. Values that Druid rejected may now parse successfully and change those counts.

## SSC-FDM-DR0007

Druid TIME\_CEIL returns the input unchanged when it is already on a unit boundary; Snowflake TIME\_SLICE(…, ‘END’) always advances to the next boundary.

#### Description

Snowflake has no `DATE_CEIL` function, so Druid’s `TIME_CEIL` is translated to [TIME\_SLICE](/sql-reference/functions/time_slice) with the `END` boundary. The two agree for timestamps inside a bucket, but differ exactly on a boundary: Druid returns the input unchanged, while `TIME_SLICE(..., 'END')` advances to the start of the next bucket.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT TIME_CEIL(event_time, 'PT1H') FROM Events;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT TIME_SLICE(event_time, 1, 'HOUR', 'END') /*** SSC-FDM-DR0007 - DRUID TIME_CEIL RETURNS THE INPUT UNCHANGED WHEN IT IS ALREADY ON A UNIT BOUNDARY; SNOWFLAKE TIME_SLICE(..., 'END') ALWAYS ADVANCES TO THE NEXT BOUNDARY ***/ FROM Events;
```

#### Best Practices

- Add an exact-boundary check when the difference matters, for example returning the input unchanged when it already equals its floored value.
- Assess how often boundary values actually occur. Data captured at whole hours or midnight hits this case frequently; irregular event timestamps rarely do.

## SSC-FDM-DR0008

ARRAY\_INTERSECTION returns distinct elements, so duplicates and order may not be preserved.

#### Description

Druid’s `MV_FILTER_ONLY` keeps the elements of an array that appear in a supplied list, preserving duplicates and position. It is translated to Snowflake [ARRAY\_INTERSECTION](/sql-reference/functions/array_intersection), which retains the same value set but returns distinct elements, so multiplicity and ordering can change.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT MV_FILTER_ONLY(tags, allowed_tags) FROM Products;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT ARRAY_INTERSECTION(tags, allowed_tags) /*** SSC-FDM-DR0008 - ARRAY_INTERSECTION RETURNS DISTINCT ELEMENTS, SO DUPLICATES AND ORDER MAY NOT BE PRESERVED ***/ FROM Products;
```

#### Best Practices

- Review consumers that read by index or count elements, since both depend on the duplicates and positions that are not preserved.
- Use a `FILTER` lambda that tests membership per element when the original multiplicity and order must be kept.

## SSC-FDM-DR0009

MV\_FILTER\_REGEX uses Java regex syntax; the translated Snowflake REGEXP\_INSTR uses a different regex dialect, so some patterns may match differently.

#### Description

`MV_FILTER_REGEX` keeps the array elements matching a Java regular expression. It is translated to a Snowflake [FILTER](/sql-reference/functions/filter) lambda that tests each element with [REGEXP\_INSTR](/sql-reference/functions/regexp_instr). The filtering structure is equivalent, but the regex dialects are not identical, so individual patterns can match differently.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT MV_FILTER_REGEX(tags, '^priority_') FROM Tickets;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT FILTER(tags, x -> REGEXP_INSTR(x, '^priority_') > 0) /*** SSC-FDM-DR0009 - MV_FILTER_REGEX USES JAVA REGEX SYNTAX; THE TRANSLATED SNOWFLAKE REGEXP_INSTR USES A DIFFERENT REGEX DIALECT, SO SOME PATTERNS MAY MATCH DIFFERENTLY ***/ FROM Tickets;
```

#### Best Practices

- Look for Java-specific constructs such as possessive quantifiers, `\\p{...}` character classes, or named groups, which need rewriting for Snowflake.
- Validate the translated pattern against a sample of real array values rather than only against the literal used in the query.

## SSC-FDM-DR0010

Druid CAST(x AS CHAR(n)) was rewritten to RPAD(CAST(x AS VARCHAR), n, ‘ ‘). Druid pads short strings with spaces to length n; Snowflake CHAR(n) does not pad. The rewrite preserves padding semantics.

#### Description

Druid pads a `CHAR(n)` result with trailing spaces up to length `n`, while Snowflake `CHAR(n)` performs no padding. To preserve the source behavior, the cast is rewritten as [RPAD](/sql-reference/functions/rpad) over a `VARCHAR` cast. The rewrite applies to every explicit length, including `CHAR(1)`.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT CAST(status_code AS CHAR(5)) FROM Orders;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT RPAD(CAST(status_code AS VARCHAR), 5, ' ') /*** SSC-FDM-DR0010 - DRUID CAST(x AS CHAR(n)) WAS REWRITTEN TO RPAD(CAST(x AS VARCHAR), n, ' '). DRUID PADS SHORT STRINGS WITH SPACES TO LENGTH n; SNOWFLAKE CHAR(n) DOES NOT PAD. THE REWRITE PRESERVES PADDING SEMANTICS. ***/ FROM Orders;
```

#### Best Practices

- Check equality comparisons, joins, and hashes on the result, because the retained trailing spaces are significant in Snowflake.
- Drop the `RPAD` wrapper where the padding was incidental rather than required by a downstream fixed-width consumer.

## SSC-FDM-DR0011

Druid bare CAST(x AS CHAR) (no length) was rewritten to CAST(x AS VARCHAR). Snowflake’s bare CHAR is CHAR(1) and rejects multi-character input; Druid’s bare CHAR is unbounded.

#### Description

A bare `CHAR` in Druid is an unbounded string type, whereas Snowflake treats bare `CHAR` as `CHAR(1)`, which rejects multi-character input. The cast is therefore rewritten to `VARCHAR` so that longer values continue to convert successfully.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT CAST(customer_name AS CHAR) FROM Customers;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT CAST(customer_name AS VARCHAR) /*** SSC-FDM-DR0011 - DRUID BARE CAST(x AS CHAR) (NO LENGTH) WAS REWRITTEN TO CAST(x AS VARCHAR). SNOWFLAKE'S BARE CHAR IS CHAR(1) AND REJECTS MULTI-CHARACTER INPUT; DRUID'S BARE CHAR IS UNBOUNDED. ***/ FROM Customers;
```

#### Best Practices

- Accept the rewrite in most cases; it is what keeps multi-character values from failing the cast.
- Add an explicit `VARCHAR(n)` only when a downstream table or interface enforces a maximum length.

## SSC-FDM-DR0012

Druid CAST(x AS BOOLEAN) returns a LONG value (0/1); Snowflake returns a native BOOLEAN (TRUE/FALSE). Logical truth is preserved, but code that compares to 1/0 or concatenates the result will see different values.

#### Description

The cast syntax passes through unchanged, but the result type does not: Druid produces a numeric `LONG` of 0 or 1, while Snowflake produces a native `BOOLEAN`. Predicates keep working because the logical truth value is the same, but expressions that treat the result as a number or a string will see `TRUE` and `FALSE` instead of 1 and 0.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT CAST(is_active AS BOOLEAN) FROM Customers;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT CAST(is_active AS BOOLEAN) /*** SSC-FDM-DR0012 - DRUID CAST(x AS BOOLEAN) RETURNS A LONG VALUE (0/1); SNOWFLAKE RETURNS A NATIVE BOOLEAN (TRUE/FALSE). LOGICAL TRUTH IS PRESERVED, BUT CODE THAT COMPARES TO 1/0 OR CONCATENATES THE RESULT WILL SEE DIFFERENT VALUES. ***/ FROM Customers;
```

#### Best Practices

- Replace comparisons such as `= 1` or `= 0` with direct boolean predicates.
- Cast explicitly where the numeric or string form is required, for example `CAST(... AS BOOLEAN)::INT` for arithmetic, and check reports or exports that displayed 1 and 0.

## SSC-FDM-DR0013

Druid CAST(x AS DECIMAL/NUMERIC) was rewritten to CAST(x AS FLOAT)

#### Description

Druid treats `DECIMAL` and `NUMERIC` as approximate types backed by a double, so the cast is rewritten to Snowflake `FLOAT` to match that runtime behavior. Any declared precision and scale is dropped, and the result is subject to floating-point rounding rather than exact decimal arithmetic. The rewrite also applies when the operand is `NULL`.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
SELECT CAST(order_total AS DECIMAL(10, 2)) FROM Orders;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT CAST(order_total AS FLOAT) /*** SSC-FDM-DR0013 - DRUID CAST(x AS DECIMAL/NUMERIC) WAS REWRITTEN TO CAST(x AS FLOAT) ***/ FROM Orders;
```

#### Best Practices

- Replace the cast with `NUMBER(precision, scale)` for monetary or otherwise exact calculations, where floating-point rounding is not acceptable.
- Review equality comparisons and sums over many rows, which are the places where accumulated floating-point error becomes visible.

## SSC-FDM-DR0014

Druid PARTITIONED BY <granularity> specifies ingestion-time segment bucketing; the translated Snowflake INSERT omits the clause and relies on micro-partitions, so time-bucketed segmentation is not preserved.

#### Description

In Druid ingestion DML, `PARTITIONED BY <granularity>` buckets the ingested rows into time-based segments. Snowflake organizes table storage into [micro-partitions](/user-guide/tables-clustering-micropartitions) automatically, so the clause is dropped from the generated `INSERT` and this difference is reported.

`PARTITIONED BY ALL` (and its `ALL TIME` synonym) is the Druid sentinel for “do not time-partition”, so it is inert and produces no marker.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
INSERT INTO DailySales SELECT * FROM SalesStage PARTITIONED BY DAY;
```

##### Output Code:

##### Snowflake

Copy code

```
INSERT INTO DailySales SELECT * FROM SalesStage /*** SSC-FDM-DR0014 - DRUID PARTITIONED BY <GRANULARITY> SPECIFIES INGESTION-TIME SEGMENT BUCKETING; THE TRANSLATED SNOWFLAKE INSERT OMITS THE CLAUSE AND RELIES ON MICRO-PARTITIONS, SO TIME-BUCKETED SEGMENTATION IS NOT PRESERVED ***/;
```

#### Best Practices

- Rely on automatic micro-partitioning first. Snowflake prunes on the time column without any explicit partitioning clause.
- Consider [clustering](/user-guide/tables-clustering-keys) on the time column only if query profiles show poor pruning on a large table.

## SSC-FDM-DR0015

Druid CLUSTERED BY pre-sorts rows within each ingested segment by the listed keys; the translated Snowflake INSERT omits the clause and makes no within-segment ordering guarantee.

#### Description

`CLUSTERED BY` pre-sorts rows inside each Druid segment by the listed keys. The generated Snowflake `INSERT` omits the clause and makes no guarantee about the physical ordering of the inserted rows, so this difference is reported. The clause is dropped whether the keys are plain columns or expressions, and a statement using both `PARTITIONED BY <granularity>` and `CLUSTERED BY` carries this marker alongside SSC-FDM-DR0014.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
INSERT INTO DailySales SELECT * FROM SalesStage PARTITIONED BY ALL CLUSTERED BY store_id;
```

##### Output Code:

##### Snowflake

Copy code

```
INSERT INTO DailySales SELECT * FROM SalesStage /*** SSC-FDM-DR0015 - DRUID CLUSTERED BY PRE-SORTS ROWS WITHIN EACH INGESTED SEGMENT BY THE LISTED KEYS; THE TRANSLATED SNOWFLAKE INSERT OMITS THE CLAUSE AND MAKES NO WITHIN-SEGMENT ORDERING GUARANTEE ***/;
```

#### Best Practices

- Add an explicit `ORDER BY` to any query whose output order previously depended on the ingestion sort.
- Evaluate a Snowflake clustering key on the same columns when the goal was scan pruning rather than result ordering.

## SSC-FDM-DR0017

Druid applies the granularity timeZone to bucket boundaries, but the translated Snowflake DATE\_TRUNC/TIME\_SLICE aligns to calendar/epoch boundaries, so bucket edges may differ.

#### Description

A native query granularity may carry a `timeZone`, which Druid uses to place the bucket boundaries. The translation converts the timestamp with [CONVERT\_TIMEZONE](/sql-reference/functions/convert_timezone) before applying [DATE\_TRUNC](/sql-reference/functions/date_trunc) or `TIME_SLICE`, but those functions align to calendar or epoch boundaries, so the resulting bucket edges can differ from Druid’s. The difference is reported as a leading comment on the generated query.

#### Code Example

##### Input Code:

##### Druid

Copy code

```
{
  "queryType": "timeseries",
  "dataSource": "sales",
  "granularity": {"type": "period", "period": "PT1H", "timeZone": "America/Los_Angeles"},
  "aggregations": [{"type": "count", "name": "cnt"}],
  "intervals": ["2026-01-01T00:00:00Z/2026-01-02T00:00:00Z"]
}
```

##### Output Code:

##### Snowflake

Copy code

```
-- ** SSC-FDM-DR0017 - DRUID APPLIES THE GRANULARITY TIMEZONE TO BUCKET BOUNDARIES, BUT THE TRANSLATED SNOWFLAKE DATE_TRUNC/TIME_SLICE ALIGNS TO CALENDAR/EPOCH BOUNDARIES, SO BUCKET EDGES MAY DIFFER. **
SELECT
DATE_TRUNC('HOUR', CONVERT_TIMEZONE('UTC', 'America/Los_Angeles', __time)) AS __time_bucket,
COUNT(*) AS cnt
FROM
sales
WHERE
__time >= TIMESTAMP '2026-01-01 00:00:00'
AND __time < TIMESTAMP '2026-01-02 00:00:00'
GROUP BY
DATE_TRUNC('HOUR', CONVERT_TIMEZONE('UTC', 'America/Los_Angeles', __time))
ORDER BY
__time_bucket ASC NULLS LAST;
```

#### Best Practices

- Compare bucket totals around daylight-saving transitions, where the boundary placement is most likely to diverge.
- Check granularities that do not divide evenly into a calendar unit, since epoch-aligned slicing and Druid’s period boundaries drift apart fastest there.
