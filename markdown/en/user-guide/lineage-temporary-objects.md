# Preserving data lineage through temporary tables and views

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Overview

Data lineage lets you trace how data flows between objects in your account. It helps you understand dependencies, assess the impact of
schema or pipeline changes, and audit how data moved from one place to another.

Many pipelines use temporary tables and views as intermediate steps. For example, you might stage data in a temporary table before loading
it into its final destination. Previously, after that temporary object was dropped, either explicitly or automatically at the end of a
session, the lineage relationships that ran through it could be lost, leaving a gap in the lineage graph between the original source and the
final destination.

Snowflake now automatically preserves lineage across temporary objects when they’re dropped or purged. Lineage graphs and any tooling built
on lineage data, such as views in Snowsight or lineage metadata surfaced through `ACCOUNT_USAGE`, continue to show a complete and
accurate picture of how your data moved, even after intermediate temporary objects are cleaned up.

## How it works

Consider a pipeline where:

1. Data is loaded into table `a`.
2. A temporary table `t` is created from `a`:

   Copy code

   ```
   CREATE TEMPORARY TABLE t AS SELECT * FROM a;
   ```
3. Table `b` is created from `t`:

   Copy code

   ```
   CREATE TABLE b AS SELECT * FROM t;
   ```

Table `t` sits between `a` and `b` in the lineage chain. When `t` is dropped or automatically purged, Snowflake recognizes that it has both
an upstream source (`a`) and a downstream destination (`b`), and does the following:

- Records a direct lineage relationship from `a` to `b`, reflecting that data ultimately flowed from `a` into `b`.
- Removes the lineage relationships that referenced `t`, because `t` no longer exists and can no longer be resolved in lineage results.

The same bridging is applied at the column level. If a column in `b` was derived from a column in `t`, which was in turn derived from a
column in `a`, the resulting lineage shows the column in `b` as derived directly from the column in `a`.

This also applies to temporary views used in a similar way. For example, a temporary view created over a source object and then queried to
populate a destination table.

## Example

The following example creates two source tables, joins them into a temporary table, and then creates a final destination table from the
temporary table:

Copy code

```
-- Source table 1: 2 columns
CREATE DATABASE IF NOT EXISTS lineage_db;

USE DATABASE lineage_db;
USE SCHEMA public;

CREATE OR REPLACE TABLE lineage_src_1 (
  id NUMBER,
  amount NUMBER);

-- Source table 2: 3 columns
CREATE OR REPLACE TABLE lineage_src_2 (
  id NUMBER,
  region STRING,
  category STRING);

-- Middle temporary table created by joining the two sources
-- (copies some but not all columns)
CREATE OR REPLACE TEMPORARY TABLE lineage_tmp AS
  SELECT
      s1.id,
      s1.amount,
      s2.region
    FROM lineage_src_1 s1
    JOIN lineage_src_2 s2
      ON s1.id = s2.id;

-- Final regular destination table created from the temporary table
-- (again, copies a subset of columns)
CREATE OR REPLACE TABLE lineage_dest AS
  SELECT
      id,
      region
    FROM lineage_tmp;
```

Retrieve the lineage for the destination and source tables:

Copy code

```
SELECT *
  FROM TABLE(
    SNOWFLAKE.CORE.GET_LINEAGE(
      'lineage_db.public.lineage_dest',
      'TABLE',
      'UPSTREAM',
      5));

SELECT *
  FROM TABLE(
    SNOWFLAKE.CORE.GET_LINEAGE(
      'lineage_db.public.lineage_src_1',
      'TABLE',
      'DOWNSTREAM',
      5));
```

Now drop the temporary table:

Copy code

```
DROP TABLE lineage_tmp;
```

Even after the drop, the following queries return the lineage between the destination and source tables:

Copy code

```
SELECT *
  FROM TABLE(
    SNOWFLAKE.CORE.GET_LINEAGE(
      'lineage_db.public.lineage_dest',
      'TABLE',
      'UPSTREAM',
      5));

SELECT *
  FROM TABLE(
    SNOWFLAKE.CORE.GET_LINEAGE(
      'lineage_db.public.lineage_src_1',
      'TABLE',
      'DOWNSTREAM',
      5));
```

This feature also supports a chain of temporary nodes. For example, if there’s an upstream object followed by two or more temporary nodes and
a destination table, the lineage is preserved. Currently, Snowflake supports this for temporary node chains of up to 10 nodes.

## Considerations

- This applies to temporary tables and temporary views used as intermediate steps in a lineage chain.
- Lineage is preserved only for temporary objects that act as a genuine bridge, that is, they have both an upstream source and a downstream
  destination, where the destination is specifically a table. A temporary object with only an upstream source or only a downstream
  destination, but not both, has nothing to bridge and is cleaned up normally, without a replacement lineage relationship.
- The lineage relationship written in place of the temporary object retains the original timestamp and query information from when the data
  actually moved, so lineage history continues to reflect when the data movement occurred.
- This behavior is automatic and requires no configuration or action on your part.

## Limitations

- This feature isn’t supported for transient tables.
- For chained temporary nodes, especially with views or object dependency relationships, race conditions can occur where deletions cause the
  lineage to appear broken. The time period between the deletions of the temporary nodes can affect the resulting lineage graph. For
  example, consider this scenario:

  `object` » `temp_view1` » `temp_view2` » `table`

  The expected lineage after the temporary views are dropped is `object` » `table`. Snowflake expects this to be fairly rare. One way to
  reduce the chances of this happening is to delete the temporary nodes together if you do it manually. This is automatic if you choose to
  just end the session. This only reduces the probability of the issue and doesn’t eliminate it.
